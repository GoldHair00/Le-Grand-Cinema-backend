from datetime import datetime, timedelta

from app.extensions import db
from app.models.film import Film
from app.models.screening import Screening


def list_screenings(day=None, film_id=None):
    query = db.session.query(Screening, Film).join(Film, Film.id == Screening.film_id)
    if day is not None:
        start = datetime.combine(day, datetime.min.time())
        query = query.filter(
            Screening.starts_at >= start,
            Screening.starts_at < start + timedelta(days=1),
        )
    if film_id is not None:
        query = query.filter(Screening.film_id == film_id)
    return query.order_by(Screening.starts_at).all()
