from datetime import date
from flask_smorest import Blueprint
from ..extensions import db
from ..models import Certificado, AuditoriaFabrica
from ._roles import require_roles
blp=Blueprint("Alerts", __name__, description="Alertas")
THRESHOLDS=[90,60,30,15]

def cert_state(cert):
    today=date.today()
    if cert.fecha_vencimiento<today: return "vencido"
    if cert.ambito_certificado=="marca":
        audits = db.session.query(AuditoriaFabrica).filter_by(fabrica_id=cert.fabrica_id).all()
        if not any(a.fecha_auditoria<=today<=a.fecha_vencimiento for a in audits): return "suspendido"
    return "vigente"

@blp.route("/", methods=["GET"])
@require_roles("lectura")
def alerts():
    today=date.today(); res={"certificados":[], "auditorias":[], "sugerencias":[]}
    for c in db.session.query(Certificado).all():
        state=cert_state(c); days=(c.fecha_vencimiento-today).days
        if days<0 or any(days==t for t in THRESHOLDS) or state=="suspendido":
            res["certificados"].append({"id":c.id,"producto_id":c.producto_id,"tipo_certificacion_id":c.tipo_certificacion_id,"ambito":c.ambito_certificado,"fabrica_id":c.fabrica_id,"status":state,"vence_en_dias":days})
            if state=="suspendido": res["sugerencias"].append({"tipo":"programar_auditoria","certificado_id":c.id})
            if days<=30: res["sugerencias"].append({"tipo":"crear_tarea_renovar_certificado","certificado_id":c.id})
    for a in db.session.query(AuditoriaFabrica).all():
        days=(a.fecha_vencimiento-today).days
        if days<0 or any(days==t for t in THRESHOLDS):
            res["auditorias"].append({"id":a.id,"fabrica_id":a.fabrica_id,"vence_en_dias":days})
            if days<=30: res["sugerencias"].append({"tipo":"programar_auditoria","auditoria_id":a.id})
    return res
