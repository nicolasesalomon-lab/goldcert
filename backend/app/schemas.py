from . import ma
from .models import Product, Certificate, Alert, User


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True

    id = ma.auto_field()
    nombre = ma.auto_field()
    categoria = ma.auto_field()
    marca = ma.auto_field()
    origen = ma.auto_field()


class CertificateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Certificate
        load_instance = True

    id = ma.auto_field()
    producto_id = ma.auto_field()
    fecha_emision = ma.auto_field()
    fecha_vencimiento = ma.auto_field()
    documento_url = ma.auto_field()


class AlertSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Alert
        load_instance = True

    id = ma.auto_field()
    certificado_id = ma.auto_field()
    tipo = ma.auto_field()
    fecha_generada = ma.auto_field()
    enviado = ma.auto_field()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field()
    email = ma.auto_field()
    rol = ma.auto_field()
