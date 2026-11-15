
from flask import Blueprint, jsonify

from app.models.film import Film

films_bp = Blueprint("films", __name__, url_prefix="/api/films")


@films_bp.get("")
def get_films():
    """
    Liste des films
    ---
    tags:
      - Films
    responses:
      200:
        description: Liste des films
    """
    films = Film.query.order_by(Film.title.asc()).all()

    return jsonify([
        {
            "id": film.id,
            "title": film.title,
            "description": film.description,
            "duration_minutes": film.duration_minutes
        }
        for film in films
    ]), 200
