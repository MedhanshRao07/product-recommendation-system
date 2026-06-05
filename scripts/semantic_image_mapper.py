import mysql.connector
import os
import re
from collections import defaultdict

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mr_0706',
    'database': 'suggestify_db'
}

INVALID_KEYWORDS = [
    'diagram', 'chart', 'instruction', 'spec', 'dimension', 'technical', 'manual', 
    'compatible', 'protector', 'cover', 'case', 'stand', 'mount', 'bracket',
    'cable_saver', 'pedestal', 'replacement'
]

# 1. Define Strict Image Pools based on visual content
IMAGE_POOLS_KEYWORDS = {
    'monitor': ['monitor', 'display', 'screen'],
    'sd_card': ['microsd', 'memory_card', 'sdxc', 'uhs', 'sandisk'],
    'cable': ['cable', 'hdmi', 'usb', 'lightning', 'vga', 'rca', 'toslink', 'wire'],
    'charger': ['charger', 'adapter', 'power_bank', 'pd', 'charging'],
    'phone': ['iphone', 'galaxy', 'smartphone', 'oneplus', 'vivo', 'oppo', 'redmi', 'realme', 'nokia', 'mobile'],
    'laptop': ['laptop', 'macbook', 'xps', 'zenbook', 'matebook', 'computer'],
    'watch': ['watch', 'smartwatch', 'rolex', 'casio', 'g_shock', 'iwc', 'longines'],
    'shoe': ['shoe', 'sneaker', 'boot', 'slipper', 'trainers', 'nike', 'adidas', 'puma', 'new_balance', 'cleats'],
    'bottle': ['bottle', 'flask', 'shaker'],
    'bag': ['bag', 'backpack', 'handbag', 'messenger', 'tote', 'duffel'],
    'audio': ['headphone', 'earphone', 'earbuds', 'airpods', 'speaker', 'homepod', 'boat', 'jbl', 'noise', 'ptron'],
    'camera': ['camera', 'eos', 'monopod', 'selfie'],
    'mouse': ['mouse', 'deathadder', 'gaming_mouse'],
    'keyboard': ['keyboard', 'gaming_keyboard'],
    'tv': ['tv', 'television', 'oled', 'bravia', 'smart_tv'],
    'appliance': ['airfryer', 'kettle', 'purifier', 'cookware', 'coffeemaker', 'iron', 'appliance'],
    'sports_equip': ['ball', 'bat', 'racket', 'shuttlecock', 'helmet', 'glove'],
    'clothing': ['shirt', 'polo', 'sweater', 'dress', 'jeans', 'apparel'],
    'accessory_other': ['wallet', 'belt', 'sunglasses', 'glasses', 'earring', 'ring'],
    'fitness_other': ['foamroller', 'mat', 'yoga', 'gym']
}

def clean_string(s):
    if not s: return ""
    return re.sub(r'[^a-zA-Z0-9]', ' ', str(s)).lower()

def assign_image_pool(img_filename):
    img_clean = clean_string(img_filename)
    # Check keys in order
    for pool, keywords in IMAGE_POOLS_KEYWORDS.items():
        if any(k in img_clean.split() or k in img_clean for k in keywords):
            return pool
    return 'generic'

def assign_product_pool(p):
    combined = clean_string(p.get('name', '')) + " " + clean_string(p.get('subcategory', '')) + " " + clean_string(p.get('category', ''))
    words = combined.split()
    
    if 'monitor' in words or 'display' in words or 'screen' in words: return 'monitor'
    if 'sd' in words or 'microsd' in words or 'memory' in words: return 'sd_card'
    if 'bag' in words or 'backpack' in words or 'luggage' in words or 'tote' in words: return 'bag'
    if 'shoe' in words or 'sneaker' in words or 'boot' in words or 'footwear' in words or 'slipper' in words: return 'shoe'
    if 'watch' in words or 'smartwatch' in words: return 'watch'
    if 'cable' in words or 'hdmi' in words or 'usb' in words or 'wire' in words: return 'cable'
    if 'charger' in words or 'adapter' in words or 'power' in words and 'bank' in words: return 'charger'
    if 'phone' in words or 'smartphone' in words or 'mobile' in words: return 'phone'
    if 'laptop' in words or 'macbook' in words or 'notebook' in words: return 'laptop'
    if 'bottle' in words or 'hydration' in words or 'flask' in words: return 'bottle'
    if 'headphone' in words or 'earphone' in words or 'audio' in words or 'speaker' in words or 'earbuds' in words: return 'audio'
    if 'camera' in words or 'lens' in words or 'photography' in words: return 'camera'
    if 'mouse' in words or 'mice' in words: return 'mouse'
    if 'keyboard' in words: return 'keyboard'
    if 'tv' in words or 'television' in words: return 'tv'
    if 'appliance' in words or 'fryer' in words or 'kettle' in words or 'purifier' in words or 'coffee' in words: return 'appliance'
    if 'ball' in words or 'bat' in words or 'racket' in words or 'sports' in clean_string(p.get('category', '')): return 'sports_equip'
    if 'shirt' in words or 'clothing' in words or 'apparel' in words or 'dress' in words or 'polo' in words: return 'clothing'
    if 'wallet' in words or 'belt' in words or 'glasses' in words or 'sunglasses' in words or 'ring' in words: return 'accessory_other'
    if 'foam' in words or 'mat' in words or 'yoga' in words: return 'fitness_other'
    
    # Fallback to category mapped generic
    cat = clean_string(p.get('category', ''))
    if 'electronics' in cat: return 'phone' # fallback
    if 'fashion' in cat: return 'clothing'
    if 'home' in cat: return 'appliance'
    return 'generic'

