# Mock Dataset
categories = [
    {"id": 1, "name": "Elektronik"},
    {"id": 2, "name": "Pakaian"},
    {"id": 3, "name": "Makanan & Minuman"},
]

items = [
    {"id": 1, "name": "Laptop Gaming", "price": 12000000, "category_id": 1},
    {"id": 2, "name": "Kemeja", "price": 150000, "category_id": 2},
    {"id": 3, "name": "Kopi Susu", "price": 50000, "category_id": 3},
    {"id": 4, "name": "Mouse Wireless", "price": 250000, "category_id": 1},
    {"id": 5, "name": "Batik", "price": 200000, "category_id": 2},
    {"id": 6, "name": "Teh Botol", "price": 10000, "category_id": 3},
]


class ProductRepository:

  @staticmethod
  def get_all_categories():
    return categories

  @staticmethod
  def get_all_items():
    return items

  @staticmethod
  def get_item_by_id(item_id):
    return next((i for i in items if i["id"] == item_id), None)

  @staticmethod
  def update_item(item_id, data):
    item = ProductRepository.get_item_by_id(item_id)
    if item:
      item["name"] = data.get("name", item["name"])
      item["price"] = float(data.get("price", item["price"]))
      item["category_id"] = int(data.get("category_id", item["category_id"]))
      return item
    return None

  @staticmethod
  def delete_item(item_id):
    global items
    item = ProductRepository.get_item_by_id(item_id)
    if item:
      items = [i for i in items if i["id"] != item_id]
      return True
    return False