import os
import csv
import zipfile
import io
import re
import random
import math
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# ---- Configuration ----
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'datasets')
AMAZON_SALES_CSV = os.path.join(DATA_DIR, 'amazon_sales', 'amazon.csv')
AMAZON_2023_ZIP = os.path.join(PROJECT_ROOT, 'archive (4).zip')

PRODUCTS_CSV = os.path.join(DATA_DIR, 'products.csv')
INTERACTIONS_CSV = os.path.join(DATA_DIR, 'interactions.csv')

load_dotenv(os.path.join(PROJECT_ROOT, 'backend', '.env'))
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'suggestify_db'),
}

USD_INR_RATE = 83.0

# Files to extract from the 2023 archive and their target categories
ARCHIVE_MAPPINGS = {
    'All Electronics.csv': 'Electronics',
    'Headphones.csv': 'Headphones',
    'Cameras.csv': 'Electronics',
    'Watches.csv': 'Watches',
    'Shoes.csv': 'Shoes',
    'Sports Shoes.csv': 'Shoes',
    'Backpacks.csv': 'Bags',
    'Bags and Luggage.csv': 'Bags',
    'Fitness Accessories.csv': 'Fitness',
    'Sunglasses.csv': 'Accessories',
    'All Home and Kitchen.csv': 'Home & Kitchen',
}

def clean_price(price_str):
    if not price_str: return 0.0
    s = str(price_str).replace('₹', '').replace(',', '').strip()
    try:
        return float(s)
    except:
        return 0.0

def get_price_range(price_usd):
    if price_usd < 25: return 'budget'
    elif price_usd < 100: return 'mid-range'
    elif price_usd < 500: return 'premium'
    return 'luxury'

def extract_asin(link):
    if not link: return None
    match = re.search(r'/([A-Z0-9]{10})(?:/|\?|$)', link)
    if match: return match.group(1)
    return None

def extract_brand(name):
    if not name: return "Generic"
    # Try to grab the first word or two, avoiding common generic terms
    words = name.split()
    if not words: return "Generic"
    if words[0].lower() in ["amazon", "amazonbasics"]: return "AmazonBasics"
    if words[0].lower() in ["apple"]: return "Apple"
    if words[0].lower() in ["samsung"]: return "Samsung"
    if words[0].lower() in ["sony"]: return "Sony"
    if words[0].lower() in ["nike"]: return "Nike"
    
    # Just return first alphanumeric block
    brand = re.sub(r'[^a-zA-Z0-9]', '', words[0])
    if len(brand) > 1: return brand.capitalize()
    return "Generic"

def generate_tags(category, name):
    tags = {category.lower()}
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', name)]
    # Take a few descriptive words
    for w in words[:5]:
        if w not in ["with", "for", "and", "the"]:
            tags.add(w)
    return ",".join(list(tags)[:6])

