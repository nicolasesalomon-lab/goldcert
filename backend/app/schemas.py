from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from .models import User, Proveedor, Fabrica, AuditoriaFabrica, Producto, ModeloProveedor, ModeloProducto, VariacionEstetica, VariacionModelos, TipoCertificacion, Certificado, Attachment, DeclaracionJurada, DeclaracionModelos

class UserSchema(SQLAlchemyAutoSchema):
    class Meta: model=User; load_instance=False; include_fk=True; exclude=("password_hash",)

class ProveedorSchema(SQLAlchemyAutoSchema):
    class Meta: model=Proveedor; load_instance=False; include_fk=True

class FabricaSchema(SQLAlchemyAutoSchema):
    class Meta: model=Fabrica; load_instance=False; include_fk=True

class AuditoriaFabricaSchema(SQLAlchemyAutoSchema):
    class Meta: model=AuditoriaFabrica; load_instance=False; include_fk=True

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta: model=Producto; load_instance=False; include_fk=True

class ModeloProveedorSchema(SQLAlchemyAutoSchema):
    class Meta: model=ModeloProveedor; load_instance=False; include_fk=True

class ModeloProductoSchema(SQLAlchemyAutoSchema):
    class Meta: model=ModeloProducto; load_instance=False; include_fk=True

class VariacionEsteticaSchema(SQLAlchemyAutoSchema):
    class Meta: model=VariacionEstetica; load_instance=False; include_fk=True

class VariacionModelosSchema(SQLAlchemyAutoSchema):
    class Meta: model=VariacionModelos; load_instance=False; include_fk=True

class TipoCertificacionSchema(SQLAlchemyAutoSchema):
    class Meta: model=TipoCertificacion; load_instance=False; include_fk=True

class CertificadoSchema(SQLAlchemyAutoSchema):
    class Meta: model=Certificado; load_instance=False; include_fk=True

class AttachmentSchema(SQLAlchemyAutoSchema):
    class Meta: model=Attachment; load_instance=False; include_fk=True

class DeclaracionJuradaSchema(SQLAlchemyAutoSchema):
    class Meta: model=DeclaracionJurada; load_instance=False; include_fk=True

class DeclaracionModelosSchema(SQLAlchemyAutoSchema):
    class Meta: model=DeclaracionModelos; load_instance=False; include_fk=True

class LoginSchema(Schema):
    email=fields.Email(required=True); password=fields.String(required=True)

class RegisterSchema(Schema):
    email=fields.Email(required=True); password=fields.String(required=True); name=fields.String(); role=fields.String()
