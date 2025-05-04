from flask import Flask, jsonify
from config import Config
from models import db
from routes.auth import auth_bp
from routes.content import content_bp
from routes.reminders import reminders_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # mail.init_app(app) # If using Flask-Mail

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(reminders_bp)

    @app.route('/')
    def index():
        return "Backend is running!"

    @app.route('/api')
    def api_index():
        return jsonify({'message': 'Welcome to the API!',
                        'endpoints': {
                            'auth': '/api/auth',
                            'content': '/api/content',
                            'reminders': '/api/reminders'
                        }})

    # Add a route to initialize the database (for development/testing)
    @app.cli.command('init-db')
    def init_db_command():
        """Clear existing data and create new tables."""
        print('Initializing the database...')
        db.drop_all()
        db.create_all()
        print('Initialized the database.')

    return app

# This part allows running the app directly from this file
if __name__ == '__main__':
    app = create_app()
    # Ensure a SECRET_KEY is set for production, even for the mock.
    # In production
  
