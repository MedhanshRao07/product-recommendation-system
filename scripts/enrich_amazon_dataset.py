import os
import csv
import json
import random
import time
import requests
import re
from io import BytesIO
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'datasets')
PRODUCTS_CSV = os.path.join(DATA_DIR, 'products.csv')
AMAZON_CSV = os.path.join(DATA_DIR, 'amazon_sales', 'amazon.csv')

FRONTEND_PUBLIC_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'public')
IMAGES_DIR = os.path.join(FRONTEND_PUBLIC_DIR, 'images', 'products')
os.makedirs(IMAGES_DIR, exist_ok=True)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def clean_amazon_name(raw_name):
    """
    Amazon titles are often huge like:
    'boAt Airdopes 141 Bluetooth Truly Wireless in Ear Earbuds with 42H Playtime, Beast Mode...'
    We truncate at the first comma, pipe, or parenthesis.
    """
    name = raw_name.split('|')[0].split(',')[0].split('(')[0].split('-')[0]
    name = ' '.join(name.split()[:8]) # Max 8 words
    return name.strip()

def parse_inr_price(price_str):
    """ Converts ₹1,999.00 to approx USD float """
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        inr = float(cleaned)
        usd = inr / 82.0  # Approx conversion
        return max(4.99, round(usd, 2)) # Ensure reasonable minimum
    except ValueError:
        return 29.99

def map_category(amazon_category_str):
    cat_lower = amazon_category_str.lower()
    if 'headphones' in cat_lower or 'earbuds' in cat_lower or 'headsets' in cat_lower:
        return 'Headphones'
    if 'computers' in cat_lower or 'electronics' in cat_lower or 'smartphones' in cat_lower or 'tablets' in cat_lower:
        return 'Electronics'
    if 'shoes' in cat_lower or 'footwear' in cat_lower:
        return 'Shoes'
    if 'watches' in cat_lower:
        return 'Watches'
    if 'bags' in cat_lower or 'luggage' in cat_lower or 'backpacks' in cat_lower:
        return 'Bags'
    if 'sports' in cat_lower or 'fitness' in cat_lower or 'outdoors' in cat_lower:
        return 'Fitness'
    if 'accessories' in cat_lower or 'jewelry' in cat_lower:
        return 'Accessories'
    # Fallback to Home if we want, but user wants strict categories.
    return None

def download_and_validate_image(url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img.verify()
        
        img = Image.open(BytesIO(response.content))
        if img.mode in ('RGBA', 'P', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
            
        img.thumbnail((800, 800))
        img.save(save_path, "JPEG", quality=85)
        return True
    except Exception as e:
        print(f"  Failed to download/validate image: {e}")
        return False

def get_price_range(price):
    if price < 50: return 'budget'
    if price < 150: return 'mid-range'
    if price < 500: return 'premium'
    return 'luxury'

def main():
    print("--- Phase 2: Enriching Dataset via Amazon Sales Data ---")
    
    # 1. Load existing products
    existing_products = []
    used_names = set()
    max_id = 0
    
    if os.path.exists(PRODUCTS_CSV):
        with open(PRODUCTS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_products.append(row)
                used_names.add(row['name'].lower())
                max_id = max(max_id, int(row['id']))
                
    print(f"Loaded {len(existing_products)} existing products from Phase 1.")
    
    # 2. Parse Amazon data
    target_new_items = 212 # To reach ~300 total
    new_products = []
    pid = max_id + 1
    
    try:
        with open(AMAZON_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if len(new_products) >= target_new_items:
                    break
                    
                amazon_cat = row.get('category', '')
                mapped_cat = map_category(amazon_cat)
                
                if not mapped_cat:
                    continue # Skip unrelated categories (e.g. Home & Kitchen, Toys)
                    
                raw_name = row.get('product_name', '')
                clean_name = clean_amazon_name(raw_name)
                
                # Brand is usually first word of the raw name in this dataset
                brand = clean_name.split()[0] if clean_name else "Unknown"
                if len(brand) < 2:
                    brand = "AmazonBasics"
                
                # Deduplication
                if clean_name.lower() in used_names or len(clean_name) < 5:
                    continue
                
                # Image
                img_links = row.get('img_link', '')
                first_img = img_links.split('|')[0] if img_links else None
                if not first_img or not first_img.startswith('http'):
                    continue
                    
                print(f"Processing: {clean_name} ({mapped_cat})")
                
                local_filename = f"{slugify(clean_name)}.jpg"
                local_filepath = os.path.join(IMAGES_DIR, local_filename)
                
                img_saved = False
                if os.path.exists(local_filepath) and os.path.getsize(local_filepath) > 0:
                    print(f"  Image already exists locally: {local_filename}")
                    img_saved = True
                else:
                    img_saved = download_and_validate_image(first_img, local_filepath)
                    
                if not img_saved:
                    continue
                    
                used_names.add(clean_name.lower())
                
                # Metadata
                price = parse_inr_price(row.get('discounted_price', '0'))
                rating_raw = row.get('rating', '4.0')
                try:
                    rating = float(rating_raw)
                except:
                    rating = 4.0
                    
                review_count_raw = row.get('rating_count', '0')
                review_count = int(re.sub(r'[^\d]', '', review_count_raw)) if review_count_raw else random.randint(100, 5000)
                
                description = row.get('about_product', '').split('|')[0]
                if len(description) > 300:
                    description = description[:297] + "..."
                    
                tags = [mapped_cat.lower(), brand.lower()]
                if 'wireless' in raw_name.lower(): tags.append('wireless')
                if 'smart' in raw_name.lower(): tags.append('smart')
                
                new_products.append({
                    'id': pid,
                    'name': clean_name,
                    'category': mapped_cat,
                    'brand': brand,
                    'color': "Standard",
                    'price': price,
                    'rating': rating,
                    'review_count': review_count,
                    'image_url': f"/images/products/{local_filename}",
                    'description': description if description else f"Premium {mapped_cat} product.",
                    'tags': ",".join(set(tags)),
                    'features': "Verified Purchase,Premium build",
                    'price_range': get_price_range(price),
                    'amazon_url': row.get('product_link', ''),
                    'flipkart_url': "",
                    'myntra_url': ""
                })
                
                pid += 1
                
    except Exception as e:
        print(f"Error reading {AMAZON_CSV}: {e}")
        return

    print(f"\nSuccessfully processed {len(new_products)} new products from Amazon dataset.")
    
    # Append and save
    all_products = existing_products + new_products
    
    if all_products:
        with open(PRODUCTS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(all_products[0].keys()))
            writer.writeheader()
            writer.writerows(all_products)
        print(f"Saved {PRODUCTS_CSV} with {len(all_products)} total products.")

if __name__ == "__main__":
    main()
