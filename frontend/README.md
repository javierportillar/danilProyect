# Frontend (React)

## Setup local

```bash
cd frontend
npm install
cp .env.example .env
npm start
```

## Variables de entorno

- `REACT_APP_API_URL`: URL pública del backend + `/api`
  - Ejemplo producción: `https://api.tudominio.com/api`
- `REACT_APP_API_TIMEOUT_MS`: timeout de requests

## Build producción

```bash
cd frontend
npm run build
```

## Deploy frontend (Vercel/Netlify)

- Build command: `npm run build`
- Publish directory: `build`
- Env var obligatoria: `REACT_APP_API_URL`
