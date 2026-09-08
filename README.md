# Portofolio
Fullstack portofolio showcase built with Django.
Built to fulfill my PBP Individual Project obligation.

## Identity
Nama: Joachim Susatiyo

NPM: 2506602694

Kelas: PBP D

## Development Setup
There are two ways to run this application.

### Prerequisites
* Python 3.13+
* `uv` or `pip`

### Option 1: Using `uv`
```bash
uv sync
uv run python manage.py migrate
uv run python manage.py tailwind dev
```

### Option 2: using `pip`
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py tailwind dev
```

## Architecture Overview

Django MVT project with PostgreSQL and containerized development/production deployment.
Uses service selector structure popularized by [Hacksoft](https://github.com/redkoolaidplz/HackSoft-Django-Styleguide) to interact with models.

### Tech Stack

| Layer | Technology | Details |
|-------|------------|---------|
| Language | Python 3.14 | Managed via `uv` + `devenv.nix` |
| Framework | Django 6.1 | MVT, `config/` as project package |
| Database | PostgreSQL 16 Alpine | With psycopg2 |
| App Server | Gunicorn 26.2 | Run with WSGI |
| Templates | Django Templates | Global `templates/` and per-app templates |
| Tooling | Ruff, djLint | Configured in `pyproject.toml` |

### Project Structure

```bash

