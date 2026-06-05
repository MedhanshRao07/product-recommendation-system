import os
import csv
import random
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'datasets')
PRODUCTS_CSV = os.path.join(DATA_DIR, 'products.csv')
INTERACTIONS_CSV = os.path.join(DATA_DIR, 'interactions.csv')

def load_products():
    products = []
    category_map = {}
    with open(PRODUCTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = int(row['id'])
            cat = row['category']
            price = float(row.get('price', 0))
            products.append(row)
            category_map.setdefault(cat, []).append((pid, price))
    return products, category_map

# The 5 strict Personas with their preferred categories
PERSONAS = {
    'Tech Enthusiast': ['Electronics', 'Headphones'],
    'Fitness Shopper': ['Fitness', 'Shoes'],
    'Fashion Shopper': ['Bags', 'Watches', 'Accessories', 'Shoes'],
    'Luxury Buyer': ['Watches', 'Electronics', 'Bags'], # Will prioritize high price items
    'Casual Shopper': [] # Broad mixed behavior
}

# Related category map for 15-30% exploration
RELATED_CATEGORIES = {
    'Electronics': ['Headphones', 'Accessories', 'Watches'],
    'Headphones': ['Electronics', 'Accessories'],
    'Fitness': ['Shoes', 'Accessories'],
    'Shoes': ['Fitness', 'Bags'],
    'Watches': ['Accessories', 'Bags', 'Electronics'],
    'Bags': ['Fashion', 'Watches', 'Accessories'],
    'Accessories': ['Watches', 'Bags']
}

# Weighted actions: view, wishlist, add_to_cart, purchase
# Purchases should be less frequent but more realistic
ACTIONS = ['view', 'wishlist', 'add_to_cart', 'purchase']
ACTION_WEIGHTS = [0.65, 0.15, 0.15, 0.05]

def get_target_categories(persona, all_categories):
    if persona == 'Casual Shopper':
        return all_categories, all_categories
        
    preferred = PERSONAS[persona]
    related = set()
    for cat in preferred:
        related.update(RELATED_CATEGORIES.get(cat, []))
        
    related = [c for c in related if c not in preferred and c in all_categories]
    if not related:
        related = all_categories
        
    return preferred, related

def generate_user_session(user_id, category_map, now):
    persona = random.choice(list(PERSONAS.keys()))
    all_categories = list(category_map.keys())
    preferred_cats, related_cats = get_target_categories(persona, all_categories)
    
    num_interactions = random.randint(30, 80)
    user_history = []
    
    current_time = now - timedelta(days=random.randint(1, 180))
    recently_viewed = []
    
    for _ in range(num_interactions):
        current_time += timedelta(minutes=random.randint(1, 120))
        
        # 30% chance to repeat interaction (e.g. view -> add to cart -> purchase)
        if recently_viewed and random.random() < 0.3:
            prod_id = random.choice(recently_viewed)
        else:
            # 70-85% inside preferred, 15-30% related exploration
            explore_chance = random.uniform(0.15, 0.30)
            if persona == 'Casual Shopper' or random.random() < explore_chance:
                target_cat = random.choice(related_cats) if related_cats else random.choice(all_categories)
            else:
                target_cat = random.choice(preferred_cats) if preferred_cats else random.choice(all_categories)
            
            # Fallback
            if target_cat not in category_map or not category_map[target_cat]:
                target_cat = random.choice(all_categories)
                
            pool = category_map[target_cat]
            
            # Luxury buyer bias towards higher priced items
            if persona == 'Luxury Buyer' and random.random() < 0.7:
                pool = sorted(pool, key=lambda x: x[1], reverse=True)[:max(1, len(pool)//3)]
                
            prod_id, _ = random.choice(pool)
            recently_viewed.append(prod_id)
            if len(recently_viewed) > 8:
                recently_viewed.pop(0)
                
        action = random.choices(ACTIONS, weights=ACTION_WEIGHTS)[0]
        
        user_history.append({
            'user_id': user_id,
            'product_id': prod_id,
            'action': action,
            'rating': "",
            'purchase': 1 if action == 'purchase' else 0,
            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    return user_history

def main():
    print("--- Phase 3A: Generating Advanced Persona Interactions ---")
    products, category_map = load_products()
    
    if not products:
        print("Error: No products found.")
        return
        
    interactions = []
    num_users = 500
    now = datetime.now()
    
    print(f"Simulating {num_users} users with strict Phase 3 personas...")
    for user_id in range(1, num_users + 1):
        user_history = generate_user_session(user_id, category_map, now)
        interactions.extend(user_history)
        
    interactions.sort(key=lambda x: x['timestamp'])
    
    print(f"Generated {len(interactions)} realistic interactions.")
    
    with open(INTERACTIONS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['user_id', 'product_id', 'action', 'rating', 'purchase', 'timestamp'])
        writer.writeheader()
        writer.writerows(interactions)
        
    print(f"Saved to {INTERACTIONS_CSV}")

if __name__ == "__main__":
    main()
