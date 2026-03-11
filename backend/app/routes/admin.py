from datetime import date, timedelta

from flask import Blueprint, jsonify, session
from sqlalchemy import extract, func

from ..models import Producto, Usuario, Venta


admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/estadisticas")
def api_estadisticas():
    if "user_id" not in session or session.get("rol") != "admin":
        return jsonify({"error": "No autorizado"}), 403

    try:
        hoy = date.today()
        inicio_semana = hoy - timedelta(days=7)

        ventas_hoy = (
            Venta.query.with_entities(func.coalesce(func.sum(Venta.total), 0))
            .filter(func.date(Venta.fecha) == hoy)
            .scalar()
        )

        ventas_semana = (
            Venta.query.with_entities(func.coalesce(func.sum(Venta.total), 0))
            .filter(func.date(Venta.fecha) >= inicio_semana)
            .scalar()
        )

        ventas_mes = (
            Venta.query.with_entities(func.coalesce(func.sum(Venta.total), 0))
            .filter(extract("year", Venta.fecha) == hoy.year)
            .filter(extract("month", Venta.fecha) == hoy.month)
            .scalar()
        )

        ventas_totales = Venta.query.with_entities(func.coalesce(func.sum(Venta.total), 0)).scalar()

        ultimas_ventas = (
            Venta.query.join(Producto, Venta.producto_id == Producto.id)
            .join(Usuario, Venta.vendedor_id == Usuario.id)
            .with_entities(
                Venta.id,
                Producto.nombre,
                Venta.cantidad,
                Venta.total,
                Usuario.nombre.label("vendedor"),
                Venta.estado,
                Venta.fecha,
            )
            .order_by(Venta.fecha.desc())
            .limit(10)
            .all()
        )

        return jsonify(
            {
                "ventas_hoy": int(ventas_hoy or 0),
                "ventas_semana": int(ventas_semana or 0),
                "ventas_mes": int(ventas_mes or 0),
                "ventas_totales": int(ventas_totales or 0),
                "ultimas_ventas": [
                    {
                        "id": v.id,
                        "nombre": v.nombre,
                        "cantidad": v.cantidad,
                        "total": v.total,
                        "vendedor": v.vendedor,
                        "estado": v.estado,
                        "fecha": v.fecha.isoformat() if v.fecha else None,
                    }
                    for v in ultimas_ventas
                ],
                "ventas_por_vendedor": [],
                "top_productos": [],
            }
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
