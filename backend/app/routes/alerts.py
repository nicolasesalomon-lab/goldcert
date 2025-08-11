from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from ..models import Alert, Certificate
from ..schemas import AlertSchema

bp = Blueprint("alerts", __name__)
schema = AlertSchema(many=True)


@bp.get("/")
def list_alerts():
    today = datetime.utcnow().date()
    upcoming = today + timedelta(days=30)
    alerts = (
        Alert.query.join(Certificate)
        .filter(Certificate.fecha_vencimiento <= upcoming)
        .all()
    )
    return jsonify(schema.dump(alerts))
