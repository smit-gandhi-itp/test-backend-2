from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint that returns a JWT token.
    
    Request Body:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        200: {
            "access_token": "string",
            "token_type": "Bearer",
            "expires_in": 3600,
            "user": {
                "id": int,
                "username": "string",
                "email": "string"
            }
        }
        400: {"error": "Username and password are required"}
        401: {"error": "Invalid credentials"}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        result = auth_service.login(username, password)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'An error occurred during login'}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint.
    
    Request Body:
        {
            "username": "string",
            "password": "string",
            "email": "string" (optional)
        }
    
    Returns:
        201: {
            "message": "User registered successfully",
            "user": {
                "id": int,
                "username": "string",
                "email": "string"
            }
        }
        400: {"error": "Username and password are required"}
        409: {"error": "Username already exists"}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400
        
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = auth_service.register(username, password, email)
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': 'An error occurred during registration'}), 500
