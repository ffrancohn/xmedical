# XMedical Frontend (React) — LEGADO

> **Este directorio corresponde a un prototipo anterior y no forma parte del stack activo de XMedical.**
>
> La interfaz actual usa **plantillas Django** (server-side rendering). Consulta el [`README.md`](../README.md) principal para instalación y uso.

## Qué contenía este prototipo

Frontend SPA para el backend FastAPI legado, con:

- React 18 + TypeScript + Vite
- Autenticación JWT
- Páginas de documentos, beneficiarios, direcciones y feedback
- Integración con OCR y verificación biométrica

## Ejecución (solo referencia histórica)

Requiere el backend FastAPI en `server/` corriendo en http://localhost:8000.

```bash
cd client
npm install
cp env.example .env.local
npm run dev
```

- Frontend: http://localhost:3000

> **Nota:** Este frontend no se conecta al backend Django activo.

## Documentación relacionada (legado)

- [`docs/guia-integracion.md`](../docs/guia-integracion.md) — Integración con API FastAPI

---

## Referencia técnica del prototipo

### Requisitos

- Node.js 18+
- Backend FastAPI en `http://localhost:8000`

### Estructura

```
client/
├── src/
│   ├── components/    # Auth, Layout
│   ├── contexts/      # AuthContext, ThemeContext
│   ├── pages/         # Login, Dashboard, Documents, etc.
│   ├── services/      # api.ts (cliente HTTP)
│   └── types/         # Tipos TypeScript
├── package.json
└── vite.config.ts
```

### Variables de entorno

```env
VITE_API_URL=http://localhost:8000
```
