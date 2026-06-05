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

    @staticmethod
    def forgot_password(email):
        import uuid
        from datetime import datetime, timedelta
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if not cursor.fetchone():
                return {'success': False, 'error': 'If this email is registered, a reset link will be sent.'}, 200

            reset_token = str(uuid.uuid4())
            expiry = datetime.now() + timedelta(hours=1)
            
            cursor.execute(
                "UPDATE users SET reset_token = %s, reset_token_expiry = %s WHERE email = %s",
                (reset_token, expiry, email)
            )
            conn.commit()
            
            # In a real app, send an email here. For this demo, we'll return the token.
            return {'success': True, 'message': 'If this email is registered, a reset link will be sent.', 'reset_token': reset_token}, 200
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
        finally:
             if 'cursor' in locals():
                cursor.close()
             if 'conn' in locals() and conn.is_connected():
                conn.close()

    @staticmethod
    def reset_password(token, new_password):
        from datetime import datetime
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT id, reset_token_expiry FROM users WHERE reset_token = %s", (token,))
            user = cursor.fetchone()
            
            if not user:
                return {'success': False, 'error': 'Invalid or expired reset token'}, 400
                
            if user['reset_token_expiry'] and user['reset_token_expiry'] < datetime.now():
                return {'success': False, 'error': 'Reset token has expired'}, 400

            hashed_password = generate_password_hash(new_password)
            
            cursor.execute(
                "UPDATE users SET password = %s, reset_token = NULL, reset_token_expiry = NULL WHERE id = %s",
                (hashed_password, user['id'])
            )
            conn.commit()
            
            return {'success': True, 'message': 'Password has been successfully reset'}, 200
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
        finally:
             if 'cursor' in locals():
                cursor.close()
             if 'conn' in locals() and conn.is_connected():
                conn.close()
