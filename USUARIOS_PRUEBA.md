# Usuarios de prueba - XMedical MVP

Todos los usuarios usan la misma contrasena:

```text
Xmedical123!
```

## Acceso

URL de login:

```text
http://localhost:8000/auth/login/
```

## Credenciales

| Rol | Usuario | Contrasena | Nombre |
|---|---|---|---|
| Superadmin proveedor | `superadmin.demo` | `Xmedical123!` | Sofia Proveedor |
| Admin | `admin.demo` | `Xmedical123!` | Ana Administradora |
| Medico | `medico.demo` | `Xmedical123!` | Dr. Carlos Mendez |
| Enfermera | `enfermera.demo` | `Xmedical123!` | Lic. Lucia Reyes |
| Recepcionista | `recepcion.demo` | `Xmedical123!` | Marta Lopez |

## Que probar con cada usuario

### Superadmin proveedor

- Ver dashboard global del sistema.
- Ver instituciones, pacientes, citas y consultas por institucion.
- Crear respaldos globales o por institucion.
- Restaurar archivos JSON de respaldo.

Ruta util:

```text
http://localhost:8000/superadmin/
```

### Admin

- Entrar al sistema.
- Registrar nuevos usuarios desde:

```text
http://localhost:8000/auth/registro/
```

- Acceder al admin de Django si tiene permisos suficientes:

```text
http://localhost:8000/admin/
```

### Recepcionista

- Ver pacientes.
- Crear pacientes.
- Agendar citas.
- Cancelar citas.

Rutas utiles:

```text
http://localhost:8000/pacientes/
http://localhost:8000/citas/
http://localhost:8000/citas/agendar/
```

### Enfermera

- Ver pacientes en espera para preclinica.
- Registrar signos vitales.
- Revisar alertas por presion alta, fiebre o saturacion baja.

Ruta util:

```text
http://localhost:8000/preclinica/
```

### Medico

- Ver agenda del dia.
- Atender cita con wizard de 7 pasos.
- Registrar motivo, anamnesis, examen fisico, diagnostico CIE-10 y plan terapeutico.
- Ver historia clinica del paciente.

Rutas utiles:

```text
http://localhost:8000/dashboard/
http://localhost:8000/pacientes/
```

## Datos incluidos

El fixture `fixtures/initial_data.json` incluye:

- 1 institucion: Clinica Demo
- 1 especialidad: Medicina General
- 5 usuarios de prueba
- 10 pacientes sinteticos
- 3 citas para el dia 2026-06-04
- 1 registro de preclinica

Para cargar o recargar los datos:

```powershell
python manage.py loaddata fixtures/initial_data.json
```
