import os
from flask import Flask, jsonify
from backend.api.routes import api_blueprint
from backend.db import init_pool, create_tables

app = Flask(__name__)
app.register_blueprint(api_blueprint)

init_pool()
create_tables()

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false") == "true", host="0.0.0.0", port=5000)