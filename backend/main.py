# Import Flask to create the web application
from flask import Flask
# Import the function that registers routes from the api module
from backend.api.routes import register_routes
from backend.models import init_db

# Function to create and configure the Flask app
def create_app() -> Flask:
    # Create a new Flask application instance
    app = Flask(__name__)
    # Register all the API routes with the app
    register_routes(app)
    # Return the configured app
    return app

# Create the app instance (this is the main app object)
app = create_app()

# Only run the app if this file is executed directly (not imported)
if __name__ == "__main__":
    # Init DB (for sikkerhed)
    init_db()
    # Start the Flask development server
    # debug=True enables debug mode for error messages
    # host="0.0.0.0" makes it accessible from outside the container
    # port=5000 is the port to run on
    app.run(debug=True, host="0.0.0.0", port=5000)