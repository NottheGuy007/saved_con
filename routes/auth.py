from flask import Blueprint, request, jsonify, redirect, url_for
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    # In a real app, get and hash password
    # password = data.get('password')

    if not email: # or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = auth_service.register_user(email) #, password)

    if user is None:
        return jsonify({'error': 'User with this email already exists'}), 409

    # In a real app, log in the user or return success message
    return jsonify({'message': 'User registered successfully (mock)', 'user_id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    # password = data.get('password')

    if not email: # or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = auth_service.login_user(email) #, password) # Mock login

    if user is None:
        return jsonify({'error': 'Invalid credentials'}), 401

    # In a real app, create and return a JWT or session token
    return jsonify({'message': 'Login successful (mock)', 'user_id': user.id}), 200

# --- Mock OAuth Endpoints ---
# These simulate the redirects and callbacks.
# In a real app, the initiate would redirect the user's browser.
# The callback would be handled by the user's browser hitting this URL
# after they authorize on the platform's site.

@auth_bp.route('/oauth/<platform>', methods=['GET'])
def initiate_oauth(platform):
    user_id = request.args.get('user_id') # Get user ID from request (for mock)
    if not user_id:
         return jsonify({'error': 'user_id is required'}), 400

    # Validate platform
    supported_platforms = ['youtube', 'twitter', 'reddit']
    if platform not in supported_platforms:
        return jsonify({'error': f'Unsupported platform: {platform}'}), 400

    # Check if user exists
    user = auth_service.login_user(auth_service.register_user(f'user_{user_id}@example.com').email) # Ensure user exists for demo
    if not user or user.id != int(user_id):
         return jsonify({'error': 'User not found'}), 404

    # This returns the *mock* URL string for demonstration.
    # In a real app, you would return redirect(auth_service.initiate_oauth(...))
    mock_auth_url = auth_service.initiate_oauth(user.id, platform)

    if mock_auth_url:
        # In a real app, the frontend would navigate the user to this URL
        return jsonify({'message': f'Simulate redirecting user to {platform} for authorization.',
                        'auth_url': mock_auth_url,
                        'callback_info': 'After auth, the platform redirects to the callback URL with a "code" parameter.'}), 200
    else:
         return jsonify({'error': f'Failed to initiate OAuth for {platform}'}), 500


@auth_bp.route('/oauth/<platform>/callback', methods=['GET'])
def oauth_callback(platform):
    # In a real app, get 'code' and 'state' from request.args
    # state would typically contain user_id and other session info for security
    auth_code = request.args.get('code', 'mock_auth_code_from_platform') # Mock receiving a code
    state = request.args.get('state', 'mock_user_id-mock_platform') # Mock receiving state

    # In a real app, parse state to get user_id and verify state parameter security
    try:
        user_id_str, platform_from_state = state.split('-', 1)
        user_id = int(user_id_str)
        # Basic check: does platform match the URL?
        if platform_from_state != platform:
            return jsonify({'error': 'Platform mismatch in state parameter'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid state parameter'}), 400


    # Validate platform again
    supported_platforms = ['youtube', 'twitter', 'reddit']
    if platform not in supported_platforms:
        return jsonify({'error': f'Unsupported platform: {platform}'}), 400

    # Handle the callback - exchange code for tokens (mocked inside service)
    success = auth_service.handle_oauth_callback(user_id, platform, auth_code)

    if success:
         # In a real app, redirect user back to the frontend app with success/error status
         return jsonify({'message': f'{platform} account linked successfully for user {user_id} (mock)'}), 200
    else:
         return jsonify({'error': f'Failed to link {platform} account for user {user_id} (mock)'}), 500 # Or more specific error

@auth_bp.route('/user/<int:user_id>/platforms', methods=['GET'])
def get_user_platforms(user_id):
     # In a real app, authenticate the request to ensure the user is requesting their own data
     linked_platforms = auth_service.get_user_linked_platforms(user_id)
     return jsonify({'user_id': user_id, 'linked_platforms': linked_platforms}), 200
