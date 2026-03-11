from flask import Blueprint, jsonify, request, session

from ..extensions import db
from ..models import Venta


sales_bp = Blueprint("sales", __name__)


@sales_bp.post("/ventas")
def api_registrar_venta():
    if "user_id" not in session:
        return jsonify({"error": "No autenticado"}), 401

    try:
        data = request.get_json(silent=True) or {}
        productos = data.get("productos", [])
        metodo_pago = data.get("metodo_pago", "efectivo")

        if not productos:
            return jsonify({"error": "No hay productos en la venta"}), 400

        total_general = 0
        ventas = []

        for item in productos:
            producto_id = item["producto_id"]
            cantidad = int(item["cantidad"])
            precio = int(item["precio"])
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
    except Exception as exc:
        db.session.rollback()
        return jsonify({"error": str(exc)}), 500
