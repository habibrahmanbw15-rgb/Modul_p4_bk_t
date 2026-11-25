from app.models.product_model import Category, Product, db


class ProductRepository:

    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return [c.to_dict() for c in categories]

    @staticmethod
    def get_category_by_id(category_id):
        category = db.session.get(Category, category_id)
        return category.to_dict() if category else None

    @staticmethod
    def get_all_items():
        items = Product.query.all()
        return [i.to_dict() for i in items]

    @staticmethod
    def get_item_by_id(item_id):
        item = db.session.get(Product, item_id)
        return item.to_dict() if item else None

    @staticmethod
    def insert_item(name, price, category_id, stock=0):
        try:
            new_item = Product(
                name=name,
                price=price,
                category_id=category_id,
                stock=stock
            )
            db.session.add(new_item)
            db.session.commit()
            return new_item.id
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_item(item_id, data):
        item = db.session.get(Product, item_id)
        if not item:
            return None
        try:
            item.name = data.get("name", item.name)
            item.price = float(data.get("price", item.price))
            item.stock = int(data.get("stock", item.stock))
            item.category_id = int(data.get("category_id", item.category_id))
            db.session.commit()
            return item.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_item(item_id):
        item = db.session.get(Product, item_id)
        if not item:
            return False
        try:
            db.session.delete(item)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e