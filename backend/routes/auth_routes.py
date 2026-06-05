from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    print("Received register request on /api/auth/register")
    data = request.get_json()
    print(f"Request JSON Data: {data}")
    
    if not data or not all(k in data for k in ("name", "email", "password")):
        print("Error: Missing name, email, or password in request")
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    name = data['name']
    email = data['email']
    password = data['password']

    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters long'}), 400

    response, status_code = AuthService.register_user(name, email, password)
    print(f"Register Response: {response}, Status: {status_code}")
    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    print("Received login request on /api/auth/login")
    data = request.get_json()
    print(f"Request JSON Data: {data}")
    
    if not data or not all(k in data for k in ("email", "password")):
        print("Error: Missing email or password in request")
        return jsonify({'success': False, 'error': 'Missing email or password'}), 400

    email = data['email']
    password = data['password']

    response, status_code = AuthService.login_user(email, password)
    print(f"Login Response: {response}, Status: {status_code}")
    return jsonify(response), status_code

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    current_user_id = get_jwt_identity()
    from ..database.db_connection import get_connection as get_db_connection
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400
        
    response, status_code = AuthService.forgot_password(email)
    return jsonify(response), status_code

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'success': False, 'error': 'Token and new password are required'}), 400
        
    if len(new_password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters long'}), 400
        
    response, status_code = AuthService.reset_password(token, new_password)
    return jsonify(response), status_code
