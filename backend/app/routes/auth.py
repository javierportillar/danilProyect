from flask import Blueprint, current_app, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models import Usuario


auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/test")
def api_test():
    return jsonify({"message": "API funcionando", "status": "ok"})


@auth_bp.post("/login")
def api_login():
    try:
        data = request.get_json(silent=True) or {}
        username = data.get("username", "")
        password = data.get("password", "")

        user = Usuario.query.filter_by(username=username).first()
        if not user:
            return jsonify({"success": False, "error": "Credenciales inválidas"}), 401

        stored_password = user.password or ""
        valid_password = False

        if stored_password.startswith("pbkdf2:") or stored_password.startswith("scrypt:"):
            valid_password = check_password_hash(stored_password, password)
        else:
            # Backward compatibility for legacy plain-text users.
            valid_password = stored_password == password
            if valid_password:
                user.password = generate_password_hash(password)
                db.session.commit()

        if not valid_password:
            return jsonify({"success": False, "error": "Credenciales inválidas"}), 401

        session["user_id"] = user.id
        session["username"] = user.username
        session["rol"] = user.rol
        session["nombre"] = user.nombre
        session.permanent = True

        return jsonify(
            {
                "success": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "rol": user.rol,
                    "nombre": user.nombre,
                },
            }
        )
    except Exception:
        current_app.logger.exception("Error in /api/login")
        return jsonify({"success": False, "error": "Error interno del servidor"}), 500


@auth_bp.get("/session")
def api_session():
    if "user_id" in session:
        return jsonify(
            {
                "authenticated": True,
                "user": {
                    "id": session["user_id"],
                    "username": session["username"],
                    "rol": session["rol"],
                    "nombre": session["nombre"],
                },
            }
        )
    return jsonify({"authenticated": False})


@auth_bp.post("/logout")
def api_logout():
    session.clear()
    return jsonify({"success": True})
