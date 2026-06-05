import os
import csv
import json
import random
import time
import requests
import re
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'datasets')
os.makedirs(DATA_DIR, exist_ok=True)
PRODUCTS_CSV = os.path.join(DATA_DIR, 'products.csv')
INTERACTIONS_CSV = os.path.join(DATA_DIR, 'interactions.csv')

FRONTEND_PUBLIC_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'public')
IMAGES_DIR = os.path.join(FRONTEND_PUBLIC_DIR, 'images', 'products')
os.makedirs(IMAGES_DIR, exist_ok=True)

# Map DummyJSON categories to our Premium Ecommerce Categories
CATEGORY_MAPPING = {
    'smartphones': 'Electronics',
    'laptops': 'Electronics',
    'tablets': 'Electronics',
    'mens-shoes': 'Shoes',
    'womens-shoes': 'Shoes',
    'mens-watches': 'Watches',
    'womens-watches': 'Watches',
    'sunglasses': 'Accessories',
    'womens-jewellery': 'Accessories',
    'womens-bags': 'Bags',
    'sports-accessories': 'Fitness',
    'mobile-accessories': 'Headphones'
}

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def download_and_validate_image(url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Try opening with PIL to validate
        img = Image.open(BytesIO(response.content))
        img.verify()
        
        # Re-open for resizing/converting
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB (in case of RGBA/P)
        if img.mode in ('RGBA', 'P', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
            
        # Resize if too large to save space (max 800x800)
        img.thumbnail((800, 800))
        img.save(save_path, "JPEG", quality=85)
        return True
    except Exception as e:
        print(f"  Failed to download/validate {url}: {e}")
        return False

def get_price_range(price):
    if price < 50: return 'budget'
    if price < 150: return 'mid-range'
    if price < 500: return 'premium'
    return 'luxury'

def main():
    print("--- Phase 1: Generating Realistic Dataset via DummyJSON ---")
    
    products = []
    pid = 1
    used_names = set()
    
    # Fetch all dummyjson products
    try:
        res = requests.get('https://dummyjson.com/products?limit=200')
        res.raise_for_status()
        all_dummy_products = res.json().get('products', [])
    except Exception as e:
        print(f"Failed to fetch from DummyJSON: {e}")
        return

    for dp in all_dummy_products:
        dummy_cat = dp.get('category')
        if dummy_cat not in CATEGORY_MAPPING:
            continue
            
        target_cat = CATEGORY_MAPPING[dummy_cat]
        name = dp.get('title', '').strip()
        brand = dp.get('brand') or name.split()[0]
        
        # Deduplicate
        if name in used_names:
            continue
        used_names.add(name)
        
        print(f"Processing: {name} ({target_cat})")
        
        # Pick best image (prefer images[0] over thumbnail if available for higher res)
        images = dp.get('images', [])
        image_url = images[0] if images else dp.get('thumbnail')
        
        if not image_url:
            print(f"  WARNING: No image found for {name}. Skipping.")
            continue
            
        local_filename = f"{slugify(name)}.jpg"
        local_filepath = os.path.join(IMAGES_DIR, local_filename)
        
        img_saved = False
        if os.path.exists(local_filepath) and os.path.getsize(local_filepath) > 0:
            print(f"  Image already exists locally: {local_filename}")
            img_saved = True
        else:
            print(f"  Downloading: {image_url}")
            img_saved = download_and_validate_image(image_url, local_filepath)
            
        if not img_saved:
            print(f"  WARNING: Skipping {name} due to image download failure.")
            continue
            
        price = float(dp.get('price', 99.99))
        rating = float(dp.get('rating', 4.5))
        review_count = dp.get('reviews')
        if review_count and isinstance(review_count, list):
            review_count = len(review_count) * random.randint(10, 50)
        else:
            review_count = random.randint(50, 1500)
            
        # Extract color if present in name, else default
        color = "Standard"
        for c in ["Black", "White", "Red", "Blue", "Green", "Silver", "Gold", "Grey", "Brown"]:
            if c.lower() in name.lower():
                color = c
                break
                
        tags = dp.get('tags', [])
        tags.extend([target_cat.lower(), brand.lower()])
        tags_str = ",".join(set(tags))
        
        products.append({
            'id': pid,
            'name': name,
            'category': target_cat,
            'brand': brand,
            'color': color,
            'price': price,
            'rating': rating,
            'review_count': review_count,
            'image_url': f"/images/products/{local_filename}",
            'description': dp.get('description', f"Premium {target_cat} product."),
            'tags': tags_str,
            'features': "Premium build,Official warranty",
            'price_range': get_price_range(price),
            'amazon_url': "",
            'flipkart_url': "",
            'myntra_url': ""
        })
        
        pid += 1

    print(f"\nGenerated {len(products)} validated products with local images.")
    
    if products:
        with open(PRODUCTS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(products[0].keys()))
            writer.writeheader()
            writer.writerows(products)
        print(f"Saved {PRODUCTS_CSV}")
        
    # Generate interactions.csv
    print("Generating cohesive interactions...")
    interactions = []
    now = datetime.now()
    
    related_map = {
        "Shoes": ["Shoes", "Fitness", "Bags"],
        "Watches": ["Watches", "Accessories", "Bags"],
        "Electronics": ["Electronics", "Headphones", "Bags"],
        "Headphones": ["Headphones", "Electronics"],
        "Fitness": ["Fitness", "Shoes", "Bags"],
        "Bags": ["Bags", "Shoes", "Watches"],
        "Accessories": ["Accessories", "Watches", "Bags"]
    }
    
    category_products = {}
    for p in products:
        category_products.setdefault(p['category'], []).append(p['id'])
        
    for user_id in range(1, 101):
        if not category_products:
            break
            
        primary_category = random.choice(list(category_products.keys()))
        pool_categories = [primary_category]
        if primary_category in related_map:
            pool_categories.extend(related_map[primary_category])
            
        user_pool = []
        for cat in pool_categories:
            if cat in category_products:
                user_pool.extend(category_products[cat])
                
        if not user_pool:
            user_pool = [p['id'] for p in products]
            
        num_interactions = random.randint(5, 30)
        for _ in range(num_interactions):
            prod_id = random.choice(user_pool)
            timestamp = now - timedelta(days=random.randint(1, 90), hours=random.randint(0, 23))
            
            action_roll = random.random()
            if action_roll < 0.6: action = 'click'
            elif action_roll < 0.85: action = 'view'
            elif action_roll < 0.95: action = 'purchase'
            else: action = 'rating'
            
            interactions.append({
                'user_id': user_id,
                'product_id': prod_id,
                'action': action,
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'rating': round(random.uniform(4.0, 5.0), 1) if action == 'rating' else "",
                'purchase': 1 if action == 'purchase' else 0
            })
            
    if interactions:
        with open(INTERACTIONS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['user_id', 'product_id', 'action', 'rating', 'purchase', 'timestamp'])
            writer.writeheader()
            writer.writerows(interactions)
        print(f"Saved {INTERACTIONS_CSV} ({len(interactions)} records)")

if __name__ == "__main__":
    main()
