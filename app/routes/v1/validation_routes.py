from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas.user_schema import UserRegisterSchema

val_bp = Blueprint("validation_demo", __name__, url_prefix="/api/v1/auth-val")
register_schema = UserRegisterSchema()


@val_bp.route("/register", methods=["POST"])
def register_with_validation():
    # 1. Validasi Header Content-Type & sintaksis JSON secara aman
    if not request.is_json:
        return jsonify({"status": "fail", "message": "Header Content-Type wajib application/json"}), 400

    raw_payload = request.get_json(silent=True)
    if raw_payload is None:
        return jsonify({"status": "fail", "message": "Sintaksis JSON pada request body rusak atau kosong"}), 400

    # 2. Validasi Skema Deklaratif menggunakan Marshmallow
    try:
        validated_data = register_schema.load(raw_payload)
        # Serialisasi kembali menggunakan dump() agar field load_only (password) otomatis tersembunyi
        safe_response_data = register_schema.dump(validated_data)
        return jsonify({
            "status": "success",
            "message": "Data registrasi valid dan siap diproses",
            "data": safe_response_data
        }), 201
    except ValidationError as err:
        return jsonify({
            "status": "fail",
            "message": "Validasi data input gagal",
            "errors": err.messages
        }), 422


@val_bp.route("/trigger-500-demo", methods=["GET"])
def trigger_server_error_demo():
    # Endpoint simulasi bug internal untuk menguji Global Error Handler 500 & Error Logging
    hasil = 100 / 0
    return jsonify({"hasil": hasil}), 200