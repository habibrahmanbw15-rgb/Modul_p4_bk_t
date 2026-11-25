from flask import Blueprint, request

from app.services.product_service import ProductService
from app.utils.response_helper import fail_response, success_response

product_bp = Blueprint("product_bp", __name__)


@product_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = ProductService.get_categories()
    return success_response(
        data={"categories": categories, "total": len(categories)},
        message="List kategori berhasil diambil",
        code=200,
    )

@product_bp.route("/categories/<int:categories_id>", methods=["GET"])
def get_categories_by_id(categories_id):
    categories = ProductService.get_categories_id(categories_id)
    if not categories:
        return fail_response(
            {"categories_id": f"categori dengan ID {categories_id} tidak ada"},404
        )
    return success_response(
        data=categories,message="detail categori ditemukan",code=200
    )

@product_bp.route("/items", methods=["POST"])
def create_item():
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)

    data = request.get_json()
    if not data:
        return fail_response({"body": "Body request tidak boleh kosong"}, 400)

    # Validasi field wajib
    required_fields = ["name", "price", "category_id"]
    missing = {field: f"Field {field} wajib diisi" for field in required_fields if field not in data}
    if missing:
        return fail_response(missing, 400)

    try:
        new_item = ProductService.create_item_data(data)
    except ValueError as e:
        return fail_response(
            {
                "price": "Format price tidak valid (harus angka)",
                "category_id": "Format category_id atau data tidak valid",
                "detail": str(e),
            },
            400,
        )

    return success_response(
        data=new_item, message="Data barang berhasil ditambahkan", code=201
    )

@product_bp.route("/items", methods=["GET"])
def get_items():
    category_query = request.args.get("category")
    min_price_query = request.args.get("min_price")

    try:
        filtered = ProductService.get_filtered_items(
            category_query, min_price_query
        )
    except ValueError:
        # Menggunakan fail_response dengan menyertakan nama field yang error
        return fail_response(
            {
                "category": "Query parameter harus integer",
                "min_price": "Query parameter harus angka valid",
            },
            400,
        )

    return success_response(
        data={"items": filtered, "total": len(filtered)},
        message="List barang berhasil diambil",
        code=200,
    )


@product_bp.route("/items/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    item = ProductService.get_item_detail(item_id)
    if not item:
        return fail_response(
            {"item_id": f"Barang dengan ID {item_id} tidak ditemukan"}, 404
        )
    return success_response(
        data=item, message="Detail barang ditemukan", code=200
    )


@product_bp.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)
        
    data = request.get_json()
    if not data:
        return fail_response({"body": "Body request tidak boleh kosong"}, 400)

    try:
        updated_item = ProductService.update_item_data(item_id, data)
        if not updated_item:
            return fail_response(
                {"item_id": f"Barang dengan ID {item_id} tidak ditemukan"}, 404
            )
    except ValueError:
        return fail_response(
            {
                "price": "Format price tidak valid (harus angka)",
                "category_id": "Format category_id tidak valid (harus angka)",
            },
            400,
        )

    return success_response(
        data=updated_item, message="Data barang berhasil diperbarui", code=200
    )


@product_bp.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    
    success = ProductService.remove_item(item_id)
    if not success:
        return fail_response(
            {"item_id": f"Barang dengan ID {item_id} tidak ditemukan"}, 404
        )

    return success_response(message="Data barang berhasil dihapus", code=200)

