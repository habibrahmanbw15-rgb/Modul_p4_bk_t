from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate, validates


class UserRegisterSchema(Schema):
    class Meta:
        # Mengabaikan field asing yang tidak didefinisikan dalam skema (mencegah Mass Assignment)
        unknown = EXCLUDE

    username = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=4, max=30, error="Username harus antara 4 hingga 30 karakter."
            ),
            validate.Regexp(
                r"^[a-zA-Z0-9_]+$",
                error="Username hanya boleh berisi huruf, angka, dan underscore.",
            ),
        ],
        error_messages={"required": "Field username wajib diisi."},
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Field email wajib diisi.",
            "invalid": "Format alamat email tidak valid.",
        },
    )
    password = fields.Str(
        required=True,
        load_only=True,  # Tidak pernah dikembalikan saat proses serialisasi (dump)
        validate=validate.Length(min=8, error="Password minimal harus 8 karakter."),
    )
    age = fields.Int(
        required=False,
        validate=validate.Range(
            min=17, max=100, error="Usia harus berada di rentang 17 hingga 100 tahun."
        ),
    )
    role = fields.Str(
        load_default="user",
        validate=validate.OneOf(
            ["user", "admin"], error="Role hanya diperbolehkan 'user' atau 'admin'."
        ),
    )

    @validates("username")
    def validate_reserved_username(self, value, **kwargs):
        # Contoh Custom Validator untuk aturan bisnis spesifik
        reserved = {"admin", "root", "superuser", "system"}
        if value.lower() in reserved:
            raise ValidationError(
                f"Username '{value}' dilindungi sistem dan tidak dapat digunakan."
            )