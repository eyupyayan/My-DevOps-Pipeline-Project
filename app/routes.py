from flask import Blueprint, jsonify, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .utils import get_status_payload, REQUEST_COUNT

bp = Blueprint("routes", __name__)


def register_routes(app):
    @bp.route("/")
    def home():
        REQUEST_COUNT.labels(endpoint="/").inc()
        return jsonify(
            {
                "message": "Welcome to my-devops-app",
                "hint": "Try /health, /info or /metrics",
            }
        )

    @bp.route("/health")
    def health():
        REQUEST_COUNT.labels(endpoint="/health").inc()
        return jsonify({"status": "ok"}), 200

    @bp.route("/info")
    def info():
        REQUEST_COUNT.labels(endpoint="/info").inc()
        return jsonify(get_status_payload(app.config["APP_CONFIG"]))

    @bp.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    app.register_blueprint(bp)