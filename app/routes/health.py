from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.get("/health")
def health_check():
    """Vérifie que l'API répond."""
    return jsonify(status="ok")
