"""
Schema Migration: Add subcategory and popularity_score to products table.
Safe to run multiple times — checks for column existence before altering.
"""
import os
import sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

def migrate():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'suggestify_db')
    )
    cursor = conn.cursor()

    # Add subcategory column
    cursor.execute("SHOW COLUMNS FROM products LIKE 'subcategory'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE products ADD COLUMN subcategory VARCHAR(100) AFTER category")
        print("[+] Added 'subcategory' column")
    else:
        print("[=] 'subcategory' column already exists")

    # Add popularity_score column
    cursor.execute("SHOW COLUMNS FROM products LIKE 'popularity_score'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE products ADD COLUMN popularity_score FLOAT DEFAULT 0.0")
        print("[+] Added 'popularity_score' column")
    else:
        print("[=] 'popularity_score' column already exists")

    # Ensure user_activity table exists with proper structure
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_activity (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            action VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_product_id (product_id),
            INDEX idx_created_at (created_at)
        )
    """)
    print("[+] user_activity table ensured")

    conn.commit()
    cursor.close()
    conn.close()
    print("[OK] Migration complete.")

if __name__ == "__main__":
    migrate()
