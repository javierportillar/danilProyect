from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db, migrate
from .routes import register_routes
from .seed import seed_defaults


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    register_routes(app)

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
