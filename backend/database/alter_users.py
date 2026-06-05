import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def alter_table():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'suggestify_db')
        )
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if columns exist first
            cursor.execute("SHOW COLUMNS FROM users LIKE 'reset_token'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN reset_token VARCHAR(255) DEFAULT NULL;")
                print("Added reset_token column.")
                
            cursor.execute("SHOW COLUMNS FROM users LIKE 'reset_token_expiry'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME DEFAULT NULL;")
                print("Added reset_token_expiry column.")
                
            connection.commit()
            print("Database altered successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    alter_table()
