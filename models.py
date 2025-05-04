from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # In a real app, store password hashes, not plain text
    # password_hash = db.Column(db.String(128))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    platform_accounts = db.relationship('PlatformAccount', backref='user', lazy='dynamic')
    saved_content = db.relationship('SavedContent', backref='user', lazy='dynamic')
    reminders = db.relationship('Reminder', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

class PlatformAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False) # 'youtube', 'twitter', 'reddit'
    # Store tokens securely, likely encrypted in a real app
    access_token = db.Column(db.String(256), nullable=False)
    refresh_token = db.Column(db.String(256)) # May not exist for all platforms
    expires_at = db.Column(db.DateTime) # Token expiration time

    __table_args__ = (db.UniqueConstraint('user_id', 'platform', name='_user_platform_uc'),)

    def __repr__(self):
        return f'<PlatformAccount {self.user.email} - {self.platform}>'

class SavedContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    original_id = db.Column(db.String(100), nullable=False) # ID on the original platform
    title = db.Column(db.String(200))
    url = db.Column(db.String(256))
    description = db.Column(db.Text)
    content_type = db.Column(db.String(50)) # e.g., 'video', 'tweet', 'post'
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    original_published_at = db.Column(db.DateTime) # Original creation time

    # Add more fields as needed for normalization (e.g., author, thumbnail, etc.)

    __table_args__ = (db.UniqueConstraint('user_id', 'platform', 'original_id', name='_user_platform_content_uc'),)

    def __repr__(self):
        return f'<SavedContent "{self.title}" from {self.platform}>'

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('saved_content.id'), nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='scheduled') # 'scheduled', 'sent', 'cancelled'

    content = db.relationship('SavedContent', backref='reminders')

    def __repr__(self):
        return f'<Reminder for content {self.content_id} at {self.reminder_time}>'
