from app.services.product_service import ProductService
from flask import Blueprint, jsonify, request

product_bp = Blueprint("product_bp", __name__)


@product_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = ProductService.get_categories()
    return (
        jsonify(
            {
                "status": "success",
                "total": len(categories),
                "message": "List kategori berhasil diambil",
                "data": categories,
            }
        ),
        200,
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
        return (
            jsonify({
                "status": "fail",
                "message": (
                    "Query parameter 'category' harus integer dan 'min_price'"
                    " harus angka valid."
                ),
            }),
            400,
        )

    return (
        jsonify({
            "status": "success",
            "total": len(filtered),
            "message": "List barang berhasil diambil",
            "data": filtered,
        }),
        200,
    )


@product_bp.route("/items/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    item = ProductService.get_item_detail(item_id)
    if not item:
        return (
            jsonify({
                "status": "fail",
                "message": f"Barang dengan ID {item_id} tidak ditemukan",
            }),
            404,
        )
    return (
        jsonify({
            "status": "success",
            "message": "Detail barang ditemukan",
            "data": item,
        }),
        200,
    )


@product_bp.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    if not data:
        return (
            jsonify({"status": "fail", "message": "Body request tidak boleh kosong"}),
            400,
        )

    try:
        updated_item = ProductService.update_item_data(item_id, data)
        if not updated_item:
            return (
                jsonify({
                    "status": "fail",
                    "message": f"Barang dengan ID {item_id} tidak ditemukan",
                }),
                404,
            )
    except ValueError:
        return (
            jsonify({
                "status": "fail",
                "message": (
                    "Format data price atau category_id tidak valid (harus angka)."
                ),
            }),
            400,
        )

    return (
        jsonify({
            "status": "success",
            "message": "Data barang berhasil diperbarui",
            "data": updated_item,
        }),
        200,
    )


@product_bp.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    success = ProductService.remove_item(item_id)
    if not success:
        return (
            jsonify({
                "status": "fail",
                "message": f"Barang dengan ID {item_id} tidak ditemukan",
            }),
            404,
        )

    return (
        jsonify({
            "status": "success",
            "message": "Data barang berhasil dihapus",
        }),
        200,
    )