├── config/               # Django project package
├── apps/                 # Django app packages
│   └── home/             
├── templates/            # Global templates
├── manage.py             # Django management entry point
├── compose.yml           # Dev: PostgreSQL only
├── prod.compose.yml      # Prod: web + db (as template only)
├── Dockerfile            # Used for deployment
├── devenv.nix            # Nix-based dev environment 
└── pyproject.toml        # Dependencies & tool config 
```

## Reflection
Answers for weekly reflective questions

### Tugas 1
1. Ya, saya menstruktur halaman HTML saya menggunakan elemen semantik bawaan HTML. Saya menggunakan elemen `header`, `nav`, `main`, `section`, dan `footer` pada halaman portofolio saya. Pemisahan elemen menggunakan tags tersebut memberikan makna semantik sehingga meningkatkan accessibility, seperti screen reader, dan juga memisahkan informasi yang sesuai untuk digunakan dalam mengomptimasi search engine reach. Apabila saya tidak menggunakan elemen semantik ini, konten portofolio akan dianggap sebagai satu kesatuan tanpa memiliki makna apapun. 
2. Dalam mengatur css, saya mengalami tantangan dalam 2 section, yaitu hero dengan permasalahan image scaling dan my interests dengan permasalahan translation. Pada section hero, diperlukan menggunakan class absolute agar kedua gambar dapat menindih satu sama lainnya yang konsekuensinya pada saat itu adalah merusak tampilan pada mobile. Solusi saya pada saat itu adalah dengan melakukan pengaturan dengan flexbox untuk memindahkan foto menjadi lebih luwes. Lalu, scrolling interests sangat menantang kemampuan menyusun struktur HTMl agar ketika dilakukan translasi vertikal semua konten akan ter-scroll dengan baik. Kemudian, beberapa permasalahan dalam membuat page menjadi responsif pada mobile dan desktop seperti mengubah arah flexbox agar elemen tidak overflow, pengaturan centering elemen, dan membuat breakpoint agar elemen pada desktop ataupun mobile menghilang pada waktu yang sesuai.
3. Pada tahap development ini, saya merasakan bahwa terdapat pengulangan data yang seharusnya dapat di grouping dalam array, seperti pada scrolling interests. Pada static web, data terpaksa harus di hardcode karena tidak ada fitur untuk rendering secara dynamic seperti pada React. Lalu, pada roadmap, saya ingin menambahkan fitur untuk searching dan filtering secara dynamic yang mungkin akan sangat sulit untuk diterapkan pada static web.


#### AI Disclosure
Saya menggunakan Chatbot Google Gemini selama proses programming fitur untuk membantu dalam hal berikut.
1. Menyiapkan boilerplate saat melakukan revamp 100% website. Termasuk dalam pembuatan Dockerfile dan instalasi django-tailwind.
2. Membantu menyelesaikan permasalahan styling, seperti: permasalahan centering pada elemen dan gambar pada hero section dan about me section.
3. Membantu menyiapkan keyframes dalam melakukan animasi scrolling menggunakan tailwind css.

Keterbatasan AI sempat saya rasakan ketika beberapa fitur yang disarankan tidak sesuai dengan visi saya. AI tidak memiliki "mata" untuk melihat tampilan sebuah halaman seperti seorang manusia. Oleh karena itu, sering terjadi kesalahan saat melakukan styling, seperti saat animasi scrolling, dan centering beberapa elemen. Saya sendiri harus mengoreksi hampir semua fitur yang dibantu oleh AI, seperti permasalahan flexbox dan coloring. Namun, AI sangat berguna dalam menyelesaikan tugas repetitif seperti menyiapkan data hardcoded pada fitur scrolling saya.

### Tugas 2
1. Alur request hingga response saat user membuka halaman portofolio baru sebagai berikut.
  - request: user meng-klik tombol navigasi pada salah satu halaman di website, misalnya: `projects`.
  - `urls.py` (project): django menerima HTTP Request melalui `urls` proyek. File ini memeriksa request url dan membaca setiap route yang tersedia pada file urls. Kemudian, django meneruskan penanganan request ke `urls` milik aplikasi melalui fungsi `include`.
  - `urls.py` (app): urls milik aplikasi mencocokkan URL dengan `view` yang sesuai untuk menangani halaman tersebut.
  - `views.py`: view memroses logika bisnis. Mulai dari meminta data portofolio dari model hingga pengolahan data untuk dimasukkan ke dalam context halaman dan kemudian akan ditampilkan melalui fungsi `render()`.
  - `models.py`: model melakukan query ke database, seperti `Project.objects.all()` untuk mengambil data portofolio yang tersimpan, lalu mengembalikan data tersebut ke view.
  - template : django template engine menggabungkan struktur HTML dengan data dari context menggunakan sintaks Django Template Language (DTL).
  - response: hasil akhir berupa dokumen HTML hasil gabungan data yang sudah diproses dikirimkan ke browser user untuk ditampilkan.
2. Data portofolio sebaiknya disimpan dalam suatu model karena hal berikut.
  - separation of concerns: memisahkan fungsi dan data dari tampilan. Fungsi suatu halaman ditulis dalam view aplikasi, dan penyimpanan serta deklarasi data disimpan pada suatu model sehingga tidak terjadi pengulangan deklarasi data.
  - maintainability: menambah, mengedit, atau menghapus data pada projek atau aplikasi tidak memerlukan perubahan kode, commit git, ataupun deployment ulang server. Karena dapat melakukan pembaruan data melalui halaman admin atau interface lainnya.
  - scalability: apabila nanti portofolio memiliki ratusan hingga ribuan data yang dapat berubah, template cukup menggunakan satu perulangan tanpa perlu menulis elemen HTML berkali-kali.
3. Fungsi `makemigrations` adalah untuk mendeteksi perubahan model dan membuat file migrasi dalam bentuk script python, baik untuk memanipulasi data ataupun membuat definisi data yang baru. Sedangkan, fungsi `migrate` untuk menerapkan script migrasi python yang sudah dibuat melalui command `makemigrations` sebelumnya. Saya mengubah salah satu kolom pada model `Experience` dan menambahkan model `Project` yang baru untuk menyimpan semua projek saya. Saat mengubah salah satu kolom, saya melakukan perubahan pada file `models.py` terlebih dahulu, lalu melakukan `makemigrations` (`0002_rename_experience_type_experience_category.py`) dan kemudian melakukan `migrate`. Alur yang sama terjadi juga ketika saya menambahkan model `Project` yang baru hanya saja saya membuat class model baru. Semua migrasi data dilakukan oleh script kepada database seperti PostgreSQL ataupun SQLite.

#### AI Disclosure
Saya menggunakan Chatbot Google Gemini dan ChatGPT selama proses programming untuk membantu dalam hal berikut. Chat Logs: [https://docs.google.com/document/d/1rD72sG6wP-SsP1-JLVWpy-S9herYrWJCqkQsDDLfAwU/edit?usp=sharing](https://docs.google.com/document/d/1rD72sG6wP-SsP1-JLVWpy-S9herYrWJCqkQsDDLfAwU/edit?usp=sharing)
1. Membantu saya dalam melakukan research mengenai best practices dalam menstruktur templates dalam bahasa templating django.
2. Membantu saya dalam melakukan perbaikan pada animasi css untuk meningkatkan interaktibilitas website.
3. Membantu saya dalam melakukan refactor pada test cases tutorial.