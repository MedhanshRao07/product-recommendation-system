from ..database.db_connection import get_connection as get_db_connection
import logging
import math
from collections import defaultdict

logger = logging.getLogger('suggestify.product_service')

# Phase 3: Lightweight Recommendation Engine
# Removed heavy ML dependencies (scikit-learn) in favor of optimized hybrid scoring
_ML_AVAILABLE = False

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
        Highly Adaptive Recommendation Engine:
        Strictly limits unrelated products to 1-2 items maximum.
        Forces homepage to heavily shift toward the dominant category.
        Uses action weights (view=1, wishlist=3, add_to_cart=5, purchase=10) and time decay.
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # 1. Fetch user's recent history with actions to understand context
            cursor.execute("""
                SELECT p.id, p.category, p.brand, p.name, p.price, ua.action, ua.created_at
                FROM user_activity ua
                JOIN products p ON ua.product_id = p.id
                WHERE ua.user_id = %s
                ORDER BY ua.created_at DESC
                LIMIT 50
            """, (user_id,))
            history = cursor.fetchall()
            
            history_ids = set(row['id'] for row in history)
            latest_viewed = history[0] if history else None
            
            # 2. Action weights & Time Decay
            action_weights = {
                'view': 1,
                'click': 1,
                'wishlist': 3,
                'add_to_cart': 5,
                'cart': 5,
                'purchase': 10
            }
            
            category_scores = defaultdict(float)
            brand_scores = defaultdict(float)
            
            for idx, item in enumerate(history):
                # Strong time decay: last 15 items matter massively
                decay = max(0.1, 1.0 - (idx / 15.0))
                action_w = action_weights.get(item['action'], 1)
                weight = decay * action_w
                
                category_scores[item['category']] += weight
                brand_scores[item['brand']] += weight
                
            # 3. Dominant Category Detection
            dominant_category = None
            if category_scores:
                dominant_category = max(category_scores.items(), key=lambda x: x[1])[0]
                
            # 4. Collaborative Filtering Candidates
            candidates = []
            if history_ids:
                placeholders = ','.join(['%s'] * len(history_ids))
                cursor.execute(f"""
                    SELECT p.id, p.category, p.brand, p.name, p.rating, p.price, COUNT(*) as collab_weight
                    FROM user_activity ua
                    JOIN products p ON ua.product_id = p.id
                    WHERE ua.user_id IN (
                        SELECT DISTINCT user_id FROM user_activity WHERE product_id IN ({placeholders}) AND user_id != %s
                    )
                    AND p.id NOT IN ({placeholders})
                    GROUP BY p.id
                    ORDER BY collab_weight DESC
                    LIMIT 300
                """, (*list(history_ids), user_id, *list(history_ids)))
                candidates = cursor.fetchall()
            
            if not candidates:
                cursor.execute("SELECT id, category, brand, name, rating, price, image_url FROM products ORDER BY rating DESC LIMIT 100")
                candidates = cursor.fetchall()
                # Cold start: if no history, forcefully categorize the candidates to create sections
                if not history_ids:
                    for i, c in enumerate(candidates[:12]):
                        if i < 4:
                            c['recommendation_reason'] = "Trending Now"
                            c['base_score'] = 1.0 - (i * 0.01)
                        elif i < 8:
                            c['recommendation_reason'] = f"Popular in {c['category']}"
                            c['base_score'] = 0.8 - (i * 0.01)
                        else:
                            c['recommendation_reason'] = "Staff Picks"
                            c['base_score'] = 0.6 - (i * 0.01)
                    return candidates[:12]
                
            max_collab = max((c.get('collab_weight', 0) for c in candidates), default=1) or 1
            max_rating = max((c.get('rating', 0) or 0 for c in candidates), default=5.0) or 5.0
            
            related_map = {
                'Electronics': ['Headphones', 'Accessories', 'Watches'],
                'Headphones': ['Electronics', 'Accessories'],
                'Fitness': ['Shoes', 'Accessories'],
                'Shoes': ['Fitness', 'Bags'],
                'Watches': ['Accessories', 'Bags', 'Electronics'],
                'Bags': ['Watches', 'Accessories', 'Shoes'],
                'Accessories': ['Watches', 'Bags', 'Electronics']
            }
            
            dominant_pool = []
            related_pool = []
            unrelated_pool = []
            
            for c in candidates:
                # Base scoring
                collab_score = c.get('collab_weight', 0) / max_collab
                max_brand = max(brand_scores.values()) if brand_scores else 1
                brand_score = brand_scores.get(c['brand'], 0) / (max_brand or 1)
                popularity = (c.get('rating', 0) or 0) / max_rating
                
                final_score = (0.40 * collab_score) + (0.30 * brand_score) + (0.30 * popularity)
                c['base_score'] = final_score
                
                # Assign to pools and generate strict labels
                if dominant_category and c['category'] == dominant_category:
                    if float(c['price'] or 0) > 400:
                        c['recommendation_reason'] = f"Premium {dominant_category}"
                    else:
                        c['recommendation_reason'] = f"Because you explored {dominant_category}"
                    dominant_pool.append(c)
                elif dominant_category and c['category'] in related_map.get(dominant_category, []):
                    c['recommendation_reason'] = f"Trending in {c['category']}"
                    related_pool.append(c)
                else:
                    c['recommendation_reason'] = "Popular choice"
                    unrelated_pool.append(c)
                    
            # Sort each pool by base quality
            dominant_pool.sort(key=lambda x: x['base_score'], reverse=True)
            related_pool.sort(key=lambda x: x['base_score'], reverse=True)
            unrelated_pool.sort(key=lambda x: x['base_score'], reverse=True)
            
            # 5. Controlled Diversity & Strict Limiting
            final_selection = []
            if dominant_category:
                # Enforce: 8 dominant, 3 related, 1 unrelated (Max 12)
                dom_count = min(len(dominant_pool), 8)
                rel_count = min(len(related_pool), 3)
                unrel_count = min(len(unrelated_pool), 1)
                
                # If short on dominant, pad with related
                if dom_count < 8:
                    rel_count = min(len(related_pool), 3 + (8 - dom_count))
                    
                final_selection.extend(dominant_pool[:dom_count])
                final_selection.extend(related_pool[:rel_count])
                final_selection.extend(unrelated_pool[:unrel_count])
            else:
                final_selection = sorted(candidates, key=lambda x: x['base_score'], reverse=True)[:12]
                
            top_ids = [c['id'] for c in final_selection[:12]]
            
            if not top_ids:
                return []
                
            # 6. Fetch final full details and retain sorted order
            placeholders = ','.join(['%s'] * len(top_ids))
            cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", top_ids)
            final_products = ProductService.filter_valid_products(cursor.fetchall())
            
            ordered_products = []
            for sc in final_selection:
                for fp in final_products:
                    if fp['id'] == sc['id']:
                        fp['recommendation_reason'] = sc['recommendation_reason']
                        ordered_products.append(fp)
                        break
                        
            return ordered_products
            
        except Exception as e:
            logger.error(f"Error in auto recommendations: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def get_related_products(product_id, limit=6):
        """
        Lightweight related products using strict category affinity.
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT category, brand FROM products WHERE id = %s", (product_id,))
            row = cursor.fetchone()
            if not row:
                return []
                
            cat = row['category']
            brand = row['brand']
            
            # Related category relationships
            related_map = {
                'Electronics': ['Headphones', 'Accessories', 'Watches'],
                'Headphones': ['Electronics', 'Accessories'],
                'Fitness': ['Shoes', 'Accessories'],
                'Shoes': ['Fitness', 'Bags'],
                'Watches': ['Accessories', 'Bags', 'Electronics'],
                'Bags': ['Watches', 'Accessories', 'Shoes'],
                'Accessories': ['Watches', 'Bags', 'Electronics']
            }
            related_cats = related_map.get(cat, [])
            
            # Get candidates
            cursor.execute("""
                SELECT id, name, price, rating, image_url, brand, category
                FROM products
                WHERE id != %s AND (category = %s OR category IN (%s))
                ORDER BY rating DESC
                LIMIT 50
            """ % ("%s", "%s", ','.join(['%s']*len(related_cats)) if related_cats else "''"), 
            (product_id, cat, *related_cats))
            
            candidates = cursor.fetchall()
            
            for c in candidates:
                # Same brand bonus
                score = 0
                if c['category'] == cat: score += 5
                elif c['category'] in related_cats: score += 2
                if c['brand'] == brand: score += 3
                score += (c.get('rating', 0) or 0) / 5.0
                c['sim_score'] = score
                c['recommendation_reason'] = "Similar product"
                
            candidates.sort(key=lambda x: x['sim_score'], reverse=True)
            return ProductService.filter_valid_products(candidates)[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching related products: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()
