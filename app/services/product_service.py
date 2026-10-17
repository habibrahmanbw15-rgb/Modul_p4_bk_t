from app.repositories.product_repo import ProductRepository


class ProductService:

  @staticmethod
  def get_categories():
    return ProductRepository.get_all_categories()

  @staticmethod
  def get_filtered_items(category_query=None, min_price_query=None):
    filtered = ProductRepository.get_all_items()

    if category_query:
      cat_id = int(category_query)
      filtered = [i for i in filtered if i["category_id"] == cat_id]

    if min_price_query:
      min_price = float(min_price_query)
      filtered = [i for i in filtered if i["price"] >= min_price]

    return filtered

  @staticmethod
  def get_item_detail(item_id):
    return ProductRepository.get_item_by_id(item_id)

  @staticmethod
  def update_item_data(item_id, data):
    return ProductRepository.update_item(item_id, data)

  @staticmethod
  def remove_item(item_id):
    return ProductRepository.delete_item(item_id)