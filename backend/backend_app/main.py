import os
import sys

# Add the project root to the Python path
# This might not be strictly necessary depending on how Flask discovers the app,
# but can help in some environments.
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import create_app # Import the factory function

app = create_app() # Create the Flask app instance

if __name__ == '__main__':
    # Use environment variable for port or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Run the app
    # debug=True is useful for development but should be False in production
    app.run(host='0.0.0.0', port=port, debug=os.getenv("FLASK_DEBUG", "True") == "True")

