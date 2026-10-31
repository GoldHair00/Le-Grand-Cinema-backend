from app.models.user import User

VALID_USER = {
    "email": "marie@cinema.fr",
    "password": "MotDePasse123",
    "first_name": "Marie",
    "last_name": "Dupont",
}


def test_register_success(client):
    response = client.post("/api/auth/register", json=VALID_USER)

    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == "marie@cinema.fr"
    assert data["role"] == "USER"
    assert "id" in data


def test_register_never_returns_password(client):
    response = client.post("/api/auth/register", json=VALID_USER)

    assert "password" not in response.get_json()


def test_register_hashes_password(client):
    client.post("/api/auth/register", json=VALID_USER)

    user = User.query.filter_by(email="marie@cinema.fr").first()
    assert user.password_hash != VALID_USER["password"]


def test_register_duplicate_email_returns_409(client):
    client.post("/api/auth/register", json=VALID_USER)
    response = client.post("/api/auth/register", json=VALID_USER)

    assert response.status_code == 409
    assert response.get_json()["error"] == "email_already_used"


def test_register_invalid_email_returns_422(client):
    payload = {**VALID_USER, "email": "pas-un-email"}
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 422


def test_register_missing_field_returns_422(client):
    payload = {key: value for key, value in VALID_USER.items() if key != "last_name"}
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 422


def test_register_empty_body_returns_422(client):
    response = client.post("/api/auth/register", json={})

    assert response.status_code == 422
