# XMedical - Documentacion Fase 1

## Resumen

La Fase 1 de XMedical implementa un MVP de gestion clinica multi-tenant para atencion de primer nivel. El sistema permite administrar pacientes, citas, preclinica, consulta medica guiada, diagnosticos CIE-10, historia clinica, usuarios por rol, preferencias visuales y una vista superadmin del proveedor.

## Tecnologia

| Capa | Tecnologia |
|---|---|
| Backend | Django 4.2 |
| Frontend | Django Templates, Tailwind CSS, DaisyUI |
| Base de datos | PostgreSQL |
| Tareas futuras | Celery y Redis |
| Autenticacion | Django Auth y sesiones |
| Contenedores | Docker Compose |

## Roles

| Rol | Alcance |
|---|---|
| Superadmin | Administrador del proveedor del sistema. Puede ver todas las instituciones, generar respaldos y restaurar datos. |
| Admin | Administrador de una clinica/institucion. Gestiona usuarios y configuracion de su institucion. |
| Medico | Atiende citas y completa el flujo de consulta. |
| Enfermera | Registra preclinica y signos vitales. |
| Recepcionista | Registra pacientes y agenda citas. |

## Multi-tenant

El sistema soporta multiples instituciones mediante el modelo `Institucion`.

La identificacion de clinica se realiza por subdominio usando `TenantMiddleware`.

Ejemplo:

```text
demo.xmedical.local
```

Para desarrollo local, si no hay subdominio, el sistema usa una institucion activa como fallback para facilitar pruebas.

## Modulos implementados

### 1. Instituciones

Modelo base para separar clinicas o instituciones.

Campos principales:

- Nombre
- Subdominio
- Tipo: publica o privada
- Configuracion JSON
- Estado activo/inactivo

### 2. Especialidades

Permite registrar especialidades asociadas a una institucion.

Campos principales:

- Institucion
- Nombre
- Codigo
- Nivel: primero o segundo
- Duracion de consulta
- Estado activo/inactivo

### 3. Profesionales y roles

Cada profesional esta vinculado a un usuario de Django y una institucion.

Tipos disponibles:

- Admin
- Medico
- Enfermera
- Recepcionista

### 4. Pacientes

El modulo de pacientes permite listar, crear, editar, ver detalle e ir a historia clinica.

Datos incluidos:

- Documento
- Nombre
- Apellido
- Fecha de nacimiento
- Sexo
- Telefono movil
- Telefono fijo
- Correo electronico
- Direccion
- Ciudad
- Departamento
- Contacto de emergencia
- Telefono de emergencia
- Observaciones
- Estado activo/inactivo

Opciones disponibles:

- Buscar paciente por documento, nombre o apellido.
- Crear paciente.
- Ver informacion del paciente en modo solo lectura.
- Editar paciente.
- Abrir historia clinica.

En perfil superadmin:

- Se puede filtrar por una o varias instituciones.
- Se muestra la clinica a la que pertenece cada paciente.

### 5. Citas y agenda

El modulo de citas permite gestionar agendamiento especifico por fecha y hora.

Datos principales:

- Institucion
- Paciente
- Profesional
- Fecha
- Hora
- Estado
- Tipo de agendamiento

Estados:

- Pendiente
- Confirmada
- Cancelada
- Atendida

Opciones disponibles:

- Listar citas.
- Agendar cita.
- Cancelar cita.
- Ver agenda en multiples formatos.

Formatos de agenda:

- Lista
- Dia
- Semana
- Mes
- 2 meses
- 3 meses

En perfil superadmin:

- Se puede filtrar por una o varias instituciones.
- La agenda conserva el filtro al cambiar entre vistas.
- Se muestra la institucion en tablas, calendario y tarjetas.

### 6. Preclinica

El modulo de preclinica permite registrar signos vitales antes de la consulta medica.

Datos registrados:

- Presion arterial sistolica
- Presion arterial diastolica
- Frecuencia cardiaca
- Temperatura
- Saturacion de oxigeno
- Peso
- Talla
- IMC calculado
- Motivo de consulta
- Triaje

Alertas automaticas:

- Presion sistolica elevada
- Presion diastolica elevada
- Fiebre
- Saturacion de oxigeno baja

En perfil superadmin:

- Se puede filtrar por una o varias instituciones.
- Se muestra la institucion de cada cita.

### 7. Consulta medica guiada

La consulta medica se implementa como un wizard de 7 pasos.

Pasos:

| Paso | Nombre | Funcion |
|---|---|---|
| 1 | Revisar preclinica | Muestra signos vitales y alertas. |
| 2 | Motivo de consulta | Registra motivo principal. |
| 3 | Anamnesis | Registra historia clinica del episodio. |
| 4 | Examen fisico | Registra hallazgos del examen. |
| 5 | Diagnostico | Permite agregar diagnostico CIE-10. |
| 6 | Plan terapeutico | Registra plan y conducta. |
| 7 | Resumen | Muestra resumen y finaliza consulta. |

