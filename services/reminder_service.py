from models import db, User, SavedContent, Reminder
from datetime import datetime
from utils.email_sender import EmailSender # Import the mock email sender

class ReminderService:
    def create_reminder(self, user_id, content_id, reminder_time_str):
        content = SavedContent.query.filter_by(id=content_id, user_id=user_id).first()
        if not content:
            return None # Content not found or doesn't belong to user

        try:
            # Assuming reminder_time_str is in ISO format like 'YYYY-MM-DDTHH:MM:SS'
            reminder_time = datetime.fromisoformat(reminder_time_str)
        except ValueError:
            return None # Invalid time format

        # Optional: Check if reminder_time is in the future
        if reminder_time <= datetime.utcnow():
             print("--- REMINDER: Cannot set reminder in the past ---")
             return None

        new_reminder = Reminder(
            user_id=user_id,
            content_id=content_id,
            reminder_time=reminder_time,
            status='scheduled'
        )
        db.session.add(new_reminder)
        db.session.commit()
        print(f"--- REMINDER: Created reminder for content {content_id} at {reminder_time} for user {user_id} ---")
        return new_reminder

    def get_user_reminders(self, user_id):
        """Retrieves scheduled and past reminders for a user."""
        return Reminder.query.filter_by(user_id=user_id).order_by(Reminder.reminder_time.asc()).all()

    def process_due_reminders(self):
        """
        Mocks processing reminders that are due.
        In a real app, this would run periodically via a background scheduler.
        """
        print("\n--- REMINDER PROCESSOR: Checking for due reminders ---")
        now = datetime.utcnow()
        due_reminders = Reminder.query.filter(
            Reminder.reminder_time <= now,
            Reminder.status == 'scheduled'
        ).all()

        email_sender = EmailSender() # Instantiate the mock sender

        for reminder in due_reminders:
            user = User.query.get(reminder.user_id)
            content = SavedContent.query.get(reminder.content_id)

            if user and content:
                subject = f"Reminder: Check out this saved item from {content.platform}"
                body = f"Hi {user.email},\n\n" \
                       f"You asked to be reminded about this saved item:\n\n" \
                       f"Title: {content.title}\n" \
                       f"URL: {content.url}\n" \
                       f"Platform: {content.platform}\n\n" \
                       f"Saved on: {content.saved_at.strftime('%Y-%m-%d %H:%M')}\n\n" \
                       f"Best regards,\nYour App"

                # In a real app, handle email sending results and retries
                email_sender.send_email(user.email, subject, body)

                reminder.status = 'sent'
                print(f"--- REMINDER PROCESSOR: Sent reminder for user {user.id}, content {content.id} ---")
            else:
                # Content or User might have been deleted
                reminder.status = 'error'
                print(f"--- REMINDER PROCESSOR: Error processing reminder {reminder.id} - User or Content not found ---")


        db.session.commit()
        print("--- REMINDER PROCESSOR: Finished checking due reminders ---\n")
