import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_login import LoginManager # Import LoginManager
from src.models.user import db
# Import blueprints
from src.routes.auth import auth_bp
from src.routes.agent import agent_bp

# Initialize LoginManager
login_manager = LoginManager()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Initialize LoginManager with the app
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth') # Added prefix for clarity
app.register_blueprint(agent_bp, url_prefix='/api') # Root for agent routes

# Configure PostgreSQL database
# Using peer authentication locally, user 'postgres' connects without password
# For production, use environment variables for credentials
db_user = os.getenv('DB_USERNAME', 'postgres')
db_password = os.getenv('DB_PASSWORD', '') # Assuming peer auth or trust locally
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'ia_humanizada_db')

# Construct the URI, handling empty password for peer/trust auth
db_uri = f"postgresql+psycopg2://{db_user}@{db_host}:{db_port}/{db_name}"
if db_password:
    db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all() # Create tables based on models

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
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
