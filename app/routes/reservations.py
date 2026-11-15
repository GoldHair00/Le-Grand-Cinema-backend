
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
    """
    Créer une réservation
    ---
    tags:
      - Reservations
    summary: Réserver une place pour une séance
    description: Nécessite un jeton JWT valide.
    security:
      - Bearer: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - screening_id
            - seat_id
          properties:
            screening_id:
              type: integer
              example: 1
            seat_id:
              type: integer
              example: 5
    responses:
      201:
        description: Réservation créée avec succès
      400:
        description: Séance ou place invalide
      401:
        description: Authentification requise ou jeton invalide
      409:
        description: Cette place est déjà réservée pour cette séance
      422:
        description: Données invalides
    """

    data = request.get_json(silent=True) or {}

    screening_id = data.get("screening_id")
    seat_id = data.get("seat_id")

    if (
        not isinstance(screening_id, int)
        or isinstance(screening_id, bool)
        or not isinstance(seat_id, int)
        or isinstance(seat_id, bool)
    ):
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
