# Backend Modular API (Flask)

Proyek REST API sederhana yang dikembangkan menggunakan **Flask** dengan menerapkan prinsip **MVC (model,vew,control)** dan **Blueprint**.

---

## Dokumentasi Arsitektur (Layered Architecture)

Aplikasi ini memisahkan tanggung jawab (Separation of Concerns) ke dalam beberapa lapisan agar kode lebih terstruktur, mudah diuji, dan mudah dipelihara. 

Berikut adalah diagram alur data dan permintaan (request) pada aplikasi:

```text
[ Client / Postman ]
       │
       ▼ (HTTP Request)
[ Blueprint Route / Controller ] (`app/routes/`)
       │
       ▼ (Memanggil fungsi bisnis)
[ Service Layer ] (`app/services/`)
       │
       ▼ (Akses/Manipulasi data)
[ Repository Layer ] (`app/repositories/`)
       │
       ▼ (Data Storage)
[ Mock Dataset / Database ]


## Peta Endpoint POST & PUT di Proyekmu Saat Ini

user_routes.py (POST /api/v1/users): Endpoint registrasi user sederhana berbasis mock_users (hanya username dan email).   validation_routes.py (POST /api/v1/auth-val/register): Endpoint khusus latihan validasi Marshmallow (UserRegisterSchema dengan username, email, password, age) dan simulasi error 500 (/trigger-500-demo).
product_routes.py (POST /api/v1/items & PUT /api/v1/items/<int:item_id>): Endpoint CRUD utama untuk barang/produk (name, price, category_id, dan stock jika dipakai di service).
advanced_routes.py (POST /api/v1/advanced/products/transaction-demo): Endpoint transaksi atomik yang membuat kategori baru (jika belum ada) sekaligus produk baru (category_name, product_name, price) dalam satu transaksi database.
