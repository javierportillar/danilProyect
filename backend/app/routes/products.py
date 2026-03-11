from flask import Blueprint, jsonify
from sqlalchemy import case

from ..models import Producto


products_bp = Blueprint("products", __name__)


@products_bp.get("/productos")
def api_productos():
    order_categoria = case(
        (Producto.categoria == "hamburguesa", 1),
        (Producto.categoria == "perro", 2),
        (Producto.categoria == "bebida", 3),
        (Producto.categoria == "adicional", 4),
        else_=5,
    )

    productos = (
        Producto.query.order_by(order_categoria, Producto.nombre.asc())
        .with_entities(
            Producto.id,
            Producto.codigo,
            Producto.nombre,
            Producto.precio,
            Producto.categoria,
        )
        .all()
    )

    return jsonify(
        [
            {
                "id": p.id,
                "codigo": p.codigo,
                "nombre": p.nombre,
                "precio": p.precio,
                "categoria": p.categoria,
            }
            for p in productos
        ]
    )
