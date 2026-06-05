"""
Database Seeder for Suggestify
Loads the generated catalog SQL into the MySQL database.
Usage: python scripts/seed_catalog.py
"""
import os
import sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

CATALOG_SQL = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'catalog_seed.sql')

def seed():
    if not os.path.exists(CATALOG_SQL):
        print(f"[ERROR] Catalog SQL file not found: {CATALOG_SQL}")
        print("Run 'python scripts/generate_catalog.py' first.")
        sys.exit(1)

    print(f"[*] Reading catalog from {CATALOG_SQL}...")
    with open(CATALOG_SQL, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split into individual statements
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]

    print(f"[*] Found {len(statements)} SQL statements")
    print("[*] Connecting to database...")

    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'suggestify_db'),
        charset='utf8mb4',
        collation='utf8mb4_unicode_ci'
    )
    cursor = conn.cursor()

    # Execute each statement
    success = 0
    errors = 0
    for i, stmt in enumerate(statements):
        try:
            cursor.execute(stmt)
            success += 1
            if (i + 1) % 10 == 0:
                print(f"  [{i+1}/{len(statements)}] statements executed...")
        except Exception as e:
            errors += 1
            print(f"  [ERROR] Statement {i+1}: {str(e)[:100]}")

    conn.commit()

    # Verify
    cursor.execute("SELECT COUNT(*) FROM products")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) as cnt FROM products GROUP BY category ORDER BY cnt DESC")
    distribution = cursor.fetchall()

    cursor.execute("SELECT category, subcategory, COUNT(*) as cnt FROM products GROUP BY category, subcategory ORDER BY category, cnt DESC")
    sub_distribution = cursor.fetchall()

    print(f"\n{'='*60}")
    print(f"  SEED COMPLETE")
    print(f"{'='*60}")
    print(f"  Total products: {total}")
    print(f"  Statements: {success} OK, {errors} errors")
    print(f"\n  Category Distribution:")
    for cat, cnt in distribution:
        print(f"    {cat}: {cnt}")
    print(f"\n  Subcategory Distribution:")
    current_cat = None
    for cat, sub, cnt in sub_distribution:
        if cat != current_cat:
            print(f"\n    [{cat}]")
            current_cat = cat
        print(f"      {sub}: {cnt}")

    cursor.close()
    conn.close()
    print(f"\n[OK] Database seeded successfully with {total} products.")

if __name__ == "__main__":
    seed()
