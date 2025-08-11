from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import User, db
from ..schemas import UserSchema

bp = Blueprint("auth", __name__)
user_schema = UserSchema()


@bp.post("/register")
def register():
    data = request.get_json()
    user = User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        rol=data.get("rol", "user"),
    )
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201


@bp.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not check_password_hash(user.password_hash, data.get("password")):
        return {"message": "invalid credentials"}, 401
    token = create_access_token(identity=user.id)
    return {"access_token": token}


@bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return user_schema.dump(user)
