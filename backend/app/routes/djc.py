from datetime import date
from io import BytesIO
from flask_smorest import Blueprint, abort
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from ..extensions import db
from ..models import DeclaracionJurada, DeclaracionModelos, ModeloProducto
from ..schemas import DeclaracionJuradaSchema
from ._roles import require_roles

blp=Blueprint("DJC", __name__, description="Declaración Jurada")

def next_num():
    year=date.today().year; prefix=f"DJC-{year}-"
    count=db.session.query(DeclaracionJurada).filter(DeclaracionJurada.numero.like(f"{prefix}%")).count()
    return f"{prefix}{count+1:04d}"

@blp.route("/", methods=["POST"])
@require_roles("editor","admin")
@blp.response(201, DeclaracionJuradaSchema)
def create():
    djc=DeclaracionJurada(numero=next_num(), fecha_generacion=date.today(), plantilla="default")
    db.session.add(djc); db.session.commit(); return djc

@blp.route("/<int:djc_id>/add-modelo/<int:modelo_id>", methods=["POST"])
@require_roles("editor","admin")
def add_modelo(djc_id, modelo_id):
    if not db.session.get(DeclaracionJurada, djc_id): abort(404, message="DJC no encontrada")
    if not db.session.get(ModeloProducto, modelo_id): abort(404, message="ModeloProducto no encontrado")
    dm=DeclaracionModelos(declaracion_id=djc_id, modelo_producto_id=modelo_id)
    db.session.add(dm); db.session.commit(); return {"ok":True}

@blp.route("/<int:djc_id>/pdf", methods=["GET"])
@require_roles("lectura")
def pdf(djc_id):
    djc=db.session.get(DeclaracionJurada, djc_id)
    if not djc: abort(404, message="DJC no encontrada")
    modelos=db.session.query(DeclaracionModelos).filter_by(declaracion_id=djc_id).all()
    buf=BytesIO(); p=canvas.Canvas(buf, pagesize=A4); w,h=A4; y=h-50
    p.setFont("Helvetica-Bold",14); p.drawString(50,y,f"Declaración Jurada {djc.numero}")
    y-=20; p.setFont("Helvetica",11); p.drawString(50,y,f"Fecha: {djc.fecha_generacion.isoformat()}"); y-=30
    p.setFont("Helvetica-Bold",12); p.drawString(50,y,"Modelos incluidos:"); y-=20; p.setFont("Helvetica",11)
    for m in modelos:
        p.drawString(60,y,f"- ModeloProducto ID {m.modelo_producto_id}"); y-=16
        if y<80: p.showPage(); y=h-50
    p.showPage(); p.save(); buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f"{djc.numero}.pdf", mimetype="application/pdf")
