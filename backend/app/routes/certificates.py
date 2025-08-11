from datetime import datetime
from flask import Blueprint, request, jsonify
from ..models import Certificate, db
from ..schemas import CertificateSchema

bp = Blueprint("certificates", __name__)
schema = CertificateSchema()
schemas = CertificateSchema(many=True)


@bp.get("/")
def list_certificates():
    query = Certificate.query
    if request.args.get("expired") == "true":
        today = datetime.utcnow().date()
        query = query.filter(Certificate.fecha_vencimiento < today)
    return jsonify(schemas.dump(query.all()))


@bp.post("/")
def create_certificate():
    cert = schema.load(request.get_json(), session=db.session)
    db.session.add(cert)
    db.session.commit()
    return schema.dump(cert), 201


@bp.get("/<int:cert_id>")
def get_certificate(cert_id: int):
    cert = Certificate.query.get_or_404(cert_id)
    return schema.dump(cert)


@bp.put("/<int:cert_id>")
def update_certificate(cert_id: int):
    cert = Certificate.query.get_or_404(cert_id)
    cert = schema.load(
        request.get_json(), instance=cert, session=db.session, partial=True
    )
    db.session.commit()
    return schema.dump(cert)


@bp.delete("/<int:cert_id>")
def delete_certificate(cert_id: int):
    cert = Certificate.query.get_or_404(cert_id)
    db.session.delete(cert)
    db.session.commit()
    return "", 204
