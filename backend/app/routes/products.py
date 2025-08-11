from flask import Blueprint, request, jsonify
from ..models import Product, db
from ..schemas import ProductSchema

bp = Blueprint("products", __name__)
schema = ProductSchema()
schemas = ProductSchema(many=True)


@bp.get("/")
def list_products():
    return jsonify(schemas.dump(Product.query.all()))


@bp.post("/")
def create_product():
    product = schema.load(request.get_json(), session=db.session)
    db.session.add(product)
    db.session.commit()
    return schema.dump(product), 201


@bp.get("/<int:product_id>")
def get_product(product_id: int):
    product = Product.query.get_or_404(product_id)
    return schema.dump(product)


@bp.put("/<int:product_id>")
def update_product(product_id: int):
    product = Product.query.get_or_404(product_id)
    product = schema.load(
        request.get_json(), instance=product, session=db.session, partial=True
    )
    db.session.commit()
    return schema.dump(product)


@bp.delete("/<int:product_id>")
def delete_product(product_id: int):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return "", 204
