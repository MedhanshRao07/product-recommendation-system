"""
Collaborative Filtering Engine
==============================
Provides lightweight collaborative filtering based on user interactions.
It uses a co-occurrence matrix to find products that are frequently interacted
with together (e.g., "Users who viewed X also viewed Y").

Since we want to keep the architecture simple and beginner-friendly,
this does NOT use heavy ML libraries like TensorFlow or PyTorch.
It relies purely on counting co-occurrences in the user_activity data
and using numpy for simple matrix operations.
"""

import sys
import os
import numpy as np
import logging
from collections import defaultdict

logger = logging.getLogger('suggestify.collaborative')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    logger.addHandler(handler)

class CollaborativeFilter:
    """
    Lightweight collaborative filtering engine.
    Computes an item-item co-occurrence matrix from interaction data.
    """
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not CollaborativeFilter._is_initialized:
            self.cooccurrence_matrix = {} # format: {product_id: {other_id: score}}
            self.product_frequencies = {} # format: {product_id: total_score}
            self.is_built = False
            CollaborativeFilter._is_initialized = True

    def build(self):
        """
        Build the co-occurrence matrix by reading the user_activity table.
        """
        try:
            logger.info("Building collaborative filtering model...")
            from ..database.db_connection import get_connection
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Fetch all user activities
            cursor.execute("""
                SELECT user_id, product_id, action
                FROM user_activity
                ORDER BY user_id, created_at
            """)
            activities = cursor.fetchall()
            cursor.close()
            conn.close()

            if not activities:
                logger.warning("No activity data found. Collaborative model empty.")
                self.is_built = True
                return True

            # Group activities by user
            user_history = defaultdict(list)
            for row in activities:
                # Weight actions differently
                weight = 1.0
                if row['action'] == 'purchase':
                    weight = 5.0
                elif row['action'] == 'add_to_cart':
                    weight = 3.0
                elif row['action'] == 'rating':
                    weight = 2.0
                    
                user_history[row['user_id']].append((row['product_id'], weight))

            # Build co-occurrence matrix
            co_matrix = defaultdict(lambda: defaultdict(float))
            frequencies = defaultdict(float)

            for user_id, history in user_history.items():
                # Deduplicate history per user (take max weight if multiple actions on same product)
                unique_history = {}
                for pid, weight in history:
                    unique_history[pid] = max(unique_history.get(pid, 0), weight)
                
                pids = list(unique_history.keys())
                for i in range(len(pids)):
                    pid1 = pids[i]
                    w1 = unique_history[pid1]
                    frequencies[pid1] += w1
                    
                    for j in range(i + 1, len(pids)):
                        pid2 = pids[j]
                        w2 = unique_history[pid2]
                        
                        # Add to both sides (symmetric matrix)
                        combined_weight = min(w1, w2) # or (w1+w2)/2
                        co_matrix[pid1][pid2] += combined_weight
                        co_matrix[pid2][pid1] += combined_weight

            # Normalize the matrix (Jaccard-like similarity or cosine-like)
            # score(A,B) = co_occurrences(A,B) / sqrt(freq(A) * freq(B))
            normalized_matrix = defaultdict(dict)
            for p1, neighbors in co_matrix.items():
                for p2, co_score in neighbors.items():
                    if frequencies[p1] > 0 and frequencies[p2] > 0:
                        norm_score = co_score / np.sqrt(frequencies[p1] * frequencies[p2])
                        normalized_matrix[p1][p2] = norm_score

            self.cooccurrence_matrix = normalized_matrix
            self.product_frequencies = frequencies
            self.is_built = True
            
            logger.info(f"Collaborative model built successfully! "
                        f"Items in matrix: {len(self.cooccurrence_matrix)}")
            return True

        except Exception as e:
            logger.error(f"ERROR building collaborative model: {e}")
            import traceback
            traceback.print_exc()
            self.is_built = False
            return False

    def _ensure_built(self):
        if not self.is_built:
            self.build()
        return self.is_built

    def get_collaborative_recommendations(self, product_ids, exclude_ids=None, top_n=10):
        """
        Get recommendations based on a list of product IDs (e.g., user's history).
        
        Args:
            product_ids: list of product IDs the user likes/viewed
            exclude_ids: set of product IDs to exclude from results
            top_n: number of recommendations to return
            
        Returns:
            List of (product_id, score) tuples
        """
        if not self._ensure_built():
            return []
            
        if not product_ids:
            return []
            
        if exclude_ids is None:
            exclude_ids = set()
        
        # Add input products to exclude list so we don't recommend what they already viewed
        exclude_set = set(exclude_ids)
        exclude_set.update(product_ids)
        
        scores = defaultdict(float)
        
        # Sum up similarities for all input products
        for pid in product_ids:
            if pid in self.cooccurrence_matrix:
                for neighbor_id, score in self.cooccurrence_matrix[pid].items():
                    if neighbor_id not in exclude_set:
                        scores[neighbor_id] += score
                        
        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:top_n]

    def rebuild(self):
        self.is_built = False
        return self.build()

def get_collaborative_filter():
    return CollaborativeFilter()
