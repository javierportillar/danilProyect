from werkzeug.security import generate_password_hash

from .extensions import db
from .models import Producto, Usuario


DEFAULT_USERS = [
    ("admin", "admin123", "admin", "Administrador"),
    ("vendedor1", "vende123", "vendedor", "Vendedor 1"),
    ("vendedor2", "vende456", "vendedor", "Vendedor 2"),
]

DEFAULT_PRODUCTS = [
    ("MINIH", "Mini H", 5500, "hamburguesa"),
    ("HSINT", "H Sin T", 10000, "hamburguesa"),
    ("HCONT", "H Cont", 11000, "hamburguesa"),
    ("HDOBLE", "H Doble", 18000, "hamburguesa"),
    ("PSINT", "P Sin T", 8000, "perro"),
    ("PCONT", "P Cont", 9000, "perro"),
    ("COCA", "Coca-Cola", 3000, "bebida"),
    ("CUATRO", "Cuatro", 3000, "bebida"),
    ("JUGOS", "Jugos", 2000, "bebida"),
    ("TE", "Té", 2000, "bebida"),
    ("AGUA", "Agua", 2000, "bebida"),
    ("AQUESO", "A Queso", 1000, "adicional"),
    ("ATOCINO", "A Tocino", 1000, "adicional"),
]


def seed_defaults() -> None:
    if Usuario.query.count() == 0:
        for username, password, rol, nombre in DEFAULT_USERS:
            db.session.add(
                Usuario(
                    username=username,
                    password=generate_password_hash(password),
                    rol=rol,
                    nombre=nombre,
                )
            )

    if Producto.query.count() == 0:
        for codigo, nombre, precio, categoria in DEFAULT_PRODUCTS:
            db.session.add(
                Producto(
                    codigo=codigo,
                    nombre=nombre,
                    precio=precio,
                    categoria=categoria,
                )
            )

    db.session.commit()
