"""Migrate data from legacy SQLite file into current DATABASE_URL.

Usage:
  SQLITE_PATH=./database.db DATABASE_URL=postgresql://... python backend/scripts/migrate_sqlite_to_postgres.py
"""

import os
import sqlite3
from datetime import datetime

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Producto, Usuario, Venta


def _read_sqlite_rows(path: str, table: str):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()
    return rows


def main():
    sqlite_path = os.getenv("SQLITE_PATH", "database.db")
    if not os.path.exists(sqlite_path):
        raise FileNotFoundError(f"SQLite file not found: {sqlite_path}")

    app = create_app()
    with app.app_context():
        db.create_all()

        if Usuario.query.count() or Producto.query.count() or Venta.query.count():
            raise RuntimeError("Target database is not empty. Abort to avoid duplicates.")

        sqlite_users = _read_sqlite_rows(sqlite_path, "usuarios")
        sqlite_products = _read_sqlite_rows(sqlite_path, "productos")
        sqlite_sales = _read_sqlite_rows(sqlite_path, "ventas")

        for row in sqlite_users:
            db.session.add(
                Usuario(
                    id=row["id"],
                    username=row["username"],
                    password=generate_password_hash(row["password"]),
                    rol=row["rol"],
                    nombre=row["nombre"],
                )
            )

        for row in sqlite_products:
            db.session.add(
                Producto(
                    id=row["id"],
                    codigo=row["codigo"],
                    nombre=row["nombre"],
                    precio=row["precio"],
                    categoria=row["categoria"],
                )
            )

        for row in sqlite_sales:
            fecha = row["fecha"]
            if isinstance(fecha, str):
                fecha = datetime.fromisoformat(fecha.replace("Z", "+00:00"))

            db.session.add(
                Venta(
                    id=row["id"],
                    fecha=fecha,
                    producto_id=row["producto_id"],
                    cantidad=row["cantidad"],
                    precio_unitario=row["precio_unitario"],
                    total=row["total"],
                    vendedor_id=row["vendedor_id"],
                    estado=row["estado"],
                    pago=row["pago"],
                )
            )

        db.session.commit()
        print("Migration completed successfully")


if __name__ == "__main__":
    main()
