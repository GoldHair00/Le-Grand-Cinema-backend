from app.extensions import db


class Seat(db.Model):
    __tablename__ = "seats"
    __table_args__ = (
        db.UniqueConstraint("room_id", "row_label", "number", name="uq_seat_position"),
    )

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    row_label = db.Column(db.String(2), nullable=False)
    number = db.Column(db.Integer, nullable=False)