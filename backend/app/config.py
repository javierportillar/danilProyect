import os


def _normalize_database_url(url: str) -> str:
    """Render/Heroku may expose postgres://, SQLAlchemy expects postgresql://"""
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

    raw_database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_DATABASE_URI = _normalize_database_url(raw_database_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
