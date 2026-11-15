
from app.extensions import db
from app.models import Film


def test_list_films_empty_returns_200(client):
    response = client.get("/api/films")

    assert response.status_code == 200
    assert response.get_json() == []


def test_list_films_returns_film_details(client):
    film = Film(
        title="Film de test",
        description="Description du film",
        duration_minutes=120,
    )
    db.session.add(film)
    db.session.commit()

    response = client.get("/api/films")

    assert response.status_code == 200
    data = response.get_json()

    assert len(data) == 1
    assert data[0]["title"] == "Film de test"
    assert data[0]["description"] == "Description du film"
    assert data[0]["duration_minutes"] == 120
