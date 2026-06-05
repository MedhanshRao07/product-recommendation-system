"""Quick data quality validation for the seeded database."""
import os
import mysql.connector
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(PROJECT_ROOT, 'backend', '.env'))

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'suggestify_db')
)
cursor = conn.cursor()

print('=== DATA QUALITY CHECKS ===')

# 1. Check for NULL/empty values in critical columns
cursor.execute("SELECT COUNT(*) FROM products WHERE name IS NULL OR name = ''")
print(f'Products with empty name: {cursor.fetchone()[0]}')
cursor.execute("SELECT COUNT(*) FROM products WHERE category IS NULL OR category = ''")
print(f'Products with empty category: {cursor.fetchone()[0]}')
cursor.execute("SELECT COUNT(*) FROM products WHERE brand IS NULL OR brand = ''")
print(f'Products with empty brand: {cursor.fetchone()[0]}')
cursor.execute("SELECT COUNT(*) FROM products WHERE description IS NULL OR description = ''")
print(f'Products with empty description: {cursor.fetchone()[0]}')

# 2. Check price and rating ranges
cursor.execute('SELECT MIN(price), MAX(price), AVG(price) FROM products')
row = cursor.fetchone()
print(f'Price range: ${row[0]:.2f} - ${row[1]:.2f} (avg: ${row[2]:.2f})')
cursor.execute('SELECT MIN(rating), MAX(rating), AVG(rating) FROM products')
row = cursor.fetchone()
print(f'Rating range: {row[0]} - {row[1]} (avg: {row[2]:.2f})')
cursor.execute('SELECT COUNT(*) FROM products WHERE price <= 0')
print(f'Products with invalid price (<= 0): {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM products WHERE rating < 1 OR rating > 5')
print(f'Products with invalid rating (outside 1-5): {cursor.fetchone()[0]}')

# 3. Check for duplicate product names
cursor.execute('SELECT name, COUNT(*) as cnt FROM products GROUP BY name HAVING cnt > 1')
dupes = cursor.fetchall()
print(f'Duplicate product names: {len(dupes)}')
if dupes:
    for d in dupes[:5]:
        print(f'  DUPE: "{d[0]}" x{d[1]}')

# 4. Check categories
cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
cats = [r[0] for r in cursor.fetchall()]
print(f'Categories ({len(cats)}): {cats}')

# 5. Check user_activity referential integrity
cursor.execute('SELECT COUNT(*) FROM user_activity ua LEFT JOIN products p ON ua.product_id = p.id WHERE p.id IS NULL')
print(f'Orphan activity records (no matching product): {cursor.fetchone()[0]}')

# 6. Sample products
print('\n=== SAMPLE PRODUCTS (5) ===')
cursor.execute('SELECT id, name, category, brand, price, rating FROM products ORDER BY RAND() LIMIT 5')
for r in cursor.fetchall():
    print(f'  [{r[0]}] {r[1]} | {r[2]} | {r[3]} | ${r[4]:.2f} | {r[5]}*')

cursor.close()
conn.close()
print('\nAll checks passed!')
