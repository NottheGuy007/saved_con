from models import db, User, PlatformAccount
from config import Config
from flask import redirect, url_for, request # Needed for real OAuth flow, mocked here
import uuid # To generate mock tokens

class AuthService:
    def register_user(self, email):
        if User.query.filter_by(email=email).first():
            return None # User already exists
        # In a real app, handle password hashing and email verification here
        new_user = User(email=email) # password_hash=generate_password_hash(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def login_user(self, email): # Mock login - returns user if email exists
         # In a real app, verify password hash here
        user = User.query.filter_by(email=email).first()
        return user # Returns None if not found

    # --- Mock OAuth Flow ---
    # In a real app, you'd use a library like Authlib or Flask-OAuthlib
    # and handle redirects, state parameters, and token exchange with the platform API

    def initiate_oauth(self, user_id, platform):
        """Mocks initiating the OAuth flow - returns a mock auth URL."""
        if platform not in Config.PLATFORM_CREDS:
            return None # Unsupported platform

        creds = Config.PLATFORM_CREDS[platform]
        # In reality, you'd build a complex authorization URL
        # with client_id, redirect_uri, scope, state, etc.
        mock_auth_url = f"http://mock-oauth.com/auth?client_id={creds['client_id']}&redirect_uri={creds['redirect_uri']}&state={user_id}-{platform}"
        print(f"--- MOCK: Redirecting user {user_id} to {mock_auth_url} for {platform} OAuth ---")
        # For a real app, you'd return Flask's redirect(mock_auth_url)
        return mock_auth_url # Returning URL string for demonstration

    def handle_oauth_callback(self, user_id, platform, code):
        """Mocks handling the OAuth callback and exchanging code for tokens."""
        # In reality, you'd make a POST request to the platform's token endpoint
        # with the authorization 'code', client_id, client_secret, redirect_uri, etc.
        print(f"--- MOCK: Handling callback for user {user_id}, platform {platform} with code {code} ---")

        # Mock receiving tokens
        mock_access_token = f"mock_access_token_{uuid.uuid4()}"
        mock_refresh_token = f"mock_refresh_token_{uuid.uuid4()}" # May not exist for all platforms
        # Mock expiration time (e.g., 1 hour from now)
        from datetime import datetime, timedelta
        mock_expires_at = datetime.utcnow() + timedelta(hours=1)

        # Save tokens to the database
        account = PlatformAccount.query.filter_by(user_id=user_id, platform=platform).first()
        if account:
            # Update existing tokens
            account.access_token = mock_access_token
            account.refresh_token = mock_refresh_token
            account.expires_at = mock_expires_at
            print(f"--- MOCK: Updated tokens for user {user_id}, platform {platform} ---")
        else:
            # Create new account link
            new_account = PlatformAccount(
                user_id=user_id,
                platform=platform,
                access_token=mock_access_token,
                refresh_token=mock_refresh_token,
                expires_at=mock_expires_at
            )
            db.session.add(new_account)
            print(f"--- MOCK: Linked new account for user {user_id}, platform {platform} ---")

        db.session.commit()

        return True # Indicate success (in a real app, handle errors)

    def get_user_linked_platforms(self, user_id):
        """Gets platforms linked by a user."""
        user = User.query.get(user_id)
        if not user:
            return []
        return [acc.platform for acc in user.platform_accounts]
