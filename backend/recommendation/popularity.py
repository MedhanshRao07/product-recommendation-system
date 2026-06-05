"""
Popularity Recommendation Module
================================
Handles loading and computing popularity scores based on user interactions.
"""

import logging

logger = logging.getLogger('suggestify.recommendation.popularity')

class PopularityRecommender:
    def __init__(self):
        self.popularity_scores = {}
        self.is_built = False

    def build(self):
        """Load interaction counts and compute normalized popularity scores."""
        try:
            logger.info("Loading popularity data from database...")
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
                self.popularity_scores = {r['product_id']: r['weighted_count'] / max_weighted for r in rows}
            else:
                self.popularity_scores = {}
                
            self.is_built = True
            logger.info(f"Loaded popularity data for {len(self.popularity_scores)} products.")
            return True
            
        except Exception as e:
            logger.warning(f"Could not load popularity data: {e}")
            self.popularity_scores = {}
            self.is_built = False
            return False

    def get_score(self, product_id, product_data=None):
        """
        Get the popularity score for a product.
        Blends interaction-based popularity with the product's static rating.
        """
        pop_score = float(self.popularity_scores.get(product_id, 0.0))
        
        rating_norm = 0.0
        if product_data:
            rating = float(product_data.get('rating', 0) or 0)
            rating_norm = rating / 5.0
            
        # Blend interactions + rating (60/40 blend as in original logic)
        blended_score = 0.6 * pop_score + 0.4 * rating_norm
        return pop_score, blended_score
