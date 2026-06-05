"""
Hybrid Recommendation Engine (TF-IDF + Multi-Signal Scoring)
=============================================================
This module acts as the orchestrator combining signals from content-based
similarity and popularity/interaction metrics.

HOW THE HYBRID SCORING WORKS:
  final_score = 0.40 × tfidf_similarity
              + 0.20 × category_match
              + 0.15 × brand_match
              + 0.10 × price_similarity
              + 0.15 × popularity_score

DIVERSITY FILTER:
  To avoid recommending 5 Nike shoes when you view 1 Nike shoe, we cap
  recommendations to max 2 products per brand.
"""

import sys
import os
import numpy as np
import logging

from .content_based import ContentBasedRecommender
from .popularity import PopularityRecommender

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

            # Recommendation modules
            self.content_recommender = ContentBasedRecommender()
            self.popularity_recommender = PopularityRecommender()

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

    def build(self):
        """
        Build the recommendation models.
        """
        try:
            logger.info("Building hybrid recommendation model...")

            # Step 1: Load products
            products = self._load_products_from_db()
            if not products:
                logger.warning("No products found, model not built")
                return False

            self.product_ids = []
            self.product_data = {}
            for product in products:
                pid = product['id']
                self.product_ids.append(pid)
                self.product_data[pid] = product

            # Step 2: Build content-based model
            content_success = self.content_recommender.build(products)
            
            # Step 3: Build popularity model
            pop_success = self.popularity_recommender.build()

            self.is_built = content_success and pop_success
            
            if self.is_built:
                logger.info("Hybrid model built successfully!")
                logger.info(f"  Products: {len(products)}")
            else:
                logger.warning("Hybrid model build had issues.")
                
            return self.is_built

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
        """
        source = self.product_data.get(source_id, {})
        candidate = self.product_data.get(candidate_id, {})

        # 1. TF-IDF content similarity (from pre-computed matrix)
        tfidf_score = self.content_recommender.get_similarity_score(source_id, candidate_id)

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
        raw_pop, pop_score = self.popularity_recommender.get_score(candidate_id, candidate)

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
        """
        try:
            if not self._ensure_built():
                return []

            if product_id not in self.product_data:
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
        """
        try:
            if not self._ensure_built():
                return []

            if not product_ids:
                return []

            # Filter to only products that exist in our model
            valid_ids = [pid for pid in product_ids if pid in self.product_data]
            if not valid_ids:
                return []

            exclude_set = set(valid_ids)
            scored = []
            
            for pid in self.product_ids:
                if pid in exclude_set:
                    continue
                    
                # 1. Get average TF-IDF similarity to the user's history
                avg_tfidf = self.content_recommender.get_avg_similarity(pid, valid_ids)
                
                # 2. Get blended popularity score
                raw_pop, pop_blend = self.popularity_recommender.get_score(pid, self.product_data.get(pid))
                
                # Blend TF-IDF with popularity for the multi-product case
                final = 0.70 * avg_tfidf + 0.30 * pop_blend
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
            return self.content_recommender.get_similarity_score(product_id_a, product_id_b)
        except Exception as e:
            logger.error(f"ERROR in get_similarity_score: {e}")
            return 0.0

    def get_hybrid_score(self, product_id_a, product_id_b):
        """
        Get the full hybrid score breakdown between two products.
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
        self.content_recommender = ContentBasedRecommender()
        self.popularity_recommender = PopularityRecommender()
        return self.build()

    def get_model_info(self):
        """Return info about the current model state (useful for debugging)."""
        if not self.is_built:
            return {"status": "not_built", "products": 0, "features": 0}
        
        matrix_shape = []
        features = 0
        if self.content_recommender.similarity_matrix is not None:
            matrix_shape = list(self.content_recommender.similarity_matrix.shape)
            features = self.content_recommender.tfidf_matrix.shape[1]
            
        return {
            "status": "built",
            "products": len(self.product_ids),
            "features": features,
            "matrix_shape": matrix_shape,
            "popularity_products": len(self.popularity_recommender.popularity_scores),
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
