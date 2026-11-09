from flask import Blueprint, jsonify, request

from app.schemas.screening import ScreeningQuerySchema
from app.services import screening_service

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