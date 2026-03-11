# Backend (Flask + SQLAlchemy + Supabase Postgres)

## Estructura

- `app/`: configuración, modelos, rutas y seed
- `scripts/`: utilidades (incluye migración desde SQLite legado)
- `legacy/`: código/archivos antiguos movidos desde la raíz

## Setup local (desde `backend/`)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Inicializar base de datos

```bash
cd backend
flask --app wsgi init-db
```

## Ejecutar backend

```bash
cd backend
flask --app wsgi run --debug
```

## Migraciones de esquema

```bash
cd backend
flask --app wsgi db init
flask --app wsgi db migrate -m "init schema"
flask --app wsgi db upgrade
```

## Migrar datos del SQLite legado a Supabase

```bash
cd backend
SQLITE_PATH=./legacy/database.db DATABASE_URL="<tu-url-supabase>" \
python scripts/migrate_sqlite_to_postgres.py
```

## Variables que debes poner para deploy

- `SECRET_KEY`
- `DATABASE_URL` (la de Supabase)
- `CORS_ORIGINS` (dominio(s) reales del frontend)
- `SESSION_COOKIE_SECURE=true`
- `SESSION_COOKIE_SAMESITE=None`

## Comando de arranque en plataforma

- `gunicorn wsgi:app`
- Root directory del servicio: `backend`
