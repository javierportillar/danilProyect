from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import db, migrate
from .routes import register_routes
from .seed import seed_defaults


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    if app.config.get("ENV") == "production":
        secret = app.config.get("SECRET_KEY", "")
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if not secret or "change-this" in secret or "replace-with" in secret:
            raise RuntimeError("SECRET_KEY is not set for production.")
        if not db_uri or db_uri.startswith("sqlite"):
            raise RuntimeError("DATABASE_URL must be a PostgreSQL URL in production.")

    if app.config.get("TRUST_PROXY"):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(
        app,
        origins=app.config["CORS_ORIGINS"],
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    register_routes(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/api/health")
    def api_health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(_):
        return jsonify({"error": "Error interno del servidor"}), 500

    @app.cli.command("seed")
    def seed_command():
        """Insert default users and products."""
        seed_defaults()
        print("Seed completed")

    @app.cli.command("init-db")
    def init_db_command():
        """Create tables and seed defaults (useful for first boot)."""
        db.create_all()
        seed_defaults()
        print("Database initialized")

    return app
