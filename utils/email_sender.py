# In a real app, use Flask-Mail or smtplib with your email provider credentials
# from flask_mail import Mail, Message # If using Flask-Mail

class EmailSender:
    """Mock Email Sending Utility."""
    def __init__(self):
        # In a real app, configure Flask-Mail or smtplib
        print("--- MOCK: EmailSender initialized ---")

    def send_email(self, to, subject, body):
        """Mocks sending an email by printing to the console."""
        print("\n--- MOCK EMAIL START ---")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print("Body:")
        print(body)
        print("--- MOCK EMAIL END ---\n")
        # In a real app:
        # msg = Message(subject, recipients=[to], body=body)
        # mail.send(msg) # Assuming 'mail' is a Flask-Mail instance
