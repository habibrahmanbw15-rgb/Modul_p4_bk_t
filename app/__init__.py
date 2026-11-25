import logging
import os

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.models.product_model import db
from app.routes.v1.advanced_routes import advanced_bp
from app.routes.v1.product_routes import product_bp
from app.routes.v1.user_routes import user_bp_v1
from app.routes.v1.validation_routes import val_bp
from app.utils.error_handlers import register_error_handlers


def configure_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/app_error.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # WAJIB: Aktifkan CORS agar frontend (Live Server) bisa mengakses API
    CORS(app)

    db.init_app(app)

    # Registrasi Blueprint
    app.register_blueprint(advanced_bp, url_prefix="/api/v1")
    app.register_blueprint(product_bp, url_prefix="/api/v1")
    app.register_blueprint(user_bp_v1)
    app.register_blueprint(val_bp)
    register_error_handlers(app)  # Registrasi Global Error Handler

    with app.app_context():
        db.create_all()

    return app