from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relasi One-to-Many ke tabel products
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None
        }