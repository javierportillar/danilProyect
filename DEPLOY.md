# Deploy Ready (Supabase + Render + Vercel)

## 1) Supabase (DB)

1. Crea proyecto en Supabase.
2. En SQL Editor ejecuta `backend/schema_supabase.sql`.
3. Copia la cadena Postgres (pooler) y usa `sslmode=require`.

Ejemplo:

`postgresql://postgres.<project-ref>:<db-password>@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require`

## 2) Backend en Render (gratis)

1. Conecta repo en Render.
2. Render detecta `render.yaml` automáticamente.
3. Completa estas variables obligatorias:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `CORS_ORIGINS` (ej: `https://tu-frontend.vercel.app`)
4. Deploy.
5. Verifica salud en: `https://tu-backend.onrender.com/health`.

## 3) Frontend en Vercel (gratis)

1. Importa el repo en Vercel.
2. En Project Settings, cambia Root Directory a `frontend`.
3. Define variable obligatoria:
   - `REACT_APP_API_URL=https://tu-backend.onrender.com/api`
4. Deploy.

## 4) Checklist final

- Frontend abre y hace login.
- `GET /api/test` responde desde frontend.
- Crear venta funciona y se refleja en tabla `ventas` de Supabase.
- En backend, `CORS_ORIGINS` coincide exactamente con el dominio del frontend.

## 5) Nota de cookies

Como frontend y backend estarán en dominios distintos, debes mantener:

- `SESSION_COOKIE_SECURE=true`
- `SESSION_COOKIE_SAMESITE=None`

Si no, la sesión no persistirá correctamente en navegador.