def main():
    print("Starting STRICT Hierarchical Semantic Image Mapper...")
    images_dir = os.path.join('frontend', 'public', 'images', 'products')
    all_images = os.listdir(images_dir)
    
    # 1. Filter Invalid
    valid_images = []
    for img in all_images:
        img_clean = clean_string(img)
        if any(iv in img_clean for iv in INVALID_KEYWORDS):
            continue
        valid_images.append(img)
        
    # 2. Pool Images
    pools = defaultdict(list)
    for img in valid_images:
        pool_name = assign_image_pool(img)
        pools[pool_name].append(img)
        
    print(f"Image Pools created: { {k: len(v) for k, v in pools.items()} }")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, brand, category, subcategory FROM products")
    products = cursor.fetchall()
    
    updates = []
    usage_counts = defaultdict(int)
    
    # Category fallback boundaries (Hard Barriers)
    cat_fallbacks = {
        'Electronics': ['phone', 'laptop', 'audio', 'cable', 'charger', 'tv'],
        'Fashion': ['clothing', 'accessory_other', 'watch', 'shoe'],
        'Shoes': ['shoe'],
        'Bags': ['bag'],
        'Accessories': ['watch', 'accessory_other', 'bag'],
        'Fitness': ['fitness_other', 'bottle', 'shoe', 'sports_equip'],
        'Sports': ['sports_equip', 'shoe', 'bottle'],
        'Home Appliances': ['appliance', 'tv'],
        'Gaming': ['mouse', 'keyboard', 'audio', 'laptop']
    }
    
    for p in products:
        p_pool = assign_product_pool(p)
        cat = p.get('category', 'Other')
        
        # 3. Restrict available images to STRICT pool
        available_images = pools.get(p_pool, [])
        
        # If pool is empty or missing, fallback within HARD CATEGORY BOUNDARIES
        if not available_images:
            allowed_pools = cat_fallbacks.get(cat, ['generic'])
            for ap in allowed_pools:
                if pools.get(ap):
                    available_images.extend(pools[ap])
                    
        # If still empty, use a global safe fallback to avoid crashing
        if not available_images:
            available_images = pools.get('bag', valid_images)
            
        # 4. Brand and Semantic Scoring WITHIN the Strict Pool
        brand_words = set(clean_string(p.get('brand', '')).split())
        name_words = set(clean_string(p.get('name', '')).split())
        
        best_img = None
        best_score = -9999
        
        for img in available_images:
            img_clean = clean_string(img)
            img_words = set(img_clean.split())
            score = 0
            
            # Secondary Boost: Brand match
            if brand_words and brand_words.intersection(img_words):
                score += 100 * len(brand_words.intersection(img_words))
                
            # Name keyword match
            if name_words.intersection(img_words):
                score += 10 * len(name_words.intersection(img_words))
                
            # Diversity Penalty (Only after semantics)
            penalty = usage_counts[img] * 35
            final_score = score - penalty
            
            if final_score > best_score:
                best_score = final_score
                best_img = img
                
        if not best_img:
            best_img = available_images[0]
            
        usage_counts[best_img] += 1
        updates.append((f"/images/products/{best_img}", p['id']))
        
        if len(updates) % 150 == 0:
            print(f"[{cat}] {p.get('name')} -> Pool({p_pool}) -> {best_img} (Score: {best_score})")

    cursor.executemany("UPDATE products SET image_url = %s WHERE id = %s", updates)
    conn.commit()
    print(f"Strict Hierarchical Mapping complete! Updated {len(updates)} products.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
