from flask import Blueprint, jsonify
from .utils import get_status_payload

bp = Blueprint("routes", __name__)


def register_routes(app):
    @bp.route("/")
    def home():
        return jsonify(
            {
                "message": "Welcome to my-devops-app",
                "hint": "Try /health or /info",
            }
        )

    @bp.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @bp.route("/info")
    def info():
        return jsonify(get_status_payload(app.config["APP_CONFIG"]))

    app.register_blueprint(bp)