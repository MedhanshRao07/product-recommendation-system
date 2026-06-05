import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'suggestify_db')
        )
        if connection.is_connected():
            print("MySQL connection successful")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
