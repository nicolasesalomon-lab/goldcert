import os
from flask_smorest import Blueprint, abort
from flask import current_app, request
from ..extensions import db
from ..models import Attachment
from ..schemas import AttachmentSchema
from ._roles import require_roles

blp=Blueprint("Attachments", __name__, description="Adjuntos")

@blp.route("/upload", methods=["POST"])
@require_roles("editor","admin")
@blp.response(201, AttachmentSchema)
def upload():
    if "file" not in request.files: abort(400, message="No file part")
    f=request.files["file"]; object_type=request.form.get("object_type"); object_id=request.form.get("object_id", type=int); category=request.form.get("category")
    if not object_type or not object_id or not category: abort(400, message="object_type, object_id y category son obligatorios")
    os.makedirs(current_app.config["UPLOAD_DIR"], exist_ok=True)
    save_path=os.path.join(current_app.config["UPLOAD_DIR"], f.filename); f.save(save_path)
    att=Attachment(object_type=object_type, object_id=object_id, category=category, filename=f.filename, path=save_path, mime_type=f.mimetype, size=os.path.getsize(save_path))
    db.session.add(att); db.session.commit(); return att
