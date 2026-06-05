"""
Hybrid Recommendation Engine (TF-IDF + Multi-Signal Scoring)
=============================================================
This module implements Suggestify's core recommendation system using a
HYBRID approach that combines multiple signals:

1. TF-IDF Content Similarity — finds products with similar text descriptions
2. Category Matching — boosts products in the same category
3. Brand Similarity — boosts products from the same brand
4. Price Range Similarity — recommends products in similar price ranges
5. Popularity Score — considers ratings and interaction counts

HOW THE HYBRID SCORING WORKS:
  final_score = 0.40 × tfidf_similarity
              + 0.20 × category_match
              + 0.15 × brand_match
              + 0.10 × price_similarity
              + 0.15 × popularity_score

This ensures recommendations feel smarter — not just text-similar, but
also appropriate in category, brand, and price.

DIVERSITY FILTER:
  To avoid recommending 5 Nike shoes when you view 1 Nike shoe, we cap
  recommendations to max 2 products per brand.
"""

import sys
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Add project root to path so we can import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Set up logging
logger = logging.getLogger('suggestify.recommendation')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    logger.addHandler(handler)


# ─── Hybrid Scoring Weights ────────────────────────────────────────────────
# These can be tuned. They must sum to 1.0
WEIGHT_TFIDF = 0.40
WEIGHT_CATEGORY = 0.20
WEIGHT_BRAND = 0.15
WEIGHT_PRICE = 0.10
WEIGHT_POPULARITY = 0.15

# Diversity: max products from the same brand in one recommendation set
MAX_PER_BRAND = 2


