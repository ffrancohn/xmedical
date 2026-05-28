# 🏥 XMedical - Sistema de Asistencia Médica Inteligente

Sistema completo de verificación de identidad y asistencia médica inteligente con backend Python FastAPI y frontend React TypeScript.

## 🚀 Características Principales

### 🔐 Autenticación y Seguridad
- **JWT Authentication** con refresh tokens
- **Role-based Access Control** (Admin, Usuario, Médico)
- **Password hashing** con bcrypt
- **Middleware de autenticación** personalizado

### 📄 Gestión de Documentos
- **OCR inteligente** para extracción de datos de documentos
- **Verificación facial** con reconocimiento biométrico
- **Validación automática** de documentos de identidad
- **Almacenamiento seguro** de archivos

### 👥 Gestión de Usuarios
- **Perfiles de usuario** con roles específicos
- **Gestión de beneficiarios** y dependientes
- **Direcciones múltiples** por usuario
- **Validación avanzada** de datos personales

### 🏥 Centros Médicos
- **Registro de centros médicos** y clínicas
- **Información de contacto** y ubicación
- **Gestión de horarios** y servicios

### 💬 Sistema de Feedback
- **Encuestas de satisfacción** personalizables
- **Análisis de respuestas** en tiempo real
- **Reportes automáticos** de calidad

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web moderno
- **SQLModel** - ORM con SQLAlchemy y Pydantic
- **PostgreSQL** - Base de datos principal
- **JWT** - Autenticación de tokens
- **Pytesseract** - OCR para documentos
- **OpenCV** - Procesamiento de imágenes
- **Pillow** - Manipulación de imágenes

### Frontend
- **React 18** - Biblioteca de UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool moderno
- **Bootstrap 5** - Framework CSS
- **Radix UI** - Componentes accesibles
- **TanStack Query** - Gestión de estado del servidor
- **Wouter** - Enrutamiento ligero
- **React Hook Form** - Formularios eficientes
- **Zod** - Validación de esquemas
- **Lucide React** - Iconos modernos

## 📋 Requisitos del Sistema

### Software Requerido
- **Python 3.11+** - [Descargar](https://python.org/)
- **Node.js 18+** - [Descargar](https://nodejs.org/)
- **PostgreSQL 14+** - [Descargar](https://postgresql.org/)
- **Tesseract OCR** - [Descargar](https://github.com/UB-Mannheim/tesseract/wiki)

### Hardware Recomendado
- **RAM**: 4GB mínimo, 8GB recomendado
- **Almacenamiento**: 2GB de espacio libre
- **Procesador**: Dual-core mínimo

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Windows)

1. **Clona el repositorio**:
   ```bash
   git clone <repository-url>
   cd xmedical
   ```

2. **Ejecuta el script de inicio**:
   ```bash
   start_xmedical.bat
   ```

3. **Sigue las instrucciones** en pantalla

### Opción 2: Instalación Manual

#### Paso 1: Configurar Backend

1. **Navega al directorio del servidor**:
   ```bash
   cd server
   ```

2. **Crea entorno virtual**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos**:
   - Instala PostgreSQL
   - Crea base de datos `xmedical`
   - Copia `env.example` a `config.env`
   - Edita `config.env` con tus credenciales

5. **Inicializa la base de datos**:
   ```bash
   python init_db.py
   ```

6. **Inicia el servidor**:
   ```bash
   python start_server.py
   ```

#### Paso 2: Configurar Frontend

1. **Navega al directorio del cliente**:
   ```bash
   cd client
   ```

2. **Instala dependencias**:
   ```bash
   npm install
   ```

3. **Configura variables de entorno**:
   ```bash
   copy env.local .env.local
   ```

4. **Inicia el servidor de desarrollo**:
   ```bash
   npm run dev
   ```

## ⚙️ Configuración Detallada

### Base de Datos PostgreSQL

1. **Instalar PostgreSQL**:
   - Descarga desde [postgresql.org](https://postgresql.org/)
   - Instala con pgAdmin incluido
   - Anota la contraseña del usuario `postgres`

2. **Crear base de datos**:
   ```sql
   CREATE DATABASE xmedical;
   ```

3. **Configurar conexión** en `server/config.env`:
   ```env
   DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/xmedical
   ```

### Tesseract OCR

1. **Instalar Tesseract**:
   - Windows: Descarga desde [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt install tesseract-ocr`
   - Mac: `brew install tesseract`

2. **Configurar ruta** en `server/config.env`:
   ```env
   TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

### Variables de Entorno

#### Backend (`server/config.env`)
```env
# Base de Datos
DATABASE_URL=postgresql://postgres:password@localhost:5432/xmedical

# JWT
JWT_SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# Tesseract
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

#### Frontend (`client/.env.local`)
```env
VITE_API_URL=http://localhost:8000
VITE_DEV_MODE=true
VITE_ENABLE_LOGS=true
VITE_APP_NAME=XMedical
VITE_APP_VERSION=1.0.0
VITE_ENABLE_BIOMETRIC=true
VITE_OCR_ENDPOINT=/biometric/ocr/process
VITE_FACIAL_ENDPOINT=/biometric/facial/verify
VITE_UPLOAD_ENDPOINT=/upload/
VITE_MAX_FILE_SIZE=10485760
```

## 🎯 Uso del Sistema

### Acceso Inicial
- **URL**: http://localhost:3000
- **Usuario**: admin
- **Contraseña**: admin123

### Funcionalidades Principales

#### 🔐 Autenticación
- Registro de nuevos usuarios
- Login con JWT
- Recuperación de contraseña
- Gestión de sesiones

#### 📄 Documentos
- Subida de documentos de identidad
- OCR automático para extracción de datos
- Verificación de autenticidad
- Almacenamiento seguro

#### 👤 Perfil de Usuario
- Información personal completa
- Gestión de direcciones
- Beneficiarios y dependientes
- Preferencias de contacto

#### 🏥 Centros Médicos
- Registro de centros médicos
- Información de contacto
- Servicios disponibles
- Horarios de atención

#### 💬 Feedback
- Encuestas de satisfacción
- Análisis de respuestas
- Reportes de calidad
- Mejoras continuas

## 🔧 Scripts Útiles

### Backend
```bash
# Verificar conexión a base de datos
python test_db.py

# Inicializar base de datos
python init_db.py

# Iniciar servidor de desarrollo
python start_server.py

# Ejecutar tests
python -m pytest
```

### Frontend
```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Construir para producción
npm run build

# Ejecutar tests
npm test
```

## 📚 Documentación API

Una vez iniciado el backend, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Solución de Problemas

### Error de Conexión a Base de Datos
```bash
# Verificar que PostgreSQL esté ejecutándose
# Windows
services.msc  # Buscar "PostgreSQL"

# Verificar credenciales en config.env
# Probar conexión manual
psql -h localhost -U postgres -d xmedical
```

### Error de Tesseract
```bash
# Verificar instalación
tesseract --version

# Verificar ruta en config.env
# Windows: C:\Program Files\Tesseract-OCR\tesseract.exe
# Linux: /usr/bin/tesseract
```

### Error de Dependencias Python
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error de Dependencias Node.js
```bash
# Limpiar cache
npm cache clean --force

# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

## 🔒 Seguridad

### Recomendaciones
- Cambia la contraseña del administrador por defecto
- Usa HTTPS en producción
- Configura firewall apropiado
- Mantén dependencias actualizadas
- Usa variables de entorno para secretos

### Configuración de Producción
- Configura `DEBUG=false`
- Usa base de datos PostgreSQL en servidor dedicado
- Configura CORS apropiadamente
- Usa proxy reverso (nginx)
- Configura SSL/TLS

## 📞 Soporte

### Recursos
- **Documentación**: `/docs` en el servidor
- **Issues**: GitHub Issues
- **Wiki**: Documentación detallada

### Contacto
- **Email**: soporte@xmedical.com
- **Telegram**: @xmedical_support

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**XMedical** - Transformando la asistencia médica con tecnología inteligente 🏥✨ 