def main():
    print("--- Starting Amazon Data Seeding ---")
    
    # 1. Parse amazon_sales/amazon.csv for metadata and user profiles
    sales_metadata = {}
    users_pool = set() # Store unique user ids (strings)
    
    try:
        with open(AMAZON_SALES_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                asin = row['product_id']
                sales_metadata[asin] = row
                
                # Extract users
                uids = row.get('user_id', '').split(',')
                unames = row.get('user_name', '').split(',')
                for uid, uname in zip(uids, unames):
                    uid = uid.strip()
                    uname = uname.strip()
                    if uid and len(uid) > 10:
                        users_pool.add(uid)
    except Exception as e:
        print(f"Error reading amazon_sales: {e}")
        return

    users_list = list(users_pool)
    print(f"Loaded {len(sales_metadata)} products and {len(users_list)} unique users from sales metadata.")

    # 2. Extract products from Amazon 2023 zip
    products = []
    seen_asins = set()
    
    try:
        with zipfile.ZipFile(AMAZON_2023_ZIP) as z:
            for fname, target_cat in ARCHIVE_MAPPINGS.items():
                print(f"Processing {fname} -> {target_cat}")
                try:
                    with z.open(fname) as f:
                        reader = csv.DictReader(io.TextIOWrapper(f, 'utf-8', errors='ignore'))
                        file_products = 0
                        for row in reader:
                            asin = extract_asin(row.get('link'))
                            if not asin or asin in seen_asins:
                                continue
                                
                            name = row.get('name', '')
                            if not name or len(name) < 10: continue
                            
                            img_url = row.get('image', '')
                            if not img_url.startswith('http'): continue
                            
                            price_inr = clean_price(row.get('discount_price', ''))
                            if price_inr < 100: # Skip very cheap/invalid items
                                price_inr = clean_price(row.get('actual_price', ''))
                            if price_inr < 100: continue
                                
                            price_usd = round(price_inr / USD_INR_RATE, 2)
                            
                            rating_str = str(row.get('ratings', '0')).replace(',', '.')
                            try:
                                rating = float(re.findall(r"[-+]?\d*\.\d+|\d+", rating_str)[0])
                            except:
                                rating = 0.0
                                
                            try:
                                review_count = int(str(row.get('no_of_ratings', '0')).replace(',', ''))
                            except:
                                review_count = 0
                                
                            # Basic quality filter
                            if rating < 3.0 or review_count < 10:
                                continue
                                
                            description = name
                            if asin in sales_metadata:
                                description = sales_metadata[asin].get('about_product', name)
                                
                            brand = extract_brand(name)
                            tags = generate_tags(target_cat, name)
                            
                            p = {
                                'id': len(products) + 1, # sequential 1-indexed
                                'asin': asin,
                                'name': name[:250],
                                'category': target_cat,
                                'brand': brand[:95],
                                'color': 'Standard',
                                'price': price_usd,
                                'rating': rating,
                                'review_count': review_count,
                                'image_url': img_url,
                                'description': description,
                                'tags': tags,
                                'features': "Premium build, Official warranty",
                                'price_range': get_price_range(price_usd),
                                'amazon_url': row.get('link', ''),
                                'flipkart_url': '',
                                'myntra_url': ''
                            }
                            
                            products.append(p)
                            seen_asins.add(asin)
                            file_products += 1
                            
                            # Cap per file to avoid making the DB too huge (e.g. max 1000 per category)
                            if file_products >= 800:
                                break
                except Exception as e:
                    print(f"Error reading {fname}: {e}")
    except Exception as e:
        print(f"Error reading zip: {e}")
        return

    print(f"\nExtracted {len(products)} products total.")

    # 3. Write to products.csv
    print(f"Writing {PRODUCTS_CSV}...")
    fieldnames = ['id','name','category','brand','color','price','rating','review_count',
                  'image_url','description','tags','features','price_range',
                  'amazon_url','flipkart_url','myntra_url']
    with open(PRODUCTS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in products:
            p_copy = p.copy()
            del p_copy['asin']
            writer.writerow(p_copy)

    # 4. Generate interactions.csv
    print(f"Generating interactions...")
    interactions = []
    
    # We map the string users to integer IDs
    user_int_map = {uid: i+1 for i, uid in enumerate(users_list)}
    num_users = len(user_int_map)
    if num_users == 0:
        # Fallback if parsing failed
        num_users = 200
        user_int_map = {f"u{i}": i for i in range(1, num_users+1)}

    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    # Generate based on popularity
    for p in products:
        # Number of interactions scales with log of reviews, bounded
        base_interactions = min(50, max(2, int(math.log10(p['review_count'] + 1) * 5)))
        
        for _ in range(base_interactions):
            uid = random.randint(1, num_users)
            
            # Action distribution
            r = random.random()
            if r < 0.60: action = 'view'
            elif r < 0.85: action = 'wishlist'
            elif r < 0.95: action = 'add_to_cart'
            else: action = 'purchase'
            
            ts = start_date + timedelta(seconds=random.randint(0, 90*24*60*60))
            
            interactions.append({
                'user_id': uid,
                'product_id': p['id'],
                'action': action,
                'rating': p['rating'] if action == 'purchase' else '',
                'purchase': 1 if action == 'purchase' else 0,
                'timestamp': ts.strftime('%Y-%m-%d %H:%M:%S')
            })

    interactions.sort(key=lambda x: x['timestamp'])

    print(f"Writing {INTERACTIONS_CSV} ({len(interactions)} records)...")
    with open(INTERACTIONS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['user_id','product_id','action','rating','purchase','timestamp'])
        writer.writeheader()
        writer.writerows(interactions)


    # 5. Seed Database
    print(f"\n--- Seeding Database ---")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if not conn.is_connected():
            print("Failed to connect to MySQL")
            return
            
        cursor = conn.cursor()
        
        # Products table
        print("Recreating products table...")
        cursor.execute('DROP TABLE IF EXISTS user_activity')
        cursor.execute('DROP TABLE IF EXISTS interactions')
        cursor.execute('DROP TABLE IF EXISTS products')

        cursor.execute("""
            CREATE TABLE products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name TEXT NOT NULL,
                category VARCHAR(100) NOT NULL,
                brand VARCHAR(100),
                price FLOAT NOT NULL,
                rating FLOAT DEFAULT 0,
                review_count INT DEFAULT 0,
                color VARCHAR(50),
                image_url TEXT,
                description TEXT,
                tags VARCHAR(500),
                features TEXT,
                amazon_url TEXT,
                flipkart_url TEXT,
                myntra_url TEXT,
                price_range VARCHAR(20),
                INDEX idx_category (category(100)),
                INDEX idx_brand (brand(100)),
                INDEX idx_rating (rating)
            )
        """)
        
        # Insert products
        print(f"Inserting {len(products)} products...")
        insert_sql = """
            INSERT INTO products (id, name, category, brand, price, rating, review_count, color, image_url, description, tags, features, amazon_url, flipkart_url, myntra_url, price_range)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        batch = []
        for p in products:
            batch.append((
                p['id'], p['name'], p['category'], p['brand'], p['price'], p['rating'], 
                p['review_count'], p['color'], p['image_url'], p['description'], 
                p['tags'], p['features'], p['amazon_url'], p['flipkart_url'], 
                p['myntra_url'], p['price_range']
            ))
            
        cursor.executemany(insert_sql, batch)
        conn.commit()

        # User Activity table
        print("Recreating user_activity table...")
        cursor.execute("""
            CREATE TABLE user_activity (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                action VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_user_id (user_id),
                INDEX idx_product_id (product_id),
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)
        
        print(f"Inserting {len(interactions)} interactions...")
        insert_act_sql = """
            INSERT INTO user_activity (user_id, product_id, action, created_at)
            VALUES (%s, %s, %s, %s)
        """
        batch_act = []
        for i in interactions:
            batch_act.append((i['user_id'], i['product_id'], i['action'], i['timestamp']))
            
        # Execute in chunks
        chunk_size = 5000
        for i in range(0, len(batch_act), chunk_size):
            cursor.executemany(insert_act_sql, batch_act[i:i+chunk_size])
        conn.commit()
        
        print("Database seeded successfully!")
        
    except Error as e:
        print(f"MySQL Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

if __name__ == "__main__":
    main()
