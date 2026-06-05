import csv
import os
import sys
import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv

# ---- Configuration ----
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'datasets')
load_dotenv(os.path.join(PROJECT_ROOT, 'backend', '.env'))

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'suggestify_db'),
}

BACKUP_CSV = os.path.join(DATA_DIR, 'products_backup_before_cleanup.csv')
REMOVED_CSV = os.path.join(DATA_DIR, 'removed_duplicates.csv')


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print('MySQL connection successful')
            return conn
    except Error as e:
        print(f'Error connecting to MySQL: {e}')
        sys.exit(1)


def backup_products(cursor):
    print('-- Creating Backup --')
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    with open(BACKUP_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)
    print(f'Backed up {len(rows)} products to {BACKUP_CSV}')
    return rows, columns


def cleanup_data(conn, cursor, all_products, columns):
    print('\n-- Starting Cleanup --')
    
    # 1. Duplicate Handling
    name_groups = {}
    for prod in all_products:
        prod_dict = dict(zip(columns, prod))
        name = prod_dict['name'].strip().lower()
        if name not in name_groups:
            name_groups[name] = []
        name_groups[name].append(prod_dict)

    to_delete = []
    removed_logs = []

    for name, group in name_groups.items():
        if len(group) > 1:
            # Sort by rating and review_count descending
            group.sort(key=lambda x: (x.get('rating') or 0, x.get('review_count') or 0), reverse=True)
            # Keep the first (best), remove the rest
            best = group[0]
            inferiors = group[1:]
            for inf in inferiors:
                to_delete.append(inf['id'])
                removed_logs.append(inf)

    # 2. Suspiciously short names (Length < 3)
    for prod in all_products:
        prod_dict = dict(zip(columns, prod))
        name = prod_dict['name'].strip()
        if len(name) < 3 and prod_dict['id'] not in to_delete:
            to_delete.append(prod_dict['id'])
            removed_logs.append(prod_dict)

    # Delete the marked products
    if to_delete:
        print(f'Deleting {len(to_delete)} products (inferior duplicates or broken names)...')
        # We need to delete in chunks to avoid large IN clauses
        chunk_size = 100
        for i in range(0, len(to_delete), chunk_size):
            chunk = to_delete[i:i + chunk_size]
            format_strings = ','.join(['%s'] * len(chunk))
            # Because ON DELETE CASCADE is set on user_activity, related interactions will be deleted
            cursor.execute(f"DELETE FROM products WHERE id IN ({format_strings})", tuple(chunk))
        conn.commit()
        
        # Log removed products
        with open(REMOVED_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for r in removed_logs:
                writer.writerow(r)
        print(f'Logged deleted products to {REMOVED_CSV}')

    # 3. Price & Attribute Normalization
    print('\n-- Normalizing Attributes & Prices --')
    
    # Fetch remaining products
    cursor.execute("SELECT id, category, brand, price FROM products")
    remaining = cursor.fetchall()
    
    update_batch = []
    updates_made = 0
    for pid, category, brand, price in remaining:
        new_category = str(category).strip().title() if category else 'Uncategorized'
        # Electronics normalization
        if 'Electronic' in new_category:
            new_category = 'Electronics'
            
        new_brand = str(brand).strip().title() if brand else 'Unknown'
        
        # Price normalization
        new_price = float(price) if price else 0.0
        if new_price <= 0 or new_price > 10000:
            if new_category == 'Electronics':
                new_price = 199.99
            elif new_category in ['Clothing', 'Shoes']:
                new_price = 49.99
            else:
                new_price = 29.99
                
        if new_category != category or new_brand != brand or new_price != price:
            update_batch.append((new_category, new_brand, new_price, pid))
            updates_made += 1

    if update_batch:
        update_sql = "UPDATE products SET category = %s, brand = %s, price = %s WHERE id = %s"
        cursor.executemany(update_sql, update_batch)
        conn.commit()
        print(f'Normalized attributes and prices for {updates_made} products.')
    else:
        print('No attributes needed normalization.')


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        all_products, columns = backup_products(cursor)
        cleanup_data(conn, cursor, all_products, columns)
        print('\nCleanup completed successfully!')
    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
