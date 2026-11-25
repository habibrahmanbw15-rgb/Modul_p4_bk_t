from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError

from app.models.product_model import Category, Product, db
from app.utils.response_helper import error_response, fail_response, success_response

advanced_bp = Blueprint("advanced_bp", __name__)


@advanced_bp.route("/advanced/products", methods=["GET"])
def get_paginated_products():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    search = request.args.get("search", "", type=str).strip()

    if page < 1 or per_page < 1:
        return fail_response(
            {"pagination": "Parameter page dan per_page harus lebih besar dari 0"},
            400,
        )

    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    pagination = query.order_by(Product.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return success_response(
        data={
            "items": [item.to_dict() for item in pagination.items],
            "pagination": {
                "current_page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total,
            },
        },
        message="Data produk paginasi berhasil diambil",
        code=200,
    )


@advanced_bp.route("/advanced/products/transaction-demo", methods=["POST"])
def create_product_with_category_transaction():
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)

    data = request.get_json() or {}
    category_name = str(data.get("category_name", "")).strip()
    product_name = str(data.get("product_name", "")).strip()
    raw_price = data.get("price")

    errors = {}
    if not category_name:
        errors["category_name"] = "Field category_name wajib diisi"
    if not product_name:
        errors["product_name"] = "Field product_name wajib diisi"
    if raw_price is None or str(raw_price).strip() == "":
        errors["price"] = "Field price wajib diisi"

    if errors:
        return fail_response(errors, 400)

    try:
        price = float(raw_price)
        if price <= 0:
            return fail_response({"price": "Harga harus lebih besar dari 0"}, 400)

        cat = Category.query.filter(Category.name.ilike(category_name)).first()
        if not cat:
            cat = Category(name=category_name)
            db.session.add(cat)
            db.session.flush()  # Memperoleh cat.id sebelum commit akhir

        new_product = Product(
            name=product_name,
            price=price,
            category_id=cat.id,
        )
        db.session.add(new_product)
        db.session.commit()

        return success_response(
            data=new_product.to_dict(),
            message="Transaksi kategori dan produk berhasil disimpan",
            code=201,
        )
    except (SQLAlchemyError, ValueError, TypeError) as e:
        db.session.rollback()
        return error_response(f"Transaksi dibatalkan: {e!s}", 500)