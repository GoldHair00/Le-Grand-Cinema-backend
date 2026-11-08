import os

def _database_url():
    url = os.environ.get("DATABASE_URL", "sqlite:///cinema.db")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = _database_url()
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-secret-key-with-at-least-32-characters"