class TFIDFRecommender:
    """
    Hybrid recommendation engine using TF-IDF + multi-signal scoring.

    This class:
    - Loads all products from the MySQL database
    - Builds TF-IDF vectors from product text data
    - Pre-computes a cosine similarity matrix between all products
    - Provides methods to find similar products with hybrid scoring
    - Applies diversity filtering to avoid repetitive recommendations

    Uses a singleton pattern — only one instance exists in memory.
    The model is built lazily on first use and cached for fast lookups.
    """

    _instance = None       # Singleton instance
    _is_initialized = False  # Track if model has been built

    def __new__(cls):
        """Singleton pattern: ensure only one instance exists in memory."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the recommender (only runs once due to singleton)."""
        if not TFIDFRecommender._is_initialized:
            # Product data storage
            self.product_ids = []          # List of product IDs in order
            self.product_data = {}         # Dict mapping product_id -> product info
            self.id_to_index = {}          # Dict mapping product_id -> matrix index

            # ML model components
            self.tfidf_vectorizer = None   # The TF-IDF vectorizer
            self.tfidf_matrix = None       # The TF-IDF feature matrix
            self.similarity_matrix = None  # The cosine similarity matrix

            # Popularity data
            self.popularity_scores = {}    # product_id -> normalized popularity score

            self.is_built = False
            TFIDFRecommender._is_initialized = True

    def _load_products_from_db(self):
        """Load all products from the MySQL database."""
        try:
            from ..database.db_connection import get_connection
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, name, category, brand, price, rating, description,
                       image_url
                FROM products
            """)
            products = cursor.fetchall()
            cursor.close()
            conn.close()
            logger.info(f"Loaded {len(products)} products from database")
            return products
        except Exception as e:
            logger.error(f"ERROR loading products from DB: {e}")
            return []

    def _load_popularity_from_db(self):
        """
        Load interaction counts to compute popularity scores.
        Products with more interactions (views, clicks, purchases) are more popular.
        """
        try:
            from ..database.db_connection import get_connection
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT product_id, 
                       COUNT(*) as interaction_count,
                       SUM(CASE WHEN action = 'purchase' THEN 3
                                WHEN action = 'add_to_cart' THEN 2
                                WHEN action = 'rating' THEN 2
                                WHEN action = 'click' THEN 1
                                ELSE 0.5 END) as weighted_count
                FROM user_activity
                GROUP BY product_id
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            if rows:
                max_weighted = max(r['weighted_count'] for r in rows) or 1
                return {r['product_id']: r['weighted_count'] / max_weighted for r in rows}
            return {}
        except Exception as e:
            logger.warning(f"Could not load popularity data: {e}")
            return {}

    def _build_combined_text(self, product):
        """
        Combine product text fields into a single string for TF-IDF.

        We concatenate: name + brand + category (2x weight) + description + tags
        Missing values are replaced with empty strings to avoid errors.
        """
        name = str(product.get('name', '') or '')
        brand = str(product.get('brand', '') or '')
        category = str(product.get('category', '') or '')
        description = str(product.get('description', '') or '')
        tags = str(product.get('tags', '') or '')
        features = str(product.get('features', '') or '')

        # Repeat category and brand to give them extra weight in TF-IDF
        combined = f"{name} {brand} {brand} {category} {category} {description} {tags} {features}"
        return combined.strip()

    def _compute_price_range(self, price):
        """Classify price into a range category."""
        if price is None:
            return 'unknown'
        price = float(price)
        if price < 50:
            return 'budget'
        elif price < 150:
            return 'mid-range'
        elif price < 500:
            return 'premium'
        else:
            return 'luxury'

    def build(self):
        """
        Build the TF-IDF model, cosine similarity matrix, and popularity scores.

        This is the main training step:
        1. Load products from database
        2. Create combined text for each product
        3. Fit TF-IDF vectorizer to convert text → numerical vectors
        4. Compute cosine similarity between all product pairs
        5. Load popularity data from interaction history

        Called lazily on first recommendation request, then cached.
        """
        try:
            logger.info("Building hybrid recommendation model...")

            # Step 1: Load products
            products = self._load_products_from_db()
            if not products:
                logger.warning("No products found, model not built")
                return False

            # Step 2: Store product data and build text corpus
            self.product_ids = []
            self.product_data = {}
            self.id_to_index = {}
            corpus = []

            for idx, product in enumerate(products):
                pid = product['id']
                self.product_ids.append(pid)
                self.product_data[pid] = product
                self.id_to_index[pid] = idx
                text = self._build_combined_text(product)
                corpus.append(text)

            # Step 3: Fit TF-IDF Vectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95,
                sublinear_tf=True
            )
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)

            # Step 4: Compute Cosine Similarity Matrix
            self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

            # Step 5: Load popularity scores
            self.popularity_scores = self._load_popularity_from_db()

            self.is_built = True
            num_features = self.tfidf_matrix.shape[1]
            logger.info(f"Model built successfully!")
            logger.info(f"  Products: {len(products)}")
            logger.info(f"  TF-IDF features: {num_features}")
            logger.info(f"  Similarity matrix: {self.similarity_matrix.shape}")
            logger.info(f"  Products with popularity data: {len(self.popularity_scores)}")
            return True

        except Exception as e:
            logger.error(f"ERROR building model: {e}")
            import traceback
            traceback.print_exc()
            self.is_built = False
            return False

    def _ensure_built(self):
        """Lazy initialization: build the model on first use."""
        if not self.is_built:
            self.build()
        return self.is_built

    def _compute_hybrid_score(self, source_id, candidate_id):
        """
        Compute the hybrid recommendation score between two products.

        Returns a dict with the breakdown:
        {
            'final_score': float,
            'tfidf': float,
            'category': float,
            'brand': float,
            'price': float,
            'popularity': float
        }
        """
        source = self.product_data.get(source_id, {})
        candidate = self.product_data.get(candidate_id, {})

        # 1. TF-IDF content similarity (from pre-computed matrix)
        idx_a = self.id_to_index.get(source_id)
        idx_b = self.id_to_index.get(candidate_id)
        tfidf_score = float(self.similarity_matrix[idx_a][idx_b]) if idx_a is not None and idx_b is not None else 0.0

        # 2. Category match (1.0 if same, 0.0 if different)
        cat_score = 1.0 if source.get('category') == candidate.get('category') else 0.0

        # 3. Brand match (1.0 if same, 0.0 if different)
        brand_score = 1.0 if source.get('brand') == candidate.get('brand') else 0.0

        # 4. Price similarity (closer prices = higher score)
        source_price = float(source.get('price', 0) or 0)
        cand_price = float(candidate.get('price', 0) or 0)
        if source_price > 0 and cand_price > 0:
            ratio = min(source_price, cand_price) / max(source_price, cand_price)
            price_score = ratio  # 1.0 if same price, approaches 0 if very different
        else:
            price_score = 0.0

        # 5. Popularity score (from interaction data)
        pop_score = float(self.popularity_scores.get(candidate_id, 0.0))
        # Also factor in the product rating
        rating = float(candidate.get('rating', 0) or 0)
        rating_norm = rating / 5.0  # Normalize to 0-1
        pop_score = 0.6 * pop_score + 0.4 * rating_norm  # Blend interactions + rating

        # Weighted hybrid score
        final = (
            WEIGHT_TFIDF * tfidf_score +
            WEIGHT_CATEGORY * cat_score +
            WEIGHT_BRAND * brand_score +
            WEIGHT_PRICE * price_score +
            WEIGHT_POPULARITY * pop_score
        )

        return {
            'final_score': final,
            'tfidf': tfidf_score,
            'category': cat_score,
            'brand': brand_score,
            'price': price_score,
            'popularity': pop_score
        }

    def _apply_diversity_filter(self, scored_list, max_per_brand=MAX_PER_BRAND):
        """
        Apply diversity filtering to avoid too many products from the same brand.

        Input: list of (product_id, score_dict) sorted by final_score desc
        Output: filtered list with at most max_per_brand per brand
        """
        brand_counts = {}
        filtered = []

        for pid, score_info in scored_list:
            product = self.product_data.get(pid, {})
            brand = product.get('brand', 'Unknown')

            if brand_counts.get(brand, 0) < max_per_brand:
                filtered.append((pid, score_info))
                brand_counts[brand] = brand_counts.get(brand, 0) + 1

        return filtered

    def get_similar_products(self, product_id, top_n=10):
        """
        Find the most similar products using HYBRID scoring.

        This is the upgraded version that uses multiple signals,
        not just TF-IDF cosine similarity.

        Args:
            product_id: The ID of the product to find similar items for
            top_n: Number of similar products to return (default 10)

        Returns:
            List of tuples: [(product_id, similarity_score), ...]
            Sorted by hybrid score in descending order.
        """
        try:
            if not self._ensure_built():
                return []

            if product_id not in self.id_to_index:
                logger.warning(f"Product {product_id} not found in model")
                return []

            # Compute hybrid scores for all candidates
            scored = []
            for pid in self.product_ids:
                if pid == product_id:
                    continue
                score_info = self._compute_hybrid_score(product_id, pid)
                scored.append((pid, score_info))

            # Sort by final hybrid score
            scored.sort(key=lambda x: x[1]['final_score'], reverse=True)

            # Apply diversity filter
            scored = self._apply_diversity_filter(scored)

            # Log top recommendations for debugging
            if scored:
                source = self.product_data.get(product_id, {})
                logger.info(f"Hybrid recommendations for '{source.get('name', 'Unknown')}':")
                for pid, info in scored[:3]:
                    cand = self.product_data.get(pid, {})
                    logger.info(
                        f"  → {cand.get('name', '?')}: "
                        f"final={info['final_score']:.3f} "
                        f"(tfidf={info['tfidf']:.2f}, cat={info['category']:.0f}, "
                        f"brand={info['brand']:.0f}, price={info['price']:.2f}, "
                        f"pop={info['popularity']:.2f})"
                    )

            # Return as (product_id, final_score) tuples for backward compatibility
            results = [(pid, info['final_score']) for pid, info in scored[:top_n]]
            return results

        except Exception as e:
            logger.error(f"ERROR in get_similar_products: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_similar_to_multiple(self, product_ids, top_n=12):
        """
        Find products similar to MULTIPLE products (used for user history).

        Computes the average hybrid score across all provided products,
        giving a "combined recommendation" score.

        Args:
            product_ids: List of product IDs the user has interacted with
            top_n: Number of recommendations to return

        Returns:
            List of tuples: [(product_id, avg_score), ...]
        """
        try:
            if not self._ensure_built():
                return []

            if not product_ids:
                return []

            # Filter to only products that exist in our model
            valid_ids = [pid for pid in product_ids if pid in self.id_to_index]
            if not valid_ids:
                return []

            # For efficiency, use TF-IDF similarity as the primary signal
            # (computing full hybrid for every product × every history item is expensive)
            indices = [self.id_to_index[pid] for pid in valid_ids]
            avg_tfidf_scores = np.mean(self.similarity_matrix[indices], axis=0)

            # Build scored list with popularity boost
            exclude_set = set(valid_ids)
            scored = []
            for i, tfidf_score in enumerate(avg_tfidf_scores):
                pid = self.product_ids[i]
                if pid not in exclude_set:
                    # Blend TF-IDF with popularity for the multi-product case
                    pop = self.popularity_scores.get(pid, 0.0)
                    rating = float(self.product_data.get(pid, {}).get('rating', 0) or 0) / 5.0
                    pop_blend = 0.6 * pop + 0.4 * rating

                    final = 0.70 * float(tfidf_score) + 0.30 * pop_blend
                    scored.append((pid, final))

            scored.sort(key=lambda x: x[1], reverse=True)

            # Apply diversity filter
            scored_with_info = [(pid, {'final_score': s}) for pid, s in scored]
            filtered = self._apply_diversity_filter(scored_with_info)
            result = [(pid, info['final_score']) for pid, info in filtered[:top_n]]

            return result

        except Exception as e:
            logger.error(f"ERROR in get_similar_to_multiple: {e}")
            return []

    def get_similarity_score(self, product_id_a, product_id_b):
        """
        Get the cosine similarity score between two specific products.
        Returns a float between 0.0 and 1.0.
        """
        try:
            if not self._ensure_built():
                return 0.0
            if product_id_a not in self.id_to_index or product_id_b not in self.id_to_index:
                return 0.0
            idx_a = self.id_to_index[product_id_a]
            idx_b = self.id_to_index[product_id_b]
            return float(self.similarity_matrix[idx_a][idx_b])
        except Exception as e:
            logger.error(f"ERROR in get_similarity_score: {e}")
            return 0.0

    def get_hybrid_score(self, product_id_a, product_id_b):
        """
        Get the full hybrid score breakdown between two products.
        Returns a dict with score components.
        """
        try:
            if not self._ensure_built():
                return {'final_score': 0.0}
            return self._compute_hybrid_score(product_id_a, product_id_b)
        except Exception as e:
            logger.error(f"ERROR in get_hybrid_score: {e}")
            return {'final_score': 0.0}

    def rebuild(self):
        """Force rebuild the model (e.g., after products are added/updated)."""
        logger.info("Rebuilding model...")
        self.is_built = False
        self.product_ids = []
        self.product_data = {}
        self.id_to_index = {}
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.popularity_scores = {}
        return self.build()

    def get_model_info(self):
        """Return info about the current model state (useful for debugging)."""
        if not self.is_built:
            return {"status": "not_built", "products": 0, "features": 0}
        return {
            "status": "built",
            "products": len(self.product_ids),
            "features": self.tfidf_matrix.shape[1] if self.tfidf_matrix is not None else 0,
            "matrix_shape": list(self.similarity_matrix.shape) if self.similarity_matrix is not None else [],
            "popularity_products": len(self.popularity_scores),
            "weights": {
                "tfidf": WEIGHT_TFIDF,
                "category": WEIGHT_CATEGORY,
                "brand": WEIGHT_BRAND,
                "price": WEIGHT_PRICE,
                "popularity": WEIGHT_POPULARITY
            }
        }


# ─── Singleton accessor ─────────────────────────────────────────────────────
def get_recommender():
    """Get the singleton TFIDFRecommender instance."""
    return TFIDFRecommender()
