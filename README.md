# Portofolio
Fullstack portofolio showcase built with Django.
Built to fulfill my PBP Individual Project obligation.

## Identity
Nama: Joachim Susatiyo

NPM: 2506602694

Kelas: PBP D

## Architecture Overview

Django MVT project with PostgreSQL and containerized development/production deployment.

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