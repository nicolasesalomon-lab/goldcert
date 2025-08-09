from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import User, TipoCertificacion

app=create_app()
with app.app_context():
    if not db.session.scalar(db.select(User).filter_by(email="admin@test.com")):
        db.session.add(User(email="admin@test.com", name="Admin", role="admin", password_hash=generate_password_hash("admin")))
    for n in ["SE","EE","ENACOM","INAL"]:
        if not db.session.scalar(db.select(TipoCertificacion).filter_by(nombre=n)):
            db.session.add(TipoCertificacion(nombre=n, descripcion=f"Tipo {n}"))
    db.session.commit()
    print("Seed ok")
