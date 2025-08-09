from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import Producto, Proveedor
from ..schemas import ProductoSchema
from ._roles import require_roles

blp=Blueprint("Products", __name__, description="Productos")

@blp.route("/", methods=["GET"])
@require_roles("lectura")
@blp.response(200, ProductoSchema(many=True))
def list_products():
    return db.session.scalars(db.select(Producto).order_by(Producto.id.desc())).all()

@blp.route("/", methods=["POST"])
@require_roles("editor","admin")
@blp.arguments(ProductoSchema)
@blp.response(201, ProductoSchema)
def create_product(args):
    if not db.session.get(Proveedor, args["proveedor_id"]): abort(400, message="Proveedor inválido")
    p=Producto(**args); db.session.add(p); db.session.commit(); return p
