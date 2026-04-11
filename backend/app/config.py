import os
from datetime import timedelta


def _normalize_database_url(url: str) -> str:
    """Render/Heroku may expose postgres://, SQLAlchemy expects postgresql://"""
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = _to_bool(os.getenv("FLASK_DEBUG"), default=False)

    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

    raw_database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_DATABASE_URI = _normalize_database_url(raw_database_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
    }

    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

    SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "urbanfood_session")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = _to_bool(os.getenv("SESSION_COOKIE_SECURE"), default=False)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=int(os.getenv("SESSION_MAX_AGE_HOURS", "12")))

    TRUST_PROXY = _to_bool(os.getenv("TRUST_PROXY"), default=True)
