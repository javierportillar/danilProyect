from .admin import admin_bp
from .auth import auth_bp
from .products import products_bp
from .sales import sales_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(products_bp, url_prefix="/api")
    app.register_blueprint(sales_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
