from app.extensions import db


class Screening(db.Model):
    __tablename__ = "screenings"

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey("films.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    starts_at = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
