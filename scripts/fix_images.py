import mysql.connector
import os
from collections import defaultdict
import random

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mr_0706',
    'database': 'suggestify_db'
}

def get_images_by_category():
    images_dir = os.path.join('frontend', 'public', 'images', 'products')
    all_images = os.listdir(images_dir)
    
    cat_images = defaultdict(list)
    
    for img in all_images:
        img_lower = img.lower()
        if 'tv' in img_lower or 'remote' in img_lower or 'usb' in img_lower or 'cable' in img_lower or 'charger' in img_lower or 'laptop' in img_lower or 'macbook' in img_lower or 'monitor' in img_lower or 'power' in img_lower or 'earphone' in img_lower or 'headphone' in img_lower or 'airpod' in img_lower or 'mouse' in img_lower or 'keyboard' in img_lower or 'speaker' in img_lower or 'iphone' in img_lower or 'samsung' in img_lower or 'nokia' in img_lower or 'vivo' in img_lower or 'oppo' in img_lower or 'realme' in img_lower or 'redmi' in img_lower or 'oneplus' in img_lower:
            cat_images['Electronics'].append(img)
        elif 'airfryer' in img_lower or 'coffee' in img_lower or 'kettle' in img_lower or 'purifier' in img_lower or 'cookware' in img_lower or 'spice' in img_lower:
            cat_images['Home Appliances'].append(img)
        elif 'shirt' in img_lower or 'polo' in img_lower or 'sweater' in img_lower or 'glass' in img_lower or 'earring' in img_lower or 'ring' in img_lower or 'model' in img_lower:
            cat_images['Fashion'].append(img)
        elif 'wallet' in img_lower or 'belt' in img_lower or 'watch' in img_lower or 'band' in img_lower or 'rolex' in img_lower or 'casio' in img_lower:
            cat_images['Accessories'].append(img)
        elif 'foamroller' in img_lower or 'bottle' in img_lower or 'yoga' in img_lower or 'gym' in img_lower:
            cat_images['Fitness'].append(img)
        elif 'football' in img_lower or 'basketball' in img_lower or 'baseball' in img_lower or 'cricket' in img_lower or 'tennis' in img_lower or 'golf' in img_lower or 'shuttlecock' in img_lower or 'volleyball' in img_lower:
            cat_images['Sports'].append(img)
        elif 'shoe' in img_lower or 'nike' in img_lower or 'adidas' in img_lower or 'puma' in img_lower or 'boot' in img_lower or 'sneaker' in img_lower or 'slipper' in img_lower or 'trainers' in img_lower or 'new_balance' in img_lower:
            cat_images['Shoes'].append(img)
        elif 'bag' in img_lower or 'backpack' in img_lower or 'handbag' in img_lower or 'messenger' in img_lower:
            cat_images['Bags'].append(img)
        else:
            cat_images['Other'].append(img)
            
    # Fallbacks if a category is empty
    if not cat_images['Gaming']:
        cat_images['Gaming'] = [img for img in all_images if 'mouse' in img.lower() or 'keyboard' in img.lower()] or ['keyboard1.png']
    if not cat_images['Fashion']:
        cat_images['Fashion'] = ['shirt1.png', 'polo.png', 'patagonia_sweater.png']
        
    return cat_images

def fix_images():
    print("Connecting to DB...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    cat_images = get_images_by_category()
    
    # Shuffle lists to ensure variety when we pop/cycle
    for k in cat_images:
        random.shuffle(cat_images[k])
        print(f"Category {k} has {len(cat_images[k])} images")
        
    cursor.execute("SELECT id, name, category, subcategory FROM products")
    products = cursor.fetchall()
    
    # Track usage to minimize duplication
    usage_counts = defaultdict(int)
    
    updates = []
    
    for p in products:
        cat = p['category']
        subcat = p['subcategory']
        name = p['name'].lower()
        
        # Try to find a specific keyword match first
        chosen_img = None
        pool = cat_images.get(cat, [])
        if not pool:
            pool = cat_images.get('Other', [])
            
        # Select image with minimum usage from the pool
        pool.sort(key=lambda x: usage_counts[x])
        if pool:
            # Maybe pick from the top 3 least used to add randomness
            top_candidates = pool[:max(1, len(pool)//5)]
            chosen_img = random.choice(top_candidates)
            
        if chosen_img:
            usage_counts[chosen_img] += 1
            new_url = f"/images/products/{chosen_img}"
            updates.append((new_url, p['id']))
            
    print(f"Preparing to update {len(updates)} products...")
    
    update_query = "UPDATE products SET image_url = %s WHERE id = %s"
    cursor.executemany(update_query, updates)
    conn.commit()
    
    print("Done! Updated products with local image paths.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    fix_images()
