from flask import Blueprint, request, jsonify
from services.reminder_service import ReminderService
# from services.auth_service import AuthService # Might need this later for token validation
from routes.content import require_auth # Use the auth decorator

reminders_bp = Blueprint('reminders', __name__, url_prefix='/api/reminders')
reminder_service = ReminderService()
# auth_service = AuthService()

@reminders_bp.route('/', methods=['POST'])
@require_auth
def create_reminder(user_id):
    data = request.json
    content_id = data.get('content_id')
    reminder_time_str = data.get('reminder_time') # e.g., "YYYY-MM-DDTHH:MM:SS"

    if not content_id or not reminder_time_str:
        return jsonify({'error': 'content_id and reminder_time are required'}), 400

    reminder = reminder_service.create_reminder(user_id, content_id, reminder_time_str)

    if reminder:
        return jsonify({
            'message': 'Reminder created successfully',
            'reminder': {
                'id': reminder.id,
                'content_id': reminder.content_id,
                'reminder_time': reminder.reminder_time.isoformat(),
                'status': reminder.status
            }
        }), 201
    else:
        return jsonify({'error': 'Failed to create reminder. Content not found or time invalid.'}), 400

@reminders_bp.route('/', methods=['POST']) # Use POST to get user_id from body
@require_auth
def get_user_reminders(user_id):
    reminders = reminder_service.get_user_reminders(user_id)

    reminders_data = []
    for r in reminders:
        reminders_data.append({
            'id': r.id,
            'content_id': r.content_id,
            'reminder_time': r.reminder_time.isoformat(),
            'created_at': r.created_at.isoformat(),
            'status': r.status,
            # Include some content info for context
            'content_title': r.content.title if r.content else None,
            'content_url': r.content.url if r.content else None,
            'content_platform': r.content.platform if r.content else None,
        })

    return jsonify(reminders_data), 200

# Endpoint to trigger the *mock* reminder processing manually
@reminders_bp.route('/process-due', methods=['POST'])
def trigger_process_reminders():
     # WARNING: Running this synchronously in a real app will block the server!
     # This is only for demonstration purposes.
     print("--- API: Received request to trigger mock reminder processing ---")
     reminder_service.process_due_reminders()
     return jsonify({'message': 'Mock reminder processing triggered (ran synchronously)'}), 200