Conductas disponibles:

- Alta medica
- Cita subsiguiente
- Referencia

Al finalizar la consulta, la cita queda marcada como atendida.

### 8. Diagnostico CIE-10

El MVP incluye un buscador basico de codigos CIE-10 con una lista inicial.

Ejemplos incluidos:

- I10 - Hipertension esencial primaria
- E11 - Diabetes mellitus tipo 2
- J00 - Rinofaringitis aguda
- N39.0 - Infeccion de vias urinarias
- R51 - Cefalea

### 9. Historia clinica

La historia clinica muestra consultas previas de un paciente.

Incluye:

- Fecha de consulta
- Motivo
- Plan terapeutico
- Diagnosticos registrados

### 10. Configuracion visual por usuario

Cada usuario puede seleccionar un tema visual DaisyUI.

Ruta:

```text
/auth/preferencias/
```

Temas disponibles:

- Garden
- Claro
- Oscuro
- Corporativo
- Esmeralda
- Suave
- Amarillo
- Invierno
- Noche
- Bosque
- Aqua
- Minimalista

### 11. Superadmin

El superadmin representa al proveedor del sistema, no a una clinica especifica.

Ruta:

```text
/superadmin/
```

Opciones:

- Ver dashboard global.
- Ver instituciones registradas.
- Ver metricas globales:
  - instituciones
  - pacientes
  - citas
  - consultas
- Ver metricas por institucion.
- Crear respaldos globales.
- Crear respaldos por institucion.
- Restaurar archivos JSON.
- Ver bitacora de respaldos/restauraciones.

### 12. Respaldos y restauraciones

Los respaldos se generan en la carpeta:

```text
backups/
```

Tipos:

- Respaldo global
- Respaldo por institucion

La restauracion usa `loaddata`, por lo tanto es una restauracion logica por fixtures JSON.

Nota importante:

Para produccion se recomienda agregar validacion adicional, confirmacion doble y respaldo fisico de PostgreSQL con `pg_dump`.

## Usuarios de prueba

Archivo:

```text
USUARIOS_PRUEBA.md
```

Usuarios incluidos:

| Rol | Usuario | Contrasena |
|---|---|---|
| Superadmin | `superadmin.demo` | `Xmedical123!` |
| Admin | `admin.demo` | `Xmedical123!` |
| Medico | `medico.demo` | `Xmedical123!` |
| Enfermera | `enfermera.demo` | `Xmedical123!` |
| Recepcionista | `recepcion.demo` | `Xmedical123!` |

## Datos de prueba

Fixture:

```text
fixtures/initial_data.json
```

Incluye:

- 1 institucion demo
- 1 especialidad
- 5 usuarios de prueba
- 10 pacientes sinteticos
- 3 citas
- 1 preclinica

Cargar datos:

```powershell
python manage.py loaddata fixtures/initial_data.json
```

## Docker y base de datos

El archivo `docker-compose.yml` incluye:

- PostgreSQL
- Redis
- Web Django
- Celery

La base de datos usa el volumen:

```text
postgres_data
```

Por eso, los datos no se pierden al ejecutar:

```powershell
docker compose down
```

Los datos si se eliminan al ejecutar:

```powershell
docker compose down -v
```

## Scripts disponibles

En la raiz existen scripts para manejar Docker:

```text
levantar_xmedical.bat
bajar_xmedical.bat
reiniciar_xmedical.bat
```

Levantar servicios:

```powershell
.\levantar_xmedical.bat
```

Bajar servicios:

```powershell
.\bajar_xmedical.bat
```

Reiniciar servicios:

```powershell
.\reiniciar_xmedical.bat
```

## Comandos de instalacion inicial

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d db redis
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py runserver
```

Acceso:

```text
http://localhost:8000/auth/login/
```

## Alcance actual de Fase 1

Incluido:

- Multi-tenant basico.
- Usuarios y roles.
- Pacientes.
- Citas.
- Agenda multi-vista.
- Preclinica.
- Consulta medica guiada.
- Diagnostico CIE-10 basico.
- Historia clinica.
- Configuracion visual por usuario.
- Superadmin proveedor.
- Respaldos/restauraciones logicas.

Pendiente para fases siguientes:

- Agendamiento flexible automatico.
- Referencias y contrarreferencias.
- Variables clinicas por especialidad.
- QR para recetas, examenes y check-in.
- Recordatorios por correo.
- Integracion IA con OpenAI/OpenRouter.
- OCR/vision para documentos.
- Dashboards avanzados por perfil.
