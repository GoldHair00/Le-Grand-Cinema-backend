from tests.test_auth_register import VALID_USER


def _register(client):
    client.post("/api/auth/register", json=VALID_USER)


def _login(client, email, password):
    return client.post("/api/auth/login", json={"email": email, "password": password})


def test_login_success_returns_token_and_role(client):
    _register(client)
    response = _login(client, VALID_USER["email"], VALID_USER["password"])

    assert response.status_code == 200
    data = response.get_json()
    assert data["access_token"]
    assert data["role"] == "USER"
    assert "password" not in data


def test_login_wrong_password_returns_401(client):
    _register(client)
    response = _login(client, VALID_USER["email"], "MauvaisMotDePasse")

    assert response.status_code == 401
    assert response.get_json()["error"] == "invalid_credentials"


def test_login_unknown_email_gives_same_answer_as_wrong_password(client):
    _register(client)
    wrong_password = _login(client, VALID_USER["email"], "MauvaisMotDePasse")
    unknown_email = _login(client, "inconnu@cinema.fr", "MotDePasse123")

    assert unknown_email.status_code == 401
    assert unknown_email.get_json() == wrong_password.get_json()


def test_login_missing_password_returns_422(client):
    response = client.post("/api/auth/login", json={"email": VALID_USER["email"]})

    assert response.status_code == 422
    