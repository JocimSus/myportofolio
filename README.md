# Portofolio

Fullstack portofolio showcase built with Django. 

Built to fulfill my PBP Individual Project obligation.

## Identity

Nama: **Joachim Susatiyo**

NPM: **2506602694**

Kelas: **PBP D**

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Database Setup & Migrations](#database-setup--migrations)
  - [Initial Data Seeding](#initial-data-seeding)
- [Docker Setup](#docker-setup)
  - [Development Database](#development-database)
- [Testing](#testing)
  - [Running Tests](#running-tests)
  - [Code Linting & Formatting](#code-linting--formatting)
- [API Documentation](#api-documentation)
- [Reflections](#reflections)

## Overview

This Portofolio application is designed to showcase software engineering projects, work experiences, technical skill sets, and personal background. Originally developed as part of the *Pemrograman Berbasis Platform (PBP)* course at Universitas Indonesia, it has been structured to meet high open-source engineering standards, including strict code quality, type hinting, automated testing, and containerized deployment.

This Portofolio application is built to showcase my personal skills, experience, and projects. This django app is devloped for the Pemrograman Basis Platform course. It loosely follows HackSoft's Django Styleguide. This app also includes automated testing, automated deployment, and strict code quality checking.

## Tech Stack

| Role | Technology | Version | Description |
|---|---|---|---|
| **Language** | Python | `>=3.13` (also supports `3.13+`) | Virtual environment management via `uv` or `devenv.nix`. |
| **Web Framework** | Django | `5.2` (LTS) | Model-View-Template (MVT) framework. |
| **Styling** | Tailwind CSS | `v4.3.3` (`django-tailwind`) |  |
| **Development DB** | SQLite | `3` | File-based relational database. |
| **Production DB** | PostgreSQL | `16-alpine` | Relational database connected via `psycopg`. |
| **Static File Server** | WhiteNoise | `6.12.0` | Static file server from Gunicorn/WSGI. |
| **Application Server** | Gunicorn | `26.2.0` | Production WSGI HTTP server. |
| **Code Formatter & Linter** | Ruff | `0.16.4` | Python linter and formatter (Black style). |
| **Template Linter** | djLint | `1.44.2` | HTML and Django template formatter and syntax linter. |
| **Live Reloading** | Django Browser Reload | `1.21.0` | Automatic browser refresh on template or static CSS changes in dev. |
| **Containerization** | Docker & Compose | `python:3.14-slim` | Containerized deployment. |

---

## Architecture Overview

The application loosely follows HackSoft's Django Styleguide pattern to keep business logic maintainable, testable, and separated from HTTP presentation layers:

1. **Models (`apps/home/models.py`)**: Relational tables.
2. **Selectors (`apps/home/selectors.py`)**: Database queries and context fetching logic outside of view handlers.
3. **Forms (`apps/home/forms.py`)**: Validate and parse user input.
4. **Decorators (`apps/home/decorators.py`)**: Temporarily made to force password checking in mutation operations.
5. **Views (`apps/home/views.py`)**: Handle form submission and renders HTML or JSON.

## Project Structure

```text
portfolio/
├── .github/                       # GitHub Actions workflows and templates
│   ├── workflows/
├── apps/                          # Django application packages
│   ├── home/                      # Core domain application
│   │   ├── migrations/            # Database schema migrations
│   │   ├── templates/home/        # App templates
│   │   ├── templatetags/          # Custom template tags
│   │   ├── tests/                 # Unit test suite
│   │   ├── admin.py                
│   │   ├── apps.py                
│   │   ├── choices.py             # Enums for data models
│   │   ├── context_processors.py  # Global profile context processor
│   │   ├── decorators.py          # Decorators
│   │   ├── forms.py               # Forms config
│   │   ├── models.py              # Data Models
│   │   ├── selectors.py           # Database query selectors
│   │   ├── urls.py                # App routing
│   │   └── views.py               # View controllers
│   └── theme/                     # Tailwind CSS
├── config/                        # Django project configuration
├── scripts/                       # Database management and utility scripts
├── compose.yml                    # Local PostgreSQL 16 service for development
├── manage.py                      # Django CLI management entry point
├── Procfile.tailwind              # Process manager config for Django + Tailwind
├── pyproject.toml                 # Tooling configuration
├── requirements.txt               # Pinned Python package dependencies
```

## Getting Started

### Prerequisites

Ensure you have the following tools installed on your development machine:

- **Python**: `>= 3.14` (or `3.13+`)
- **Package Manager**: [`uv`](https://docs.astral.sh/uv/) (recommended) or standard `pip`
- **Docker & Docker Compose**: Optional for running a local PostgreSQL instance

---

### Local Development Setup

#### Option 1: Using `uv` (Recommended)

[`uv`](https://github.com/astral-sh/uv) provides npm-like deterministic dependency tracking:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JocimSus/myportofolio.git
   cd myportofolio
   ```

2. **Synchronize dependencies**:
   ```bash
   uv sync
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

4. **Run database migrations**:
   ```bash
   uv run python manage.py migrate
   ```

5. **Start the development server with Tailwind**:
   ```bash
   uv run python manage.py tailwind dev
   # or
   uv run python manage.py runserver 127.0.0.1:8000
   ```

---

#### Option 2: Using Python `venv` & `pip`

1. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py tailwind dev
   # or
   python manage.py runserver 127.0.0.1:8000
   ```

The application will be accessible at:
- Web Application: [http://localhost:8000](http://localhost:8000)

---

### Database Setup & Migrations

By default, when `PRODUCTION=False`, the application uses a local SQLite database (`db.sqlite3`).

```bash
# Create new migrations if you modified models
python manage.py makemigrations

# Apply pending migrations
python manage.py migrate
```

---

### Initial Data Seeding

Seeding scripts are available in the `scripts/` directory to populate your database with initial projects and experience entries.

```bash
python manage.py shell < scripts/seed_projects.py

python manage.py shell < scripts/seed_experiences.py
```

Additional database utilities.
```bash
# Export all projects and experiences to JSON
python manage.py shell < scripts/dump_data.py

# Delete all records from projects and experiences tables
python manage.py shell < scripts/delete_data.py
```

## Docker Setup

### Development Database

PostgreSQL 16 setup in `compose.yml`.

```bash
# Start PostgreSQL on port 55432
docker compose up -d

# Stop PostgreSQL service
docker compose down
```

To connect Django to this container, set `PRODUCTION=True`, `DB_HOST=localhost`, `DB_PORT=55432` in your `.env` file, and run `python manage.py migrate`.

## Testing

### Running Tests

Covers models, form validation, view routing, search filtering, and password-protected authorization forms.

```bash
# Run all tests
python manage.py test

# Run specific test suites
python manage.py test apps.home.tests.test_views
python manage.py test apps.home.tests.test_models
python manage.py test apps.home.tests.test_forms
```

#### Test Coverage

```bash
# Run tests with coverage
coverage run manage.py test

# Display coverage report
coverage report -m

# Generate HTML coverage report
coverage html
```

---

### Code Linting & Formatting

Quality checks are configured in `pyproject.toml` and also checked via GitHub Actions:

```bash
# Check Python code linting
uv run ruff check

# Automatically fix linting problems
uv run ruff check --fix

# Check Python formatting
uv run ruff format --check

# Reformat Python code
uv run ruff format

# Check Django HTML templates with djLint
uv run djlint --check .

# Automatically reformat Django HTML templates
uv run djlint --reformat .

# Lint template syntax and tags
uv run djlint --lint .
```

---

## API Documentation

All API's do not have endpoints, these serve only as documentation.

### 1. Project List API

Returns all projects serialized in JSON, with keyword filtering.

**Example Response**:
```json
[
  {
    "model": "home.project",
    "pk": "d4a8b7c2-1e3f-4a5b-8c9d-0e1f2a3b4c5d",
    "fields": {
      "title": "COMPFEST 18",
      "slug": "compfest-18",
      "description": "Main website for COMPFEST 18's Event.",
      "thumbnail": "https://zip.jocimsus.tech/u/6fa7bd84-31a5-49df-8b8f-4469c860e979.webp",
      "project_url": "https://compfest.id",
      "technologies": ["Docker", "Next.js", "TanStack", "TailwindCSS"],
      "category": "website"
    }
  }
]
```

---

### 2. Experience List API

Returns all registered experiences ordered chronologically by start date.

- **Response Format**:
```json
[
  {
    "model": "home.experience",
    "pk": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "fields": {
      "title": "RISTEK",
      "description": "Member of RISTEK's Web Development SIG",
      "category": "organization",
      "thumbnail": "https://zip.jocimsus.tech/u/13ab0ace-04e9-4c67-b738-1b545eab1306.webp",
      "start_date": "2026-05-01",
      "end_date": null
    }
  }
]
```

---

### 3. Profile Information API

Returns profile metadata.

- **Response Format**:
```json
{
  "npm": "2506602694",
  "study_program": "Ilmu Komputer - S1",
  "bio": "a passionate computer science student at Universitas Indonesia. I love exploring new technologies and applying them to solve real-world problems.",
  "interests": [
    "Web Development",
    "System Design",
    "Operating Systems",
    "Cloud Infrastructure"
  ],
  "experience_truncated": [
    "Winner of RISTEK Hackathon 2026",
    "Vice Lead of IT Dev OH Fasilkom 2026",
    "Member of RISTEK Web Development"
  ]
}
```

---

## Reflections

### Tugas 1
1. Ya, saya menstruktur halaman HTML saya menggunakan elemen semantik bawaan HTML. Saya menggunakan elemen header, nav, main, section, dan footer pada halaman portofolio saya. Pemisahan elemen menggunakan tags tersebut memberikan makna semantik sehingga meningkatkan accessibility, seperti screen reader, dan juga memisahkan informasi yang sesuai untuk digunakan dalam mengomptimasi search engine reach. Apabila saya tidak menggunakan elemen semantik ini, konten portofolio akan dianggap sebagai satu kesatuan tanpa memiliki makna apapun.
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
   * request: user meng-klik tombol navigasi pada salah satu halaman di website, misalnya: projects.
   * `urls.py` (project): django menerima HTTP Request melalui urls proyek. File ini memeriksa request url dan membaca setiap route yang tersedia pada file urls. Kemudian, django meneruskan penanganan request ke urls milik aplikasi melalui fungsi include.
   * `urls.py` (app): urls milik aplikasi mencocokkan URL dengan view yang sesuai untuk menangani halaman tersebut.
   * `views.py`: view memroses logika bisnis. Mulai dari meminta data portofolio dari model hingga pengolahan data untuk dimasukkan ke dalam context halaman dan kemudian akan ditampilkan melalui fungsi render().
   * `models.py`: model melakukan query ke database, seperti Project.objects.all() untuk mengambil data portofolio yang tersimpan, lalu mengembalikan data tersebut ke view.
   * `template` : django template engine menggabungkan struktur HTML dengan data dari context menggunakan sintaks Django Template Language (DTL).
   * response: hasil akhir berupa dokumen HTML hasil gabungan data yang sudah diproses dikirimkan ke browser user untuk ditampilkan.

2. Data portofolio sebaiknya disimpan dalam suatu model karena hal berikut.
   * separation of concerns: memisahkan fungsi dan data dari tampilan. Fungsi suatu halaman ditulis dalam view aplikasi, dan penyimpanan serta deklarasi data disimpan pada suatu model sehingga tidak terjadi pengulangan deklarasi data.
   * maintainability: menambah, mengedit, atau menghapus data pada projek atau aplikasi tidak memerlukan perubahan kode, commit git, ataupun deployment ulang server. Karena dapat melakukan pembaruan data melalui halaman admin atau interface lainnya.
   * scalability: apabila nanti portofolio memiliki ratusan hingga ribuan data yang dapat berubah, template cukup menggunakan satu perulangan tanpa perlu menulis elemen HTML berkali-kali.

3. Fungsi makemigrations adalah untuk mendeteksi perubahan model dan membuat file migrasi dalam bentuk script python, baik untuk memanipulasi data ataupun membuat definisi data yang baru. Sedangkan, fungsi migrate untuk menerapkan script migrasi python yang sudah dibuat melalui command makemigrations sebelumnya. Saya mengubah salah satu kolom pada model Experience dan menambahkan model Project yang baru untuk menyimpan semua projek saya. Saat mengubah salah satu kolom, saya melakukan perubahan pada file models.py terlebih dahulu, lalu melakukan makemigrations (0002_rename_experience_type_experience_category.py) dan kemudian melakukan migrate. Alur yang sama terjadi juga ketika saya menambahkan model Project yang baru hanya saja saya membuat class model baru. Semua migrasi data dilakukan oleh script kepada database seperti PostgreSQL ataupun SQLite.

#### AI Disclosure
Saya menggunakan Chatbot Google Gemini dan ChatGPT selama proses programming untuk membantu dalam hal berikut. Chat Logs: [https://docs.google.com/document/d/1rD72sG6wP-SsP1-JLVWpy-S9herYrWJCqkQsDDLfAwU/edit?usp=sharing](https://docs.google.com/document/d/1rD72sG6wP-SsP1-JLVWpy-S9herYrWJCqkQsDDLfAwU/edit?usp=sharing)
1. Membantu saya dalam melakukan research mengenai best practices dalam menstruktur templates dalam bahasa templating django.
2. Membantu saya dalam melakukan perbaikan pada animasi css untuk meningkatkan interaktibilitas website.
3. Membantu saya dalam melakukan refactor pada test cases tutorial.

### Tugas 3
1. Django menyediakan ModelForm yang mempercepat pembuatan form. ModelForm secara otomatis memetakan field dan tipe data dari Model Django menjadi input form HTML. ModelForm menangani validasi data secara otomatis melalui method form.is_valid(). Pembuatan atau pembaruan data pada model dari form dengan memanggil method form.save(). CSRF (Cross-Site Request Forgery) adalah suatu eksploit untuk menggunakan otorisasi suatu pengguna untuk melakukan suatu aksi atas nama pengguna tersebut. csrf_token berfungsi untuk menghasilkan sebuah token yang unik untuk setiap pengguna, sehingga ketika melakukan aksi pada form, maka token akan diverifikasi dengan sesi sebuah pengguna.
2. JSON lebih disukai dalam pengembangan web app karena memiliki struktur yang lebih concise daripada XML. JSON menggunakan struktur data key-value dibandingkan markup language seperti XML. Lalu, JSON memiliki tipe data primitif javascript seperti string, number, boolean, dll, sedangkan XML menganggap semua tipe data sebagai teks biasa. Sebagian besar ekosistem framework Frontend pada zaman sekarang menggunakan bahasa javascript, seperti React, Svelte, dll dengan API fetch yang secara default meminta data JSON.
3. Data diambil langsung dari Model data seperti Experiences melalui Experiences.objects.all(). Lalu, instance model tersebut diserealize menjadi format JSON untuk dikirimkan. Lalu, view yang memerlukan datanya mendapatkan response dalam bentuk JSON dan dideserealize menjadi sebuah objek python yang dapat diproses lebih lanjut menjadi konteks untuk template. Serialization harus dilakukan pada Model data karena suatu response memerlukan data yang bisa dikirim melalui HTTP. Serialization mengubah struktur objek python menjadi format key-value untuk dikirim melalui JSON.

#### AI Disclosure
Saya menggunakan Chatbot Google Gemini selama proses programming untuk membantu dalam hal berikut. Chat Logs: [Chat Logs](https://share.gemini.google/3bVU7RcegMAR)
1. Membantu saya dalam menganalisis struktur refactoring template projek yang baik.
2. Mengajarkan saya cara membuat suatu form untuk create dan update dengan best practices.
3. Mengklarifikasi kesalahan dalam pemrograman dan memberikan solusi untuk memelajari kesalahan.
4. Menganalisis views untuk menemukan fungsi yang dapat diubah agar menampilkan data menggunakan response JSON.

Lalu, saya menggunakan coding agent Antigravity secara lokal dalam proses rewriting dokumentasi agar memiliki kualitas lebih baik.

AI memiliki keterbatasan halusinasi konteks. Beberapa kali saat melakukan prompting, chatbot memberikan solusi yang terlihat benar, tetapi tidak sesuai dengan struktur projek saya. Setiap kali chatbot melakukan halusinasi, saya bisa memitigasinya dengan memberikan konteks secara proaktif kepada chatbot dengan prompt yang jelas. Namun, tetap saja terkadang memberikan hasil yang tidak sesuai, seperti penulisan test yang tidak sesuai keinginan, ataupun pembuatan form yang memiliki tipe input yang kurang sesuai. Saya, memperbaikinya dengan menyesuaikan input type form dengan keperluan saya. 

Kemudian, selama melakukan penulisan ulang dokumentasi, AI sering sekali menambahkan dokumentasi tidak relevan dan mengubah sebagian besar refleksi saya. Oleh karena itu, saya harus mengembalikan perubahan yang dibuat oleh AI.

### Tugas 4
Implementasi authorization and authentication.

#### AI Disclosure
Saya menggunakan Chatbot Google Gemini selama proses programming untuk membantu dalam hal berikut. Chat Logs: [Chat Logs](https://share.gemini.google/qEAdC0k8SzJS)
1. Membantu dalam researching perbedaan antara authorization group dan permissions.
2. Membantu saya dalam melakukan refactor fungsi decorator authorization sebelum adanya user.
3. Mengklarifikasi best practices dalam authorization.

Pada kali ini, AI membantu saya penuh dalam researching keunggulan dan kekurangan penggunaan perms ataupun groups untuk authorization. AI beberapa kali menjawab pertanyaan saya dengan jawaban yang kontradiktif jawabannya sebelumnya. Dalam hal ini, pengambilan keputusan berada sepenuhnya pada saya. Saya perlu melakukan research lagi secara mandiri untuk menentukan solusi authorization yang menurut saya paling scalable.