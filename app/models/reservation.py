
from app.extensions import db


class Reservation(db.Model):
    __tablename__ = "reservations"
    __table_args__ = (
        db.UniqueConstraint(
            "screening_id",
            "seat_id",
            name="uq_reservation_screening_seat"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    screening_id = db.Column(
        db.Integer,
        db.ForeignKey("screenings.id"),
        nullable=False
    )
    seat_id = db.Column(
        db.Integer,
        db.ForeignKey("seats.id"),
        nullable=False
    )
    reserved_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )
