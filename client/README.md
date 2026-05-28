# XMedical Frontend

Frontend de la aplicación XMedical - Sistema de Asistencia Médica Inteligente, desarrollado con React 18, TypeScript y Bootstrap.

## 🚀 Características

- **React 18** con TypeScript para desarrollo moderno y tipado
- **Bootstrap 5** para diseño responsive y componentes UI
- **TanStack Query** para gestión de estado del servidor
- **React Hook Form** con Zod para formularios y validaciones
- **Wouter** para enrutamiento ligero y eficiente
- **Lucide React** para iconografía moderna
- **Tema personalizable** con modo claro/oscuro y colores
- **Autenticación JWT** con refresh tokens automático
- **Verificación biométrica** integrada (OCR y reconocimiento facial)
- **Gestión completa de usuarios** con roles y permisos
- **Interfaz administrativa** para gestión del sistema

## 📋 Requisitos Previos

- Node.js 18+ 
- npm o yarn
- Backend XMedical ejecutándose en `http://localhost:8000`

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd xmedical/client
```

2. **Instalar dependencias**
```bash
npm install
# o
yarn install
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env.local
```

Editar `.env.local`:
```env
VITE_API_URL=http://localhost:8000
```

4. **Ejecutar en modo desarrollo**
```bash
npm run dev
# o
yarn dev
```

La aplicación estará disponible en `http://localhost:3000`

## 🏗️ Estructura del Proyecto

```
client/
├── public/                 # Archivos públicos
├── src/
│   ├── components/         # Componentes reutilizables
│   │   ├── Auth/          # Componentes de autenticación
│   │   └── Layout/        # Componentes de layout
│   ├── contexts/          # Contextos de React
│   ├── hooks/             # Custom hooks
│   ├── pages/             # Páginas de la aplicación
│   ├── services/          # Servicios de API
│   ├── styles/            # Estilos CSS
│   ├── types/             # Tipos TypeScript
│   ├── utils/             # Utilidades
│   ├── App.tsx            # Componente principal
│   └── main.tsx           # Punto de entrada
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 🎨 Temas y Personalización

El frontend incluye un sistema de temas personalizable:

### Modos de Tema
- **Claro**: Tema por defecto con colores claros
- **Oscuro**: Tema oscuro para mejor experiencia nocturna

### Colores de Tema
- Azul (por defecto)
- Verde
- Púrpura
- Naranja
- Rojo
- Gris

### Configuración
Los temas se pueden cambiar desde:
1. Sidebar → Configuración → Modo oscuro
2. Sidebar → Configuración → Color del tema
3. Perfil de usuario → Configuración de Tema

## 🔐 Autenticación

El sistema utiliza JWT tokens con las siguientes características:

- **Access Token**: Token de acceso de corta duración
- **Refresh Token**: Token de renovación de larga duración
- **Renovación automática**: Los tokens se renuevan automáticamente
- **Logout automático**: Redirección al login cuando los tokens expiran

### Flujo de Autenticación
1. Usuario ingresa credenciales
2. Sistema valida y retorna tokens
3. Tokens se almacenan en localStorage
4. Requests incluyen token automáticamente
5. Refresh automático cuando el access token expira

## 📱 Páginas Principales

### Páginas Públicas
- **Login**: Autenticación de usuarios
- **Register**: Registro de nuevos usuarios

### Páginas Protegidas
- **Dashboard**: Panel principal con estadísticas
- **Profile**: Gestión del perfil de usuario
- **Documents**: Gestión de documentos con verificación OCR
- **Addresses**: Gestión de direcciones
- **Beneficiaries**: Gestión de beneficiarios
- **Feedback**: Sistema de comentarios y sugerencias

### Páginas Administrativas
- **Admin**: Panel de administración del sistema

## 🔧 Configuración de Desarrollo

### Variables de Entorno
```env
# URL del backend
VITE_API_URL=http://localhost:8000

# Configuración de desarrollo
VITE_DEV_MODE=true
VITE_ENABLE_LOGS=true
```

### Scripts Disponibles
```bash
# Desarrollo
npm run dev

# Construcción para producción
npm run build

# Vista previa de producción
npm run preview

# Linting
npm run lint
```

## 🧪 Testing

```bash
# Ejecutar tests
npm test

# Tests en modo watch
npm run test:watch

# Coverage
npm run test:coverage
```

## 📦 Construcción para Producción

```bash
# Construir aplicación
npm run build

# Los archivos se generan en /dist
```

### Configuración de Servidor
Para servir la aplicación en producción:

```bash
# Instalar serve globalmente
npm install -g serve

# Servir archivos estáticos
serve -s dist -l 3000
```

## 🔌 Integración con Backend

El frontend se conecta al backend a través de:

### Endpoints Principales
- **Autenticación**: `/auth/login`, `/auth/register`, `/auth/refresh`
- **Usuarios**: `/users/`, `/users/me`
- **Documentos**: `/documents/`
- **Direcciones**: `/addresses/`
- **Beneficiarios**: `/beneficiaries/`
- **Feedback**: `/feedback/`
- **Biométricos**: `/biometric/ocr/process`, `/biometric/facial/verify`
- **Upload**: `/upload/`

### Configuración de Proxy
En desarrollo, el proxy está configurado en `vite.config.ts`:
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Error de conexión al backend**
   - Verificar que el backend esté ejecutándose en `http://localhost:8000`
   - Revisar la configuración de CORS en el backend

2. **Error de autenticación**
   - Limpiar localStorage: `localStorage.clear()`
   - Verificar que los tokens sean válidos

3. **Error de compilación TypeScript**
   - Ejecutar `npm run lint` para ver errores
   - Verificar tipos en `src/types/index.ts`

4. **Problemas de estilos**
   - Verificar que Bootstrap esté importado correctamente
   - Revisar variables CSS en `src/styles/index.css`

### Logs de Desarrollo
Habilitar logs detallados en `.env.local`:
```env
VITE_ENABLE_LOGS=true
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo
- Revisar la documentación del backend

## 🔄 Actualizaciones

Para mantener el proyecto actualizado:

```bash
# Actualizar dependencias
npm update

# Verificar vulnerabilidades
npm audit

# Corregir vulnerabilidades automáticamente
npm audit fix
```

---

**XMedical Frontend** - Sistema de Asistencia Médica Inteligente 