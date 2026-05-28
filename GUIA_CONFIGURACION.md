# 🚀 Guía de Configuración Rápida - XMedical

Guía paso a paso para configurar y ejecutar el sistema XMedical en tu máquina local.

## 📋 Checklist de Preparación

### ✅ Software Requerido
- [ ] **Python 3.11+** instalado
- [ ] **Node.js 18+** instalado
- [ ] **PostgreSQL 14+** instalado y ejecutándose
- [ ] **Tesseract OCR** instalado (opcional para OCR)

### ✅ Verificación Rápida
```bash
# Verificar Python
python --version

# Verificar Node.js
node --version

# Verificar PostgreSQL
psql --version

# Verificar Tesseract (opcional)
tesseract --version
```

## 🗄️ Paso 1: Configurar PostgreSQL

### 1.1 Instalar PostgreSQL
1. Descarga desde [postgresql.org](https://postgresql.org/)
2. Instala con **pgAdmin** incluido
3. **Anota la contraseña** del usuario `postgres`

### 1.2 Crear Base de Datos
```sql
-- Conectar como postgres
psql -U postgres

-- Crear base de datos
CREATE DATABASE xmedical;

-- Verificar creación
\l

-- Salir
\q
```

### 1.3 Verificar Conexión
```bash
# Probar conexión
psql -h localhost -U postgres -d xmedical
```

## 🐍 Paso 2: Configurar Backend Python

### 2.1 Navegar al Directorio
```bash
cd server
```

### 2.2 Crear Entorno Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2.3 Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2.4 Configurar Variables de Entorno
1. Copiar archivo de ejemplo:
   ```bash
   copy env.example config.env
   ```

2. Editar `config.env`:
   ```env
   # Base de Datos - CAMBIA LA CONTRASEÑA
   DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/xmedical
   
   # JWT - GENERA UNA CLAVE SEGURA
   JWT_SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui
   
   # Tesseract (opcional)
   TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

### 2.5 Probar Conexión
```bash
python test_db.py
```

### 2.6 Inicializar Base de Datos
```bash
python init_db.py
```

### 2.7 Iniciar Servidor Backend
```bash
python start_server.py
```

**✅ Backend listo en:** http://localhost:8000

## ⚛️ Paso 3: Configurar Frontend React

### 3.1 Navegar al Directorio
```bash
cd client
```

### 3.2 Instalar Dependencias
```bash
npm install
```

### 3.3 Configurar Variables de Entorno
```bash
# Copiar configuración
copy env.local .env.local
```

### 3.4 Iniciar Servidor Frontend
```bash
npm run dev
```

**✅ Frontend listo en:** http://localhost:3000

## 🎯 Paso 4: Verificar Sistema

### 4.1 URLs de Acceso
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

### 4.2 Credenciales por Defecto
- **Usuario**: admin
- **Contraseña**: admin123

### 4.3 Pruebas Rápidas
1. **Acceder al frontend**: http://localhost:3000
2. **Hacer login** con credenciales por defecto
3. **Verificar dashboard** cargue correctamente
4. **Probar API docs**: http://localhost:8000/docs

## 🔧 Scripts de Inicio Rápido

### Opción 1: Script Automático (Windows)
```bash
# Desde el directorio raíz
start_xmedical.bat
```

### Opción 2: Inicio Manual
```bash
# Terminal 1 - Backend
cd server
venv\Scripts\activate
python start_server.py

# Terminal 2 - Frontend
cd client
npm run dev
```

## 🐛 Solución de Problemas Comunes

### ❌ Error: "PostgreSQL no está ejecutándose"
```bash
# Windows - Verificar servicio
services.msc
# Buscar "PostgreSQL" y asegurar que esté "Running"

# Reiniciar servicio
net stop postgresql
net start postgresql
```

### ❌ Error: "No se puede conectar a la base de datos"
```bash
# Verificar credenciales en config.env
# Probar conexión manual
psql -h localhost -U postgres -d xmedical

# Si falla, verificar:
# 1. PostgreSQL ejecutándose
# 2. Contraseña correcta
# 3. Base de datos 'xmedical' existe
```

### ❌ Error: "Module not found"
```bash
# Backend - Reinstalar dependencias
cd server
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall

# Frontend - Reinstalar dependencias
cd client
rm -rf node_modules package-lock.json
npm install
```

### ❌ Error: "Tesseract not found"
```bash
# Instalar Tesseract OCR
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Verificar ruta en config.env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

## 📊 Verificación Final

### ✅ Checklist de Verificación
- [ ] PostgreSQL ejecutándose en puerto 5432
- [ ] Base de datos 'xmedical' creada
- [ ] Backend iniciado en http://localhost:8000
- [ ] Frontend iniciado en http://localhost:3000
- [ ] Login exitoso con admin/admin123
- [ ] Dashboard carga correctamente
- [ ] API docs accesible en /docs

### 🎉 ¡Sistema Listo!
Tu sistema XMedical está configurado y funcionando correctamente.

## 🔒 Próximos Pasos de Seguridad

1. **Cambiar contraseña del administrador**
2. **Configurar HTTPS** para producción
3. **Actualizar JWT_SECRET_KEY**
4. **Configurar backup** de base de datos
5. **Revisar logs** de seguridad

---

**¿Necesitas ayuda?** Consulta el README.md principal o abre un issue en GitHub. 