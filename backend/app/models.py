from datetime import date
from . import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(120))
    marca = db.Column(db.String(120))
    origen = db.Column(db.String(120))

    certificates = db.relationship("Certificate", backref="producto", lazy=True)


class Certificate(db.Model):
    __tablename__ = "certificate"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    fecha_emision = db.Column(db.Date, nullable=False, default=date.today)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    documento_url = db.Column(db.String(255))

    alerts = db.relationship("Alert", backref="certificado", lazy=True)


class Alert(db.Model):
    __tablename__ = "alert"

    id = db.Column(db.Integer, primary_key=True)
    certificado_id = db.Column(
        db.Integer, db.ForeignKey("certificate.id"), nullable=False
    )
    tipo = db.Column(db.String(50))
    fecha_generada = db.Column(db.Date, nullable=False, default=date.today)
    enviado = db.Column(db.Boolean, default=False)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default="user")
