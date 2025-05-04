from flask import Blueprint, request, jsonify
from services.data_aggregator_service import DataAggregatorService
# from services.auth_service import AuthService # Might need this later for token validation

content_bp = Blueprint('content', __name__, url_prefix='/api/content')
data_aggregator_service = DataAggregatorService()
# auth_service = AuthService() # For authentication

# Middleware/Decorator for authentication (placeholder)
def require_auth(f):
    # In a real app, this would check for a valid token/session in the request headers/cookies
    # and lookup the user. For this demo, we'll just require a 'user_id' in the body/args.
    # @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.json.get('user_id') if request.json else request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required: user_id missing'}), 401
        # In a real app, lookup user by token and pass user object or user_id
        kwargs['user_id'] = int(user_id) # Pass the user_id extracted
        return f(*args, **kwargs)
    return decorated_function


@content_bp.route('/', methods=['POST']) # Use POST to get user_id from body
@require_auth
def get_user_content(user_id):
    platform = request.json.get('platform') # Optional filter
    content_list = data_aggregator_service.get_user_content(user_id, platform)

    # Serialize the content list to JSON
    content_data = []
    for item in content_list:
        content_data.append({
            'id': item.id,
            'platform': item.platform,
            'original_id': item.original_id,
            'title': item.title,
            'url': item.url,
            'description': item.description,
            'content_type': item.content_type,
            'saved_at': item.saved_at.isoformat(),
            'original_published_at': item.original_published_at.isoformat() if item.original_published_at else None
        })

    return jsonify(content_data), 200

@content_bp.route('/sync/<platform>', methods=['POST'])
@require_auth
def sync_platform(user_id, platform):
    # In a real app, this would typically just *trigger* a background job
    # not perform the sync synchronously within the request handler.
    # user_id is passed by require_auth decorator

    supported_platforms = ['youtube', 'twitter', 'reddit']
    if platform not in supported_platforms:
         return jsonify({'error': f'Unsupported platform: {platform}'}), 400

    print(f"--- API: Received manual sync request for user {user_id}, platform {platform} ---")
    success = data_aggregator_service.sync_user_platform(user_id, platform) # Sync directly for demo

    if success:
        return jsonify({'message': f'Manual sync triggered for {platform} for user {user_id} (mock - ran synchronously)'}), 200
    else:
        return jsonify({'error': f'Failed to trigger sync for {platform} for user {user_id}. Check if account is linked.'}), 400

# Endpoint to trigger the *mock* full background sync process manually
@content_bp.route('/sync/all', methods=['POST'])
def trigger_full_sync():
     # WARNING: Running this synchronously in a real app will block the server!
     # This is only for demonstration purposes to show the mock scheduler function.
     print("--- API: Received request to trigger mock full sync ---")
     data_aggregator_service.schedule_full_sync()
     return jsonify({'message': 'Mock full sync process triggered (ran synchronously)'}), 200
