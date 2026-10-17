from app.routes.product_routes import product_bp
from flask import Flask


def create_app():
  app = Flask(__name__)
  app.config.from_object("app.config.Config")

  # Registrasi Blueprint dengan prefix /api/v1
  app.register_blueprint(product_bp, url_prefix="/api/v1")

  return app