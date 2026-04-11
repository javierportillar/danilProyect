# Backend (Flask + Supabase Postgres)

## 1) Setup local

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 2) Variables críticas para producción

- `DATABASE_URL`: URL de Supabase con `sslmode=require`
- `CORS_ORIGINS`: dominio real del frontend (ej. `https://app.tudominio.com`)
- `SECRET_KEY`: valor largo y aleatorio
- `SESSION_COOKIE_SECURE=true`
- `SESSION_COOKIE_SAMESITE=None` (si front y back van en dominios distintos)

## 3) Inicializar esquema y seed

```bash
cd backend
flask --app wsgi init-db
```

Si prefieres SQL directo en Supabase, usa:

- `schema_supabase.sql`

## 4) Ejecutar local

```bash
cd backend
flask --app wsgi run --debug
```

## 5) Deploy backend (Render/Railway/Fly)

- Root directory: `backend`
- Start command: `gunicorn --config gunicorn.conf.py wsgi:app`
- Health check: `/health` o `/api/health`

## 6) Migrar datos desde SQLite legado a Supabase

```bash
cd backend
SQLITE_PATH=./legacy/database.db DATABASE_URL="<tu-url-supabase>" \
python scripts/migrate_sqlite_to_postgres.py
```
