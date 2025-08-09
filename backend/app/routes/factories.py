from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import Fabrica, Proveedor
from ..schemas import FabricaSchema
from ._roles import require_roles

blp=Blueprint("Factories", __name__, description="Fábricas")

@blp.route("/", methods=["GET"])
@require_roles("lectura")
@blp.response(200, FabricaSchema(many=True))
def list_factories():
    return db.session.scalars(db.select(Fabrica).order_by(Fabrica.id.desc())).all()

@blp.route("/", methods=["POST"])
@require_roles("editor","admin")
@blp.arguments(FabricaSchema)
@blp.response(201, FabricaSchema)
def create_factory(args):
    if not db.session.get(Proveedor, args["proveedor_id"]): abort(400, message="Proveedor inválido")
    fab=Fabrica(**args); db.session.add(fab); db.session.commit(); return fab
