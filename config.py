import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key-for-dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Placeholder for platform credentials - replace with actual values and secure storage
    PLATFORM_CREDS = {
        'youtube': {
            'client_id': os.environ.get('YOUTUBE_CLIENT_ID', 'mock_youtube_client_id'),
            'client_secret': os.environ.get('YOUTUBE_CLIENT_SECRET', 'mock_youtube_client_secret'),
            'redirect_uri': 'http://localhost:5000/api/auth/oauth/youtube/callback'
        },
        'twitter': { # Twitter API is now X API - requires different approach/pricing
            'client_id': os.environ.get('TWITTER_CLIENT_ID', 'mock_twitter_client_id'),
            'client_secret': os.environ.get('TWITTER_CLIENT_SECRET', 'mock_twitter_client_secret'),
            'redirect_uri': 'http://localhost:5000/api/auth/oauth/twitter/callback'
        },
        'reddit': {
            'client_id': os.environ.get('REDDIT_CLIENT_ID', 'mock_reddit_client_id'),
            'client_secret': os.environ.get('REDDIT_CLIENT_SECRET', 'mock_reddit_client_secret'),
            'redirect_uri': 'http://localhost:5000/api/auth/oauth/reddit/callback'
        }
    }

    # Mock email settings
    MAIL_SERVER = 'smtp.mock.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'mock_user')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'mock_password')
    ADMINS = ['admin@mock.com']
