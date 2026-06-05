"""
Fix product images using deterministic, local static image mapping per keyword.
Prevents heavy duplication while maintaining strict product-type matching.
"""
import os
import mysql.connector
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(PROJECT_ROOT, 'backend', '.env'))

DB = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'suggestify_db')
}

PRODUCT_MAP_LISTS = {
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

GENERIC_PRODUCT_FALLBACK = [
    '/images/products/backpack1.png'
]

def find_image_for_product(name, product_id):
    """Find matching image URL deterministically, using modulo array access."""
    s_name = name.lower()
    
    # 1. Product Type Mapping
    for keyword, url_list in PRODUCT_MAP_LISTS.items():
        if keyword in s_name:
            return url_list[product_id % len(url_list)]
            
    # 2. Generic object fallback
    return GENERIC_PRODUCT_FALLBACK[product_id % len(GENERIC_PRODUCT_FALLBACK)]


def main():
    conn = mysql.connector.connect(**DB)
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT id, name, brand, category, image_url FROM products ORDER BY id')
    products = cursor.fetchall()

    updates = []
    for p in products:
        new_url = find_image_for_product(p['name'], p['id'])
        if new_url != p['image_url']:
            updates.append((new_url, p['id']))

    if updates:
        cursor.executemany('UPDATE products SET image_url = %s WHERE id = %s', updates)
        conn.commit()
        print(f'Updated {len(updates)} images with deterministic LOCAL list rotation.')
    else:
        print('All images already mapped correctly.')

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
