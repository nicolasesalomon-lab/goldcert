from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import ModeloProveedor, ModeloProducto, Producto
from ..schemas import ModeloProveedorSchema, ModeloProductoSchema
from ._roles import require_roles

blp=Blueprint("Models", __name__, description="Modelos proveedor y producto")

@blp.route("/proveedor", methods=["GET"])
@require_roles("lectura")
@blp.response(200, ModeloProveedorSchema(many=True))
def list_modelo_proveedor():
    return db.session.scalars(db.select(ModeloProveedor).order_by(ModeloProveedor.id.desc())).all()

@blp.route("/proveedor", methods=["POST"])
@require_roles("editor","admin")
@blp.arguments(ModeloProveedorSchema)
@blp.response(201, ModeloProveedorSchema)
def create_modelo_proveedor(args):
    if not db.session.get(Producto, args["producto_id"]): abort(400, message="Producto inválido")
    m=ModeloProveedor(**args); db.session.add(m); db.session.commit(); return m

@blp.route("/producto", methods=["GET"])
@require_roles("lectura")
@blp.response(200, ModeloProductoSchema(many=True))
def list_modelo_producto():
    return db.session.scalars(db.select(ModeloProducto).order_by(ModeloProducto.id.desc())).all()

@blp.route("/producto", methods=["POST"])
@require_roles("editor","admin")
@blp.arguments(ModeloProductoSchema)
@blp.response(201, ModeloProductoSchema)
def create_modelo_producto(args):
    if not db.session.get(ModeloProveedor, args["modelo_proveedor_id"]): abort(400, message="ModeloProveedor inválido")
    m=ModeloProducto(**args); db.session.add(m); db.session.commit(); return m
