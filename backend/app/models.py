from datetime import date, datetime, timedelta
from sqlalchemy import func, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .extensions import db

class BaseModel(db.Model):
    __abstract__=True
    id: Mapped[int]=mapped_column(primary_key=True)
    created_at: Mapped[datetime]=mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime]=mapped_column(default=func.now(), onupdate=func.now(), nullable=False)

class User(BaseModel):
    __tablename__="users"
    email=db.Column(db.String(255), unique=True, nullable=False)
    password_hash=db.Column(db.String(255), nullable=False)
    name=db.Column(db.String(120), nullable=False, default="User")
    role=db.Column(db.String(20), nullable=False, default="admin") # admin|editor|lectura

class Proveedor(BaseModel):
    __tablename__="proveedores"
    nombre=db.Column(db.String(200), nullable=False, unique=True)
    contacto_email=db.Column(db.String(255))
    contacto_telefono=db.Column(db.String(50))
    fabricas=relationship("Fabrica", back_populates="proveedor")

class Fabrica(BaseModel):
    __tablename__="fabricas"
    proveedor_id=mapped_column(ForeignKey("proveedores.id"), nullable=False)
    direccion=db.Column(db.String(255))
    proveedor=relationship("Proveedor", back_populates="fabricas")
    auditorias=relationship("AuditoriaFabrica", back_populates="fabrica")

class AuditoriaFabrica(BaseModel):
    __tablename__="auditorias_fabrica"
    fabrica_id=mapped_column(ForeignKey("fabricas.id"), nullable=False)
    fecha_auditoria=db.Column(db.Date, nullable=False)
    fecha_vencimiento=db.Column(db.Date, nullable=False)
    fabrica=relationship("Fabrica", back_populates="auditorias")
    @property
    def vigente(self)->bool:
        today=date.today(); return self.fecha_auditoria<=today<=self.fecha_vencimiento

class Producto(BaseModel):
    __tablename__="productos"
    nombre=db.Column(db.String(200), nullable=False)
    categoria=db.Column(db.String(120))
    marca=db.Column(db.String(120))
    origen=db.Column(db.String(120))
    proveedor_id=mapped_column(ForeignKey("proveedores.id"), nullable=False)

class ModeloProveedor(BaseModel):
    __tablename__="modelos_proveedor"
    producto_id=mapped_column(ForeignKey("productos.id"), nullable=False)
    codigo_proveedor=db.Column(db.String(120), nullable=False)
    __table_args__=(UniqueConstraint("producto_id","codigo_proveedor", name="uq_producto_codigo_proveedor"),)

class ModeloProducto(BaseModel):
    __tablename__="modelos_producto"
    modelo_proveedor_id=mapped_column(ForeignKey("modelos_proveedor.id"), nullable=False)
    codigo_goldmund=db.Column(db.String(120), nullable=False)
    __table_args__=(UniqueConstraint("modelo_proveedor_id","codigo_goldmund", name="uq_modelo_codigo_goldmund"),)

class VariacionEstetica(BaseModel):
    __tablename__="variaciones_esteticas"
    producto_id=mapped_column(ForeignKey("productos.id"), nullable=False)
    nombre_grupo=db.Column(db.String(200), nullable=False)

class VariacionModelos(BaseModel):
    __tablename__="variacion_modelos"
    variacion_id=mapped_column(ForeignKey("variaciones_esteticas.id"), nullable=False)
    modelo_producto_id=mapped_column(ForeignKey("modelos_producto.id"), nullable=False)

class TipoCertificacion(BaseModel):
    __tablename__="tipos_certificacion"
    nombre=db.Column(db.String(50), nullable=False, unique=True)
    descripcion=db.Column(db.Text)

class Certificado(BaseModel):
    __tablename__="certificados"
    producto_id=mapped_column(ForeignKey("productos.id"), nullable=False)
    tipo_certificacion_id=mapped_column(ForeignKey("tipos_certificacion.id"), nullable=False)
    ambito_certificado=db.Column(db.String(10), nullable=True) # 'tipo'|'marca'|NULL
    modelo_proveedor_id=mapped_column(ForeignKey("modelos_proveedor.id"), nullable=False)
    fabrica_id=mapped_column(ForeignKey("fabricas.id"), nullable=False)
    tipo_ensayo=db.Column(db.String(120))
    test_report=db.Column(db.String(200))
    fecha_emision=db.Column(db.Date, nullable=False)
    fecha_vencimiento=db.Column(db.Date, nullable=False)
    status=db.Column(db.String(20), nullable=False, default="draft")
    __table_args__=(CheckConstraint("ambito_certificado in ('tipo','marca') or ambito_certificado is null", name="ck_ambito"),)

class Attachment(BaseModel):
    __tablename__="attachments"
    object_type=db.Column(db.String(40), nullable=False) # certificado|auditoria|producto|modelo_proveedor|djc
    object_id=db.Column(db.Integer, nullable=False)
    category=db.Column(db.String(40), nullable=False) # TEST_REPORT|ETIQUETAS|MANUALES|MODELOS_MAP|DECL_IDENTIDAD|VERIF_IDENTIDAD|OCC|AUDIT_REPORT
    filename=db.Column(db.String(255), nullable=False)
    path=db.Column(db.String(500), nullable=False)
    mime_type=db.Column(db.String(120))
    size=db.Column(db.Integer)

class DeclaracionJurada(BaseModel):
    __tablename__="declaraciones_juradas"
    numero=db.Column(db.String(50), nullable=False, unique=True)
    fecha_generacion=db.Column(db.Date, nullable=False)
    plantilla=db.Column(db.Text)

class DeclaracionModelos(BaseModel):
    __tablename__="declaracion_modelos"
    declaracion_id=mapped_column(ForeignKey("declaraciones_juradas.id"), nullable=False)
    modelo_producto_id=mapped_column(ForeignKey("modelos_producto.id"), nullable=False)
