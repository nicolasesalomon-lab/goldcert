from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import AuditoriaFabrica, Fabrica
from ..schemas import AuditoriaFabricaSchema
from ._roles import require_roles

blp=Blueprint("Audits", __name__, description="Auditorías de fábrica")

@blp.route("/", methods=["GET"])
@require_roles("lectura")
@blp.response(200, AuditoriaFabricaSchema(many=True))
def list_audits():
    return db.session.scalars(db.select(AuditoriaFabrica).order_by(AuditoriaFabrica.id.desc())).all()

@blp.route("/", methods=["POST"])
@require_roles("editor","admin")
@blp.arguments(AuditoriaFabricaSchema)
@blp.response(201, AuditoriaFabricaSchema)
def create_audit(args):
    if not db.session.get(Fabrica, args["fabrica_id"]): abort(400, message="Fábrica inválida")
    if args["fecha_vencimiento"] < args["fecha_auditoria"]: abort(400, message="Vencimiento no puede ser anterior a la auditoría")
    a=AuditoriaFabrica(**args); db.session.add(a); db.session.commit(); return a
