# Doc 25 — Gemelo digital de la clínica: qué es aquí y cómo llegar

El objetivo declarado es «una especie de gemelo digital de una clínica», no completo. Este documento
define qué significa en XMedical, mide la distancia con lo que hay hoy y propone tres incrementos con
pantallas por perfil.

## 1. Cuatro niveles de fidelidad

| Nivel | Qué añade | Señal de que se alcanzó |
|---|---|---|
| **0 — Tablero** | Métricas y listas | Hay números, pero no hay espacio |
| **1 — Plano** | La clínica como espacio: salas, estaciones, capacidad | Se ve **dónde** pasa cada cosa |
| **2 — Plano vivo** | Estado por sala y por persona en tiempo real (derivado de la operación, sin sensores) | El plano cambia solo cuando la clínica cambia |
| **3 — Simulación** | Escenarios *what-if* sobre el modelo | Se puede preguntar «¿y si abro otra consulta?» |

«Gemelo digital» en sentido estricto es el nivel 3 con datos sincronizados. Lo razonable para este
producto es **llegar a 2 y hacer 3 en modo consulta** (simulación con datos históricos, no en vivo).

## 2. Dónde está XMedical hoy: nivel 1,2

Lo que ya existe y sirve de cimiento:

- **Máquina de estados real**: `Cita.estado` (`pendiente → confirmada → en_espera → atendida`, más
  `cancelada`) y `Preclinica` (triaje, signos, alertas) y `Consulta` (cierre). El *hilo* del día ya
  agrupa esos estados en estaciones: agendar, recibir, medir, atender, derivar.
- **Recursos con tiempo**: `Horario` por profesional y día, `Especialidad.duracion_consulta_minutos`.
- **Predicción**: `apps/ia_predictiva` (ausentismo, demanda, riesgo crónico).
- **Una escena isométrica** del consultorio del médico (doc 24) que ya es un plano vivo de *su* sala.

Lo que falta para el gemelo:

| Falta | Por qué importa |
|---|---|
| **Espacios** (salas, consultorios, boxes, laboratorio) con capacidad y posición | Sin espacios no hay plano; hoy la clínica es una lista de citas |
| **Asignación** cita → sala y profesional → sala | El plano no puede mostrar quién está dónde |
| **Historial de transiciones** (`cita_id`, de estado, a estado, cuándo) | Sin marcas de tiempo por etapa no hay esperas, cuellos de botella ni simulación |
| **Capacidad y ocupación** por sala/equipo | El gemelo debe saber si una sala está llena, no solo si hay citas |
| **Equipos** (ecógrafo, laboratorio) y su estado | Un gemelo clínico sin recursos físicos es un calendario |

## 3. Pantallas por perfil (qué ve cada uno en el gemelo)

| Perfil | Pantalla del gemelo | Qué responde |
|---|---|---|
| **Dirección / administración** | Plano de planta con ocupación por sala, colas, tiempo medio de espera, semáforo de capacidad | «¿Dónde se atasca la clínica hoy?» |
| **Recepción** | Plano operativo: llegadas, quién está en sala, quién lleva más esperando, salas libres | «¿A dónde mando a este paciente?» |
| **Enfermería** | Estación de signos: cola de triaje, alertas vitales, salas esperando preclínica | «¿A quién mido ahora?» |
| **Médico / especialista** | Su consultorio (ya existe, doc 24) + contexto del piso: quién viene en camino | «¿Quién es el siguiente y cuánto falta?» |
| **Epidemiología / calidad** | Mapa de calor por diagnóstico y por sala, tendencias | «¿Qué está pasando en la población?» |
| **Paciente (portal)** | Su posición en la cola y tiempo estimado | «¿Cuánto falta para mi turno?» |
| **Superadmin** | Vista multi-sede: comparación de ocupación entre instituciones | «¿Qué sede necesita refuerzo?» |

Regla de privacidad: en las vistas colectivas se muestran **iniciales, estado y tiempo**, nunca
nombre completo ni motivo de consulta. El detalle con PHI queda en las pantallas por rol.

## 4. Tres incrementos

### I1 — Plano vivo (base del gemelo) · ~1 semana

1. Modelo `Espacio` (`tipo`: consultorio/laboratorio/triaje/recepción, `capacidad`, `posicion` en el
   plano, `institucion`, `activo`) y `AsignacionCita` (cita → espacio) o `Cita.espacio` directo.
2. Vista **Dirección**: plano de planta con una tarjeta por espacio: ocupado/libre, paciente en
   curso, minutos de espera, semáforo por capacidad.
3. Vista **Recepción**: el mismo plano en modo operativo, con acciones (asignar sala, llamar).
4. Datos derivados de lo que ya hay: `Cita.estado` + `Preclinica` + `Consulta`. Cero sensores.

### I2 — Flujo y tiempos · ~1 semana

1. `CitaEvento` (cita, estado anterior, estado nuevo, `ocurrido_en`, usuario): se escribe en cada
   transición; un `signal`/servicio evita tocar todas las vistas.
2. Métricas por estación: espera media/p90, tiempo de consulta, tiempo de derivación.
3. Plano con **heatmap temporal** y alertas de atasco («3 salas en espera > 30 min»).
4. Portal del paciente: posición y estimación (regla simple, sin promesas).

### I3 — Simulación (what-if) · ~2 semanas

1. Motor simple: capacidad × horario × `duracion_consulta_minutos` × demanda histórica
   (`ia_predictiva`).
2. Escenarios: «+1 consultorio», «mover 2 citas a la tarde», «ausentismo 15 %».
3. Resultado comparado: espera media, ocupación, citas no atendidas. Se guarda el escenario.

## 5. Cómo encaja con lo ya construido

- La **escena blueprint** del médico es la primera pieza del gemelo: un espacio con estado.
  El patrón se repite para el resto de la clínica en vista de planta (no isométrica: un plano de
  arquitecto 2D es más legible para dirección y cuesta mucho menos que 20 escenas 3D).
- El **hilo del día** ya es, conceptualmente, el flujo del gemelo; I2 lo convierte en serie temporal.
- `atlas_explore` y `hilo_del_dia` siguen siendo la fuente de agregados; el gemelo solo añade
  espacio y tiempo.

## 6. Riesgos

1. **PHI en pantallas compartidas**: en recepción el plano se ve de pie, en un mostrador. Iniciales y
   estado, nunca diagnóstico.
2. **Mantenimiento del plano**: cada institución necesita su planta. Se resuelve con un editor
   mínimo (arrastrar salas sobre una cuadrícula) o cargando un JSON por sede.
3. **Expectativa de tiempo real**: sin sensores, el «tiempo real» es el de las transiciones que el
   personal ya registra. Si no se marcan llegadas, el gemelo miente. Hay que hacer que marcar sea
   un clic (botón «llegó» en recepción).
4. **Simulación mal calibrada**: vender precisión que no hay. Etiquetar como estimación y mostrar el
   rango.

## 7. Recomendación

Empezar por **I1 con la vista de Dirección**, porque es la que justifica el gemelo ante quien decide
(ocupación y cuellos de botella) y porque obliga a modelar `Espacio`, que es la pieza que falta.
Recepción entra en el mismo incremento con el mismo plano y tres acciones.

Después I2 (tiempos) y, si el uso se sostiene, I3 (simulación).
