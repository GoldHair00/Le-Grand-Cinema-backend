from flask import Blueprint, jsonify, request

from app.schemas.screening import ScreeningQuerySchema
from app.services import screening_service
from app.extensions import db
from app.models import Seat, Reservation, Screening

screenings_bp = Blueprint("screenings", __name__, url_prefix="/api/screenings")


@screenings_bp.route("", methods=["GET"])
def list_screenings():
    """Lister les séances, filtrables par date et par film
    ---
    tags:
      - Séances
    parameters:
      - in: query
        name: date
        type: string
        format: date
        example: "2026-07-10"
      - in: query
        name: film_id
        type: integer
    responses:
      200:
        description: Liste des séances triées par heure de début
      422:
        description: Paramètres invalides
    """
    params = ScreeningQuerySchema().load(request.args.to_dict())
    rows = screening_service.list_screenings(
        day=params.get("date"), film_id=params.get("film_id")
    )
    result = [
        {
            "id": screening.id,
            "film_id": film.id,
            "film_title": film.title,
            "room_id": screening.room_id,
            "starts_at": screening.starts_at.isoformat(),
            "price": str(screening.price),
        }
        for screening, film in rows
    ]
    return jsonify(result), 200


@screenings_bp.route("/<int:screening_id>/seats", methods=["GET"])
def list_screening_seats(screening_id):
    """
    Liste les sièges d'une séance et leur disponibilité.
    ---
    tags:
      - Séances
    parameters:
      - in: path
        name: screening_id
        required: true
        type: integer
    responses:
      200:
        description: Liste des sièges et de leur disponibilité
      404:
        description: Séance introuvable
    """
    screening = db.session.get(Screening, screening_id)

    if screening is None:
        return jsonify({"message": "Séance introuvable"}), 404

    seats = Seat.query.filter_by(
        room_id=screening.room_id
    ).order_by(
        Seat.row_label, Seat.number
    ).all()

    reserved_seat_ids = {
        reservation.seat_id
        for reservation in Reservation.query.filter_by(
            screening_id=screening_id
        ).all()
    }

    return jsonify([
        {
            "id": seat.id,
            "row": seat.row_label,
            "number": seat.number,
            "available": seat.id not in reserved_seat_ids
        }
        for seat in seats
    ]), 200
