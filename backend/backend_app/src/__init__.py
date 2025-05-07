from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS # Import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Configure CORS
    # Allow all origins for development, restrict in production
    # Also allow credentials (cookies)
    CORS(app, supports_credentials=True, origins="*") # Adjust origins for production
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT') # Use env var or default

    # Configure PostgreSQL database
    db_user = os.getenv('DB_USERNAME', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '') # Assuming peer auth or trust locally
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'ia_humanizada_db')

    db_uri = f"postgresql+psycopg2://{db_user}@{db_host}:{db_port}/{db_name}"
    if db_password:
        db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Specify the login view for @login_required

    # Import models here to ensure they are registered with SQLAlchemy
    from .models.user import User
    from .models.agent import Agent, KnowledgeBase

    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.agent import agent_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(agent_bp, url_prefix='/api')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # --- Static file serving (Keep as is or adjust if needed) --- #
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
                return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                # If no index.html, maybe return API status or a simple message
                # return "index.html not found", 404
                 return jsonify({"message": "Backend API is running. No frontend index.html found."}), 200

    return app

