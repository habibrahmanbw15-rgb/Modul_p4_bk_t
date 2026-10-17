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