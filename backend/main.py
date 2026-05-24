from flask import Flask
from backend.api.routes import api_blueprint
from backend.db import create_tables

app = Flask(__name__)
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True, host="0.0.0.0", port=5000)