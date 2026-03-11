"""Compat entrypoint kept for local scripts that still call App.py."""

from backend.wsgi import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
