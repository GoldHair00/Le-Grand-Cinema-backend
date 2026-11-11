
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services import reservation_service

reservations_bp = Blueprint(
    "reservations",
    __name__,
    url_prefix="/api/reservations"
)


@reservations_bp.route("", methods=["POST"])
@jwt_required()
def create_reservation():
    data = request.get_json(silent=True) or {}

    screening_id = data.get("screening_id")
    seat_id = data.get("seat_id")

    if not isinstance(screening_id, int) or not isinstance(seat_id, int):
        return jsonify({
            "error": "validation_error",
            "message": "screening_id et seat_id doivent être des entiers"
        }), 422

    reservation = reservation_service.create_reservation(
        user_id=int(get_jwt_identity()),
        screening_id=screening_id,
        seat_id=seat_id,
    )

    return jsonify({
        "id": reservation.id,
        "screening_id": reservation.screening_id,
        "seat_id": reservation.seat_id,
        "reserved_at": reservation.reserved_at.isoformat(),
    }), 201
