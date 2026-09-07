# Portofolio
Fullstack portofolio showcase built with Django.
Built to fulfill my PBP Individual Project obligation.

## Identity
Nama: Joachim Susatiyo

NPM: 2506602694

Kelas: PBP D

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