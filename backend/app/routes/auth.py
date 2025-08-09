import json
from flask_smorest import Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import db
from ..models import User
from ..schemas import LoginSchema, RegisterSchema, UserSchema

blp=Blueprint("Auth", __name__, description="Auth")

@blp.route("/register", methods=["POST"])
@blp.arguments(RegisterSchema)
@blp.response(201, UserSchema)
def register(args):
    if db.session.scalar(db.select(User).filter_by(email=args["email"])): abort(409, message="Email already registered")
    user=User(email=args["email"], name=args.get("name","User"), role=args.get("role","editor"), password_hash=generate_password_hash(args["password"]))
    db.session.add(user); db.session.commit(); return user

@blp.route("/login", methods=["POST"])
@blp.arguments(LoginSchema)
def login(args):
    user=db.session.scalar(db.select(User).filter_by(email=args["email"]))
    if not user or not check_password_hash(user.password_hash, args["password"]): abort(401, message="Invalid credentials")
    identity=json.dumps({"id":user.id,"email":user.email,"role":user.role})
    token=create_access_token(identity=identity); return {"access_token":token}

@blp.route("/me", methods=["GET"])
@jwt_required()
@blp.response(200, UserSchema)
def me():
    ident_raw=get_jwt_identity()
    try: ident=json.loads(ident_raw)
    except Exception: abort(401, message="Invalid token identity payload")
    user=db.session.get(User, ident.get("id")); return user
