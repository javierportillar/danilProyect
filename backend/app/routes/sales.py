from flask import Blueprint, current_app, jsonify, request, session

from ..extensions import db
from ..models import Producto, Venta


sales_bp = Blueprint("sales", __name__)

ALLOWED_PAYMENT_METHODS = {"efectivo", "transferencia", "tarjeta"}


@sales_bp.post("/ventas")
def api_registrar_venta():
    if "user_id" not in session:
        return jsonify({"error": "No autenticado"}), 401

    try:
        data = request.get_json(silent=True) or {}
        productos = data.get("productos", [])
        metodo_pago = data.get("metodo_pago", "efectivo")

        if metodo_pago not in ALLOWED_PAYMENT_METHODS:
            return jsonify({"error": "Método de pago inválido"}), 400

        if not isinstance(productos, list) or not productos:
            return jsonify({"error": "No hay productos en la venta"}), 400

        total_general = 0
        ventas = []

        for item in productos:
            producto_id = item.get("producto_id")
            cantidad = int(item.get("cantidad", 0))

            if not producto_id or cantidad <= 0:
                return jsonify({"error": "Producto o cantidad inválida"}), 400

            producto = Producto.query.filter_by(id=producto_id, activo=True).first()
            if not producto:
                return jsonify({"error": f"Producto inválido o inactivo: {producto_id}"}), 400

            precio = int(producto.precio)
            total = precio * cantidad
            total_general += total

            venta = Venta(
                producto_id=producto_id,
                cantidad=cantidad,
                precio_unitario=precio,
                total=total,
                vendedor_id=session["user_id"],
                estado="pendiente",
                pago=metodo_pago,
            )
            db.session.add(venta)
            ventas.append(venta)

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "venta_id": ventas[0].id if ventas else None,
                "total": total_general,
                "cantidad_productos": len(productos),
            }
        )
    except ValueError:
        db.session.rollback()
        return jsonify({"error": "Formato numérico inválido"}), 400
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Error in /api/ventas")
        return jsonify({"error": "Error interno del servidor"}), 500
