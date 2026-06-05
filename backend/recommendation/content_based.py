"""
Content-Based Recommendation Module
===================================
Handles TF-IDF vectorization and cosine similarity calculations.
"""

import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..data_processor import build_combined_text

logger = logging.getLogger('suggestify.recommendation.content_based')

class ContentBasedRecommender:
    def __init__(self):
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.id_to_index = {}
        self.is_built = False

    def build(self, products):
        """
        Build the TF-IDF model and cosine similarity matrix.
        
        Args:
            products: List of product dictionaries.
        """
        try:
            logger.info("Building content-based (TF-IDF) model...")
            
            self.id_to_index = {}
            corpus = []
            
            for idx, product in enumerate(products):
                pid = product['id']
                self.id_to_index[pid] = idx
                text = build_combined_text(product)
                corpus.append(text)
                
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95,
                sublinear_tf=True
            )
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
            self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
            
            self.is_built = True
            logger.info(f"Content-based model built. Features: {self.tfidf_matrix.shape[1]}")
            return True
            
        except Exception as e:
            logger.error(f"ERROR building content-based model: {e}")
            import traceback
            traceback.print_exc()
            self.is_built = False
            return False

    def get_similarity_score(self, source_id, candidate_id):
        """Get the precomputed cosine similarity score between two products."""
        if not self.is_built:
            return 0.0
            
        idx_a = self.id_to_index.get(source_id)
        idx_b = self.id_to_index.get(candidate_id)
        
        if idx_a is not None and idx_b is not None:
            return float(self.similarity_matrix[idx_a][idx_b])
        return 0.0

    def get_avg_similarity(self, candidate_id, source_ids):
        """Get the average similarity between a candidate and a list of source IDs."""
        if not self.is_built or not source_ids:
            return 0.0
            
        idx_c = self.id_to_index.get(candidate_id)
        if idx_c is None:
            return 0.0
            
        valid_indices = [self.id_to_index[pid] for pid in source_ids if pid in self.id_to_index]
        if not valid_indices:
            return 0.0
            
        # Get the scores for this candidate against all valid source indices
        # similarity_matrix is symmetric, so we can check row idx_c and cols valid_indices
        scores = self.similarity_matrix[idx_c, valid_indices]
        return float(scores.mean())
