from ..database.db_connection import get_connection as get_db_connection

# ─── TF-IDF ML Recommender Import ──────────────────────────────────────────
# Import the content-based recommendation engine (TF-IDF + Cosine Similarity).
# This is used to enhance recommendations with machine learning.
# If import fails (e.g., scikit-learn not installed), we gracefully degrade.
try:
    from ..recommendation.engine import get_recommender
    from ..recommendation.collaborative import get_collaborative_filter
    import logging

    logger = logging.getLogger('suggestify.product_service')
    _ML_AVAILABLE = True
    print("[ProductService] ML recommenders loaded successfully")
except ImportError as e:
    _ML_AVAILABLE = False
    print(f"[ProductService] ML recommenders not available: {e}")
    print("[ProductService] Falling back to behavior-only recommendations")

class ProductService:
    @staticmethod
    def validate_product(product):
        """Validate a product before returning it to the frontend."""
        if not product:
            return False
            
        try:
            # Check for essential fields
            if not product.get('name') or not str(product.get('name')).strip():
                logger.warning(f"[Validation] Product {product.get('id')} rejected: missing title")
                return False
                
            if not product.get('category'):
                logger.warning(f"[Validation] Product {product.get('id', 'Unknown')} rejected: missing category")
                return False
                
            if not product.get('brand'):
                logger.warning(f"[Validation] Product {product.get('id', 'Unknown')} rejected: missing brand")
                return False
                
            # Validate price format
            try:
                price = float(product.get('price', 0))
                if price <= 0:
                    logger.warning(f"[Validation] Product {product.get('id')} rejected: invalid price {price}")
                    return False
            except (ValueError, TypeError):
                logger.warning(f"[Validation] Product {product.get('id')} rejected: non-numeric price")
                return False
                
            # Image validation
            image = product.get('image_url')
            if not image or image in ['url', 'url_here'] or (not str(image).startswith('http') and not str(image).startswith('/')):
                logger.warning(f"[Validation] Product {product.get('id')} has invalid image '{image}'. Assigning fallback.")
                
                # Deterministic product-centric fallback logic
                s_name = str(product.get('name', '')).lower()
                pid = int(product.get('id', 0))
                
                product_map = {
                    'smartwatch': [
                        '/images/products/rolex_submariner.png'
                    ],
                    'watch': [
                        '/images/products/rolex_submariner.png'
                    ],
                    'wallet': [
                        '/images/products/wallet1.png'
                    ],
                    'belt': [
                        '/images/products/belt1.png'
                    ],
                    'flannel': [
                        '/images/products/shirt1.png'
                    ],
                    'polo': [
                        '/images/products/polo.png'
                    ],
                    'shirt': [
                        '/images/products/shirt1.png'
                    ],
                    'sweater': [
                        '/images/products/patagonia_sweater.png'
                    ],
                    'shoe': [
                        '/images/products/nike_air_force.png',
                        '/images/products/new_balance.png'
                    ],
                    'sneaker': [
                        '/images/products/nike_air_force.png',
                        '/images/products/new_balance.png'
                    ],
                    'boot': [
                        '/images/products/timberland_boot.png'
                    ],
                    'headphones': [
                        '/images/products/sony_headphones.png'
                    ],
                    'keyboard': [
                        '/images/products/keyboard1.png'
                    ],
                    'mouse': [
                        '/images/products/mouse.png'
                    ],
                    'monitor': [
                        '/images/products/monitor.png'
                    ],
                    'tv': [
                        '/images/products/tv1.png'
                    ],
                    'power bank': [
                        '/images/products/powerbank1.png'
                    ],
                    'foam roller': [
                        '/images/products/foamroller1.png'
                    ],
                    'bottle': [
                        '/images/products/bottle1.png'
                    ],
                    'duffel bag': [
                        '/images/products/backpack1.png'
                    ],
                    'tote bag': [
                        '/images/products/backpack1.png'
                    ],
                    'backpack': [
                        '/images/products/backpack1.png'
                    ],
                    'bag': [
                        '/images/products/backpack1.png'
                    ],
                    'laptop': [
                        '/images/products/macbook_pro_14.png'
                    ],
                    'macbook': [
                        '/images/products/macbook_pro_14.png'
                    ],
                    'phone': [
                        '/images/products/iphone_15_pro.png',
                        '/images/products/galaxy_s24_ultra.png'
                    ],
                    'camera': [
                        '/images/products/canon_eos_r5.png'
                    ],
                    'air fryer': [
                        '/images/products/airfryer.png'
                    ],
                    'cookware set': [
                        '/images/products/cookware.png'
                    ],
                    'cookware': [
                        '/images/products/cookware.png'
                    ],
                    'kettle': [
                        '/images/products/kettle.png'
                    ],
                    'coffee maker': [
                        '/images/products/coffeemaker.png'
                    ],
                    'purifier': [
                        '/images/products/purifier.png'
                    ],
                    'kitchen appliance': [
                        '/images/products/airfryer.png'
                    ]
                }
                
                fallback_url = '/images/products/backpack1.png'
                for keyword, url_list in product_map.items():
                    if keyword in s_name:
                        fallback_url = url_list[pid % len(url_list)]
                        break
                        
                product['image_url'] = fallback_url
                
            return True
        except Exception as e:
            logger.error(f"[Validation] Error validating product {product.get('id', 'unknown')}: {e}")
            return False

    @staticmethod
    def filter_valid_products(products):
        """Filter a list of products, returning only valid ones."""
        valid_products = []
        seen_ids = set()
        
        for p in products:
            if not p or 'id' not in p:
                continue
            if p['id'] in seen_ids:
                logger.warning(f"[Validation] Product {p['id']} rejected: duplicate in payload")
                continue
                
            if ProductService.validate_product(p):
                valid_products.append(p)
                seen_ids.add(p['id'])
                
        return valid_products

    @staticmethod
    def get_all_products(page=None, per_page=20):
        """Get all products, with optional pagination."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            if page is not None:
                offset = (page - 1) * per_page
                cursor.execute("SELECT COUNT(*) as total FROM products")
                total = cursor.fetchone()['total']
                cursor.execute("SELECT * FROM products LIMIT %s OFFSET %s", (per_page, offset))
                products = cursor.fetchall()
                return ProductService.filter_valid_products(products)
            else:
                cursor.execute("SELECT * FROM products")
                products = cursor.fetchall()
                return ProductService.filter_valid_products(products)
        except Exception as e:
            print(f"Error: {e}")
            return [] if page is None else {'products': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def get_trending_products(limit=8):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products ORDER BY rating DESC LIMIT %s", (limit * 2,))
            products = cursor.fetchall()
            return ProductService.filter_valid_products(products)[:limit]
        except Exception as e:
            print(f"Error fetching trending products: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def get_product_by_id(product_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if product and ProductService.validate_product(product):
                return product
            return None
        except Exception as e:
            print(f"Error fetching product: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def get_products_by_category(category):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products WHERE category = %s", (category,))
            products = cursor.fetchall()
            return ProductService.filter_valid_products(products)
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def search_products(query):
        """Search products by name, brand, or description."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            search_term = f"%{query}%"
            cursor.execute("""
                SELECT * FROM products 
                WHERE name LIKE %s OR brand LIKE %s OR description LIKE %s 
                ORDER BY rating DESC
                LIMIT 50
            """, (search_term, search_term, search_term))
            products = cursor.fetchall()
            return ProductService.filter_valid_products(products)
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def get_categories():
        """Get all distinct product categories."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
            categories = [row[0] for row in cursor.fetchall()]
            return categories
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def get_grouped_products(per_category=6):
        """Get products grouped by category for homepage display."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
            categories = [row['category'] for row in cursor.fetchall()]
            
            grouped = {}
            for cat in categories:
                cursor.execute(
                    "SELECT * FROM products WHERE category = %s ORDER BY rating DESC LIMIT %s",
                    (cat, per_category)
                )
                grouped[cat] = ProductService.filter_valid_products(cursor.fetchall())
            
            return grouped
        except Exception as e:
            print(f"Error fetching grouped products: {e}")
            return {}
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def get_recommendations(category, max_price, rating):
        """Fallback chain for recommendations."""
        logger.info(f"[Recommendations] Requested strict filter: cat={category}, max_price={max_price}, rating={rating}")
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            if not category:
                logger.warning("[Recommendations] No category provided, returning trending")
                return ProductService.get_trending_products(10)
                
            # Default missing values to lenient ones
            m_price = max_price if max_price is not None and max_price != 'NaN' else 999999
            m_rating = rating if rating is not None and rating != 'NaN' else 0

            # 1. Attempt strict match
            query = """
                SELECT id, name, price, rating, image_url, description, brand, category
                FROM products 
                WHERE category = %s AND price <= %s AND rating >= %s 
                ORDER BY rating DESC 
                LIMIT 20
            """
            cursor.execute(query, (category, m_price, m_rating))
            products = ProductService.filter_valid_products(cursor.fetchall())
            if len(products) >= 4:
                logger.info(f"[Recommendations] Source: Strict Filter, Count: {len(products)}")
                return products[:10]
                
            logger.info("[Recommendations] Stage 1 (Strict) failed/insufficient. Falling back to category + price.")
            
            # 2. Fallback: ignore rating
            query2 = """
                SELECT id, name, price, rating, image_url, description, brand, category
                FROM products 
                WHERE category = %s AND price <= %s 
                ORDER BY rating DESC 
                LIMIT 20
            """
            cursor.execute(query2, (category, m_price))
            products = ProductService.filter_valid_products(cursor.fetchall())
            if len(products) >= 4:
                logger.info(f"[Recommendations] Source: Fallback (No Rating), Count: {len(products)}")
                return products[:10]

            logger.info("[Recommendations] Stage 2 (No Rating) failed/insufficient. Falling back to similar category.")

            # 3. Fallback: just category
            query3 = """
                SELECT id, name, price, rating, image_url, description, brand, category
                FROM products 
                WHERE category = %s
                ORDER BY rating DESC 
                LIMIT 20
            """
            cursor.execute(query3, (category,))
            products = ProductService.filter_valid_products(cursor.fetchall())
            if len(products) >= 4:
                logger.info(f"[Recommendations] Source: Fallback (Category Only), Count: {len(products)}")
                return products[:10]
                
            logger.info("[Recommendations] Stage 3 (Category) failed/insufficient. Falling back to top rated.")

            # 4. Fallback: top rated everywhere
            return ProductService.get_trending_products(10)
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def track_activity(user_id, product_id, action):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO user_activity (user_id, product_id, action) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, product_id, action))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error tracking activity: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def get_auto_recommendations(user_id):
        """
        Hybrid recommendation engine (Behavior + ML + Popularity):
        
        ORIGINAL LOGIC (preserved):
        1. Multi-category affinity — weights user's top 3 interacted categories
        2. Recency bias — recent interactions count more
        3. Excludes heavily-seen products
        4. Popularity fallback for cold-start users
        
        NEW ML LAYER (added on top):
        5. TF-IDF cosine similarity — re-ranks candidates based on content
           similarity to products the user has actually interacted with
        6. Hybrid scoring formula:
           final_score = (0.5 × behavior) + (0.3 × similarity) + (0.2 × popularity)
        7. If ML fails, returns the original behavior-only results (safe fallback)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # ── Step 1: Get user's category affinities with action weights ──
            # Add to Cart = 5, Compare = 2, View/Click = 1
            # Recent interactions (today) count 3x, last week 2x, older 1x
            affinity_query = """
                SELECT p.category, 
                       COUNT(*) as interaction_count,
                       SUM(
                           (CASE 
                               WHEN ua.action = 'add_to_cart' THEN 5
                               WHEN ua.action = 'cart' THEN 5
                               WHEN ua.action = 'compare' THEN 2
                               ELSE 1
                           END) *
                           (CASE 
                               WHEN ua.created_at >= DATE_SUB(NOW(), INTERVAL 1 DAY) THEN 3
                               WHEN ua.created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 2
                               ELSE 1
                           END)
                       ) as weighted_score
                FROM user_activity ua
                JOIN products p ON ua.product_id = p.id
                WHERE ua.user_id = %s
                GROUP BY p.category
                ORDER BY weighted_score DESC
                LIMIT 3
            """
            cursor.execute(affinity_query, (user_id,))
            affinities = cursor.fetchall()
            
            if not affinities:
                # Cold-start: return popular products across all categories
                logger.info(f"[Auto-Recommend] User {user_id} has no affinity, using trending fallback")
                cursor.execute("""
                    SELECT id, name, price, rating, image_url, description, brand, category
                    FROM products
                    ORDER BY rating DESC
                    LIMIT 30
                """)
                return ProductService.filter_valid_products(cursor.fetchall())[:12]
            
            # ── Step 2: Get products the user has interacted with heavily ──
            cursor.execute("""
                SELECT product_id, COUNT(*) as cnt
                FROM user_activity 
                WHERE user_id = %s
                GROUP BY product_id
                HAVING cnt >= 3
            """, (user_id,))
            excluded_ids = [row['product_id'] for row in cursor.fetchall()]
            
            # ── Step 3: Fetch candidate products from top categories ──
            # (weighted distribution based on category affinity scores)
            recommendations = []
            total_weight = sum(a['weighted_score'] for a in affinities)
            
            for affinity in affinities:
                cat = affinity['category']
                weight = affinity['weighted_score']
                # Allocate slots proportional to affinity weight (min 2, total ~12)
                slots = max(2, round(12 * weight / total_weight))
                
                if excluded_ids:
                    placeholders = ','.join(['%s'] * len(excluded_ids))
                    cursor.execute(f"""
                        SELECT id, name, price, rating, image_url, description, brand, category
                        FROM products
                        WHERE category = %s AND id NOT IN ({placeholders})
                        ORDER BY rating DESC
                        LIMIT %s
                    """, (cat, *excluded_ids, slots))
                else:
                    cursor.execute("""
                        SELECT id, name, price, rating, image_url, description, brand, category
                        FROM products
                        WHERE category = %s
                        ORDER BY rating DESC
                        LIMIT %s
                    """, (cat, slots))
                
                recommendations.extend(cursor.fetchall())
            
            # ── Step 4: Deduplicate ──
            seen_ids = set()
            unique_recs = []
            for rec in recommendations:
                if rec['id'] not in seen_ids:
                    seen_ids.add(rec['id'])
                    unique_recs.append(rec)
            
            # ── Step 5 (NEW): Merged ML Re-ranking ──
            if _ML_AVAILABLE and unique_recs:
                try:
                    recommender = get_recommender()
                    collab_filter = get_collaborative_filter()
                    
                    # Get user's interaction history (recent 20)
                    cursor.execute("""
                        SELECT DISTINCT product_id 
                        FROM user_activity 
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                        LIMIT 20
                    """, (user_id,))
                    user_history_ids = [row['product_id'] for row in cursor.fetchall()]
                    
                    if user_history_ids:
                        # 1. Get Collaborative Filtering scores
                        cf_results = collab_filter.get_collaborative_recommendations(
                            product_ids=user_history_ids,
                            exclude_ids=set(excluded_ids),
                            top_n=100
                        )
                        cf_score_map = {pid: score for pid, score in cf_results}
                        max_cf = max(cf_score_map.values()) if cf_score_map else 1.0
                        if max_cf > 0:
                            cf_score_map = {k: v/max_cf for k, v in cf_score_map.items()}

                        # 2. Get Hybrid Content-based scores
                        ml_scores = recommender.get_similar_to_multiple(
                            user_history_ids, top_n=100
                        )
                        ml_score_map = {pid: score for pid, score in ml_scores}
                        
                        max_rating = max((r.get('rating', 0) or 0) for r in unique_recs) or 5.0
                        
                        # 3. Hybrid Scoring Formula
                        # We evaluate the behavior candidates (unique_recs) but also add top ML candidates
                        candidate_pool = {rec['id']: rec for rec in unique_recs}
                        
                        # Add top CF/ML items to candidate pool if missing
                        for pid in list(cf_score_map.keys())[:5] + list(ml_score_map.keys())[:5]:
                            if pid not in candidate_pool and pid not in excluded_ids:
                                cursor.execute("SELECT id, name, price, rating, image_url, description, brand, category FROM products WHERE id = %s", (pid,))
                                prod = cursor.fetchone()
                                if prod:
                                    candidate_pool[pid] = prod
                        
                        scored_recs = []
                        for pid, rec in candidate_pool.items():
                            # Behavior score (only if in original unique_recs)
                            behavior_score = 0.0
                            for rank, orig_rec in enumerate(unique_recs):
                                if orig_rec['id'] == pid:
                                    behavior_score = 1.0 - (rank / max(len(unique_recs), 1))
                                    break
                            
                            similarity_score = ml_score_map.get(pid, 0.0)
                            collab_score = cf_score_map.get(pid, 0.0)
                            popularity_score = (rec.get('rating', 0) or 0) / max_rating
                            
                            # Final Hybrid Score (Ensemble)
                            final_score = (
                                0.40 * behavior_score +
                                0.30 * similarity_score +
                                0.15 * collab_score +
                                0.15 * popularity_score
                            )
                            
                            scored_recs.append((rec, final_score))
                        
                        scored_recs.sort(key=lambda x: x[1], reverse=True)
                        unique_recs = [rec for rec, score in scored_recs]
                        
                        print(f"[Hybrid] Merged {len(unique_recs)} recommendations for user {user_id}")
                        logger.info(f"[Auto-Recommend] Source: ML Hybrid, Count: {len(unique_recs)}")
                
                except Exception as ml_error:
                    print(f"[Hybrid] ML re-ranking failed (using behavior-only): {ml_error}")
                    logger.info(f"[Auto-Recommend] Source: Behavior Only, Count: {len(unique_recs)}")
            else:
                logger.info(f"[Auto-Recommend] Source: Behavior Only, Count: {len(unique_recs)}")
            
            # Apply safety validation
            valid_recs = ProductService.filter_valid_products(unique_recs)
            
            # Fallback if we filtered out too many
            if len(valid_recs) < 4:
                logger.warning(f"[Auto-Recommend] Too few valid recommendations ({len(valid_recs)}), fetching trending.")
                trending = ProductService.get_trending_products(12)
                for t in trending:
                    if t['id'] not in [v['id'] for v in valid_recs]:
                        valid_recs.append(t)
            
            return valid_recs[:12]
            
        except Exception as e:
            print(f"Error in auto recommendations: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()

    @staticmethod
    def get_related_products(product_id, limit=6):
        """
        Get related products using ML cosine similarity + category fallback.
        
        ENHANCED LOGIC:
        1. First, try TF-IDF cosine similarity to find truly similar products
           (e.g., "Nike Hiking Boots" → "Adidas Hiking Boots", not just any Nike product)
        2. If ML is unavailable or returns too few results, fall back to 
           same-category products sorted by rating (original behavior)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # ── Try ML-based related products first ──
            if _ML_AVAILABLE:
                try:
                    recommender = get_recommender()
                    similar = recommender.get_similar_products(product_id, top_n=limit)
                    
                    if similar and len(similar) >= limit:
                        # Fetch full product details for the similar product IDs
                        similar_ids = [pid for pid, score in similar]
                        placeholders = ','.join(['%s'] * len(similar_ids))
                        cursor.execute(f"""
                            SELECT id, name, price, rating, image_url, brand, category
                            FROM products
                            WHERE id IN ({placeholders})
                        """, similar_ids)
                        
                        products = cursor.fetchall()
                        
                        # Re-sort by the ML similarity order (not DB order)
                        id_to_product = {p['id']: p for p in products}
                        sorted_products = [id_to_product[pid] for pid in similar_ids if pid in id_to_product]
                        
                        if sorted_products:
                            valid_sorted = ProductService.filter_valid_products(sorted_products)
                            if len(valid_sorted) >= 3:
                                logger.info(f"[Related] Source: ML Hybrid, Count: {len(valid_sorted)} for product {product_id}")
                                return valid_sorted[:limit]
                
                except Exception as ml_error:
                    print(f"[ML Related] ML fallback for product {product_id}: {ml_error}")
            
            # ── Fallback: same-category products sorted by rating (original logic) ──
            logger.info(f"[Related] Stage 1 (ML) failed/insufficient. Falling back to same-category for product {product_id}")
            cursor.execute("SELECT category FROM products WHERE id = %s", (product_id,))
            row = cursor.fetchone()
            if not row:
                return []
            
            cursor.execute("""
                SELECT id, name, price, rating, image_url, brand, category
                FROM products
                WHERE category = %s AND id != %s
                ORDER BY rating DESC
                LIMIT %s
            """, (row['category'], product_id, limit * 2))
            
            fallback_prods = ProductService.filter_valid_products(cursor.fetchall())
            if fallback_prods:
                logger.info(f"[Related] Source: Category Fallback, Count: {len(fallback_prods)} for product {product_id}")
                return fallback_prods[:limit]
            
            logger.info(f"[Related] Category Fallback empty. Returning trending.")
            return ProductService.get_trending_products(limit)
        except Exception as e:
            print(f"Error fetching related products: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn is not None and conn.is_connected():
                conn.close()
