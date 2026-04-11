from datetime import datetime

from .extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(30), nullable=False)
    nombre = db.Column(db.String(120))


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(40))
    activo = db.Column(db.Boolean, default=True, nullable=False)


class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    estado = db.Column(db.String(40), default="pendiente")
    pago = db.Column(db.String(40), default="efectivo")

    producto = db.relationship("Producto", backref="ventas")
    vendedor = db.relationship("Usuario", backref="ventas")
