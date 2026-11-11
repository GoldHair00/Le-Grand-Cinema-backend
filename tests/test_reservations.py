
from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models import Film, Room, Screening, Seat, User


def create_test_data():
    user = User(
        email="client@test.fr",
        password_hash="mot_de_passe_hash",
        first_name="Jean",
        last_name="Test",
        role="USER",
    )
    film = Film(
        title="Film de test",
        description="Description",
        duration_minutes=120,
    )
    room = Room(name="Salle 1")

    db.session.add_all([user, film, room])
    db.session.flush()

    screening = Screening(
        film_id=film.id,
        room_id=room.id,
        starts_at=datetime(2026, 11, 12, 20, 0),
        price=Decimal("10.00"),
    )
    seat = Seat(room_id=room.id, row_label="A", number=1)

    other_room = Room(name="Salle 2")
    db.session.add(other_room)
    db.session.flush()

    wrong_seat = Seat(
        room_id=other_room.id,
        row_label="A",
        number=1,
    )

    db.session.add_all([screening, seat, wrong_seat])
    db.session.commit()

    return user, screening, seat, wrong_seat


def test_reservation_success(client, app):
    with app.app_context():
        user, screening, seat, _ = create_test_data()
        screening_id = screening.id
        seat_id = seat.id
        user_id = user.id

    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(identity=str(user_id))

    response = client.post(
        "/api/reservations",
        json={"screening_id": screening_id, "seat_id": seat_id},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201


def test_reservation_requires_authentication(client, app):
    with app.app_context():
        _, screening, seat, _ = create_test_data()
        payload = {
            "screening_id": screening.id,
            "seat_id": seat.id,
        }

    response = client.post("/api/reservations", json=payload)

    assert response.status_code == 401


def test_cannot_reserve_same_seat_twice(client, app):
    with app.app_context():
        user, screening, seat, _ = create_test_data()
        user_id = user.id
        screening_id = screening.id
        seat_id = seat.id

        from flask_jwt_extended import create_access_token
        token = create_access_token(identity=str(user_id))

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"screening_id": screening_id, "seat_id": seat_id}

    first = client.post("/api/reservations", json=payload, headers=headers)
    second = client.post("/api/reservations", json=payload, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 409


def test_cannot_reserve_seat_from_another_room(client, app):
    with app.app_context():
        user, screening, _, wrong_seat = create_test_data()
        user_id = user.id
        screening_id = screening.id
        wrong_seat_id = wrong_seat.id

        from flask_jwt_extended import create_access_token
        token = create_access_token(identity=str(user_id))

    response = client.post(
        "/api/reservations",
        json={"screening_id": screening_id, "seat_id": wrong_seat_id},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
