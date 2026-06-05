from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from ..database.db_connection import get_connection as get_db_connection

class AuthService:
    @staticmethod
    def register_user(name, email, password):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return {'success': False, 'error': 'Email already registered'}, 400

            hashed_password = generate_password_hash(password)
            
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            conn.commit()
            
            # Fetch the newly created user to return it
            user_id = cursor.lastrowid
            cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
            new_user = cursor.fetchone()
            
            return {'success': True, 'message': 'User registered successfully', 'user': new_user}, 201
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    @staticmethod
    def login_user(email, password):
        print(f"Authenticating user '{email}' via database...")
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                print("Authentication successful, generating JWT")
                access_token = create_access_token(identity=str(user['id']))
                # remove password before returning to client
                user.pop('password', None) 
                return {'success': True, 'message': 'Login successful', 'access_token': access_token, 'user': user}, 200
            else:
                print("Authentication failed: Invalid credentials")
                return {'success': False, 'error': 'Invalid email or password'}, 401
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
        finally:
             if 'cursor' in locals():
                cursor.close()
             if 'conn' in locals() and conn.is_connected():
                conn.close()
