from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import Proveedor
from ..schemas import ProveedorSchema
from ._roles import require_roles

blp=Blueprint("Providers", __name__, description="Proveedores")

@blp.route("/", methods=["GET"])
@require_roles("lectura")
@blp.response(200, ProveedorSchema(many=True))
def list_providers():
    return db.session.scalars(db.select(Proveedor).order_by(Proveedor.id.desc())).all()

@blp.route("/", methods=["POST"])
@require_roles("editor","admin")
@blp.arguments(ProveedorSchema)
@blp.response(201, ProveedorSchema)
def create_provider(args):
    if db.session.scalar(db.select(Proveedor).filter_by(nombre=args.get("nombre"))): abort(409, message="El proveedor ya existe")
    prov=Proveedor(**args); db.session.add(prov); db.session.commit(); return prov
