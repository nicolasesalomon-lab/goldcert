from datetime import date, timedelta
from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import Certificado, TipoCertificacion, Producto, ModeloProveedor, Fabrica, AuditoriaFabrica, Attachment
from ..schemas import CertificadoSchema
from ._roles import require_roles

REQUIRED_BASE = {"TEST_REPORT","ETIQUETAS","MANUALES","MODELOS_MAP","OCC"}
REQUIRED_SE_TIPO_EXTRA = {"DECL_IDENTIDAD","VERIF_IDENTIDAD"}

def attachments_ok(producto_id:int, modelo_proveedor_id:int, required:set[str]):
    q = db.session.query(Attachment).filter(
        ((Attachment.object_type=="producto") & (Attachment.object_id==producto_id)) |
        ((Attachment.object_type=="modelo_proveedor") & (Attachment.object_id==modelo_proveedor_id))
    )
    cats={a.category for a in q}; missing=required - cats
    return (len(missing)==0, ", ".join(sorted(missing)))

def has_active_audit(fabrica_id:int, on_date:date)->bool:
    audits = db.session.scalars(db.select(AuditoriaFabrica).filter_by(fabrica_id=fabrica_id)).all()
    return any(a.fecha_auditoria<=on_date<=a.fecha_vencimiento for a in audits)

blp=Blueprint("Certificates", __name__, description="Certificados")

@blp.route("/", methods=["GET"])
@require_roles("lectura")
@blp.response(200, CertificadoSchema(many=True))
def list_certificates():
    return db.session.scalars(db.select(Certificado).order_by(Certificado.id.desc())).all()

@blp.route("/", methods=["POST"])
@require_roles("editor","admin")
@blp.arguments(CertificadoSchema)
@blp.response(201, CertificadoSchema)
def create_certificate(args):
    producto_id=args["producto_id"]; tipo_id=args["tipo_certificacion_id"]; modelo_proveedor_id=args["modelo_proveedor_id"]; fabrica_id=args["fabrica_id"]; ambito=args.get("ambito_certificado")
    if not db.session.get(Producto, producto_id): abort(400, message="Producto inválido")
    tipo=db.session.get(TipoCertificacion, tipo_id)
    if not tipo: abort(400, message="Tipo de certificación inválido")
    if not db.session.get(ModeloProveedor, modelo_proveedor_id): abort(400, message="ModeloProveedor inválido")
    if not db.session.get(Fabrica, fabrica_id): abort(400, message="Fábrica inválida")
    if tipo.nombre in ("ENACOM","INAL"):
        if ambito is not None: abort(400, message="ENACOM/INAL no usan ámbito; debe ser null")
    else:
        if ambito not in ("tipo","marca"): abort(400, message="Ámbito debe ser 'tipo' o 'marca' para SE/EE")
    req=set(REQUIRED_BASE)
    if tipo.nombre=="SE" and ambito=="tipo": req|=REQUIRED_SE_TIPO_EXTRA
    ok, missing=attachments_ok(producto_id, modelo_proveedor_id, req)
    if not ok: abort(400, message=f"Faltan adjuntos requeridos: {missing}")
    fecha_emision=args.get("fecha_emision") or date.today()
    if ambito=="marca" and not has_active_audit(fabrica_id, fecha_emision): abort(400, message="Requiere auditoría vigente al emitir")
    if not args.get("fecha_vencimiento"):
        args["fecha_vencimiento"]=fecha_emision + timedelta(days=365*2)
    existing = db.session.scalars(db.select(Certificado).where(
        (Certificado.producto_id==producto_id) &
        (Certificado.tipo_certificacion_id==tipo_id) &
        (Certificado.ambito_certificado==ambito) &
        (Certificado.modelo_proveedor_id==modelo_proveedor_id) &
        (Certificado.fabrica_id==fabrica_id) &
        (Certificado.status=="vigente") &
        (Certificado.fecha_vencimiento >= fecha_emision)
    )).first()
    if existing: abort(409, message="Ya existe un certificado vigente para esa combinación")
    status="vigente" if args["fecha_vencimiento"]>=fecha_emision else "vencido"
    args["status"]=status
    cert=Certificado(**args); db.session.add(cert); db.session.commit(); return cert
