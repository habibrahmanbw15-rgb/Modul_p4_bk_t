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
  def get_categories_id(categories_id):
    return ProductRepository.get_categories_by_id(categories_id)

  @staticmethod
  def get_item_detail(item_id):
    return ProductRepository.get_item_by_id(item_id)

  @staticmethod
  def update_item_data(item_id, data):
    return ProductRepository.update_item(item_id, data)

  @staticmethod
  def remove_item(item_id):
    return ProductRepository.delete_item(item_id)

  @staticmethod
  def create_item_data(data):
        name = str(data.get("name", "")).strip()
        if not name:
            raise ValueError("Nama barang tidak boleh kosong")

        # Validasi & konversi tipe data angka (akan memicu ValueError jika gagal)
        price = float(data["price"])
        category_id = int(data["category_id"])
        stock = int(data.get("stock", 0))  # Opsional jika tabel memiliki kolom stock

        if price < 0 or stock < 0:
            raise ValueError("Harga dan stok tidak boleh bernilai negatif")

        # Cek apakah category_id valid di database
        category = ProductRepository.get_category_by_id(category_id)
        if not category:
            raise ValueError(f"Kategori dengan ID {category_id} tidak ditemukan")

        # Simpan ke database melalui repository
        new_item_id = ProductRepository.insert_item(
            name=name,
            price=price,
            category_id=category_id,
            stock=stock,
        )

        # Kembalikan detail barang yang baru saja disimpan
        return ProductRepository.get_item_by_id(new_item_id)