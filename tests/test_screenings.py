from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models import Film, Room, Screening, Seat, Reservation

def _create_screening(title="Jazz Night", starts_at=datetime(2026, 7, 10, 20, 0)):

    film = Film(title=title, duration_minutes=100)
    room = Room(name=f"Salle {title}")
    db.session.add_all([film, room])
    db.session.commit()
    screening = Screening(
        film_id=film.id, room_id=room.id, starts_at=starts_at, price=Decimal("9.50")
    )
    db.session.add(screening)
    db.session.commit()
    return screening


def test_list_screenings_empty_returns_200(client):

    response = client.get("/api/screenings")

    assert response.status_code == 200
    assert response.get_json() == []


def test_list_screenings_returns_film_title(client):

    _create_screening()
    response = client.get("/api/screenings")

    assert response.status_code == 200
    assert response.get_json()[0]["film_title"] == "Jazz Night"


def test_list_screenings_filters_by_date(client):

    _create_screening("Jazz Night", datetime(2026, 7, 10, 20, 0))
    _create_screening("Blues Night", datetime(2026, 7, 11, 20, 0))
    response = client.get("/api/screenings?date=2026-07-10")

    titles = [item["film_title"] for item in response.get_json()]
    assert titles == ["Jazz Night"]


def test_list_screenings_filters_by_film_id(client):

    first = _create_screening("Jazz Night")
    _create_screening("Blues Night")
    response = client.get(f"/api/screenings?film_id={first.film_id}")

    titles = [item["film_title"] for item in response.get_json()]
    assert titles == ["Jazz Night"]


def test_list_screenings_invalid_date_returns_422(client):

    response = client.get("/api/screenings?date=pas-une-date")

    assert response.status_code == 422

def test_list_screening_seats_returns_available_seats(client):

    screening = _create_screening()
    seat = Seat(
        room_id=screening.room_id,
        row_label="A",
        number=1,
    )
    db.session.add(seat)
    db.session.commit()

    response = client.get(
        f"/api/screenings/{screening.id}/seats"
    )

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": seat.id,
            "row": "A",
            "number": 1,
            "available": True,
        }
    ]


def test_list_screening_seats_returns_reserved_status(client, app):

    from app.models import User

    screening = _create_screening()
    seat = Seat(
        room_id=screening.room_id,
        row_label="A",
        number=1,
    )
    user = User(
        email="reservation@test.fr",
        password_hash="mot_de_passe_hash",
        first_name="Jean",
        last_name="Test",
        role="USER",
    )
    db.session.add_all([seat, user])
    db.session.commit()

    reservation = Reservation(
        user_id=user.id,
        screening_id=screening.id,
        seat_id=seat.id,
    )
    db.session.add(reservation)
    db.session.commit()

    response = client.get(
        f"/api/screenings/{screening.id}/seats"
    )

    assert response.status_code == 200
    assert response.get_json()[0]["available"] is False


def test_list_screening_seats_unknown_screening_returns_404(client):

    response = client.get("/api/screenings/9999/seats")

    assert response.status_code == 404


