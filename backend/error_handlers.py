from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_error(e):
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return jsonify({"error": str(e)}), 400
