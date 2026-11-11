
from app.errors import InvalidSeatError, ReservationConflictError
from app.extensions import db
from app.models import Reservation, Screening, Seat


def create_reservation(user_id, screening_id, seat_id):
    screening = db.session.get(Screening, screening_id)
    seat = db.session.get(Seat, seat_id)

    if screening is None:
        raise InvalidSeatError("Séance introuvable")

    if seat is None or seat.room_id != screening.room_id:
        raise InvalidSeatError("Cette place n'appartient pas à la salle de cette séance")

    reservation = Reservation(
        user_id=user_id,
        screening_id=screening_id,
        seat_id=seat_id,
    )

    try:
        db.session.add(reservation)
        db.session.commit()
    except Exception as error:
        db.session.rollback()

        # La contrainte unique en base protège aussi contre
        # deux réservations simultanées de la même place.
        from sqlalchemy.exc import IntegrityError

        if isinstance(error, IntegrityError):
            raise ReservationConflictError(
                "Cette place est déjà réservée pour cette séance"
            ) from error

        raise

    return reservation
