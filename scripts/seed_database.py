"""
Seed MySQL database from generated CSV files.
Reads products.csv and interactions.csv, creates/replaces tables, and bulk-inserts data.
"""

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

PRODUCTS_CSV = os.path.join(DATA_DIR, 'products.csv')
INTERACTIONS_CSV = os.path.join(DATA_DIR, 'interactions.csv')


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print('MySQL connection successful')
            return conn
    except Error as e:
        print(f'Error connecting to MySQL: {e}')
        sys.exit(1)


def seed_products(cursor, conn):
    """Drop and recreate products table, then bulk insert from CSV."""
    print('\n-- Seeding products --')

    cursor.execute('DROP TABLE IF EXISTS user_activity')
    cursor.execute('DROP TABLE IF EXISTS interactions')
    cursor.execute('DROP TABLE IF EXISTS products')

    cursor.execute("""
        CREATE TABLE products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
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
            INDEX idx_category (category),
            INDEX idx_brand (brand),
            INDEX idx_rating (rating)
        )
    """)
    print('  Products table created')

    # Read CSV and insert
    with open(PRODUCTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    insert_sql = """
        INSERT INTO products (id, name, category, brand, price, rating, review_count, color, image_url, description, tags, features, amazon_url, flipkart_url, myntra_url, price_range)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    batch = []
    for row in rows:
        batch.append((
            int(row['id']),
            row['name'],
            row['category'],
            row['brand'],
            float(row['price']),
            float(row['rating']),
            int(row.get('review_count', 0)),
            row.get('color', ''),
            row['image_url'],
            row['description'],
            row.get('tags', ''),
            row.get('features', ''),
            row.get('amazon_url', ''),
            row.get('flipkart_url', ''),
            row.get('myntra_url', ''),
            row.get('price_range', ''),
        ))

    cursor.executemany(insert_sql, batch)
    conn.commit()
    print(f'  Inserted {len(batch)} products')


def seed_user_activity(cursor, conn):
    """Create user_activity table (used by the existing recommendation system)."""
    print('\n-- Creating user_activity table --')

    cursor.execute('DROP TABLE IF EXISTS user_activity')
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
    print('  user_activity table created')

    # Pre-seed with some interactions from CSV to give the recommendation engine data
    with open(INTERACTIONS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    insert_sql = """
        INSERT INTO user_activity (user_id, product_id, action, created_at)
        VALUES (%s, %s, %s, %s)
    """

    batch = []
    for row in rows:
        batch.append((
            int(row['user_id']),
            int(row['product_id']),
            row['action'],
            row['timestamp'],
        ))

    cursor.executemany(insert_sql, batch)
    conn.commit()
    print(f'  Inserted {len(batch)} user activity records')


def print_summary(cursor):
    """Print a summary of seeded data."""
    print('\n-- Database Summary --')

    cursor.execute('SELECT COUNT(*) FROM products')
    print(f'  Total products: {cursor.fetchone()[0]}')

    cursor.execute('SELECT category, COUNT(*) as cnt FROM products GROUP BY category ORDER BY cnt DESC')
    for row in cursor.fetchall():
        print(f'    {row[0]}: {row[1]}')

    cursor.execute('SELECT COUNT(*) FROM user_activity')
    print(f'  Total user activities: {cursor.fetchone()[0]}')

    cursor.execute('SELECT action, COUNT(*) as cnt FROM user_activity GROUP BY action ORDER BY cnt DESC')
    for row in cursor.fetchall():
        print(f'    {row[0]}: {row[1]}')

    cursor.execute('SELECT COUNT(DISTINCT user_id) FROM user_activity')
    print(f'  Unique users: {cursor.fetchone()[0]}')


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        seed_products(cursor, conn)
        seed_user_activity(cursor, conn)
        print_summary(cursor)
        print('\nDatabase seeded successfully!')
    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()
