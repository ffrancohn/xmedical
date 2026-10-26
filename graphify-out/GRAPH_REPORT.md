# Graph Report - xmedical  (2026-10-26)

## Corpus Check
- 298 files · ~193,152 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2562 nodes · 4774 edges · 205 communities (148 shown, 57 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 443 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e62335a1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AIConfigurationError
- time
- views.py
- UserPreference
- urls.py
- ausentismo.py
- views.py
- views.py
- DOCUMENTO 7: SEGURIDAD
- models.py
- QRService
- services.py
- DOCUMENTO 1: VISIÓN DEL PRODUCTO (ACTUALIZADO)
- DOCUMENTO 2: ALCANCE DEL MVP POR FASES (ACTUALIZADO CON MULTI-TENANT)
- Flujos Funcionales y Casos de Uso
- 3. Pruebas iniciales
- Análisis de Interfaz de Usuario — XMedical
- DOCUMENTO 12: SPRINT BACKLOG
- Informe de verificación — XMedical
- DOCUMENTO 8: MODELO DE NEGOCIO
- TenantMiddleware
- DOCUMENTO 11: PLAN DE DESPLIEGUE
- DOCUMENTO 4: ARQUITECTURA DE ALTO NIVEL
- tenant_transfer.py
- Documento de Requerimientos Técnicos (TRD)
- DOCUMENTO 10: PLAN DE PRUEBAS
- current_institucion
- DOCUMENTO 9: INTEGRACIONES
- 7. Servicios internos
- backup_utils.py
- 3. TABLAS COMPLETAS
- 9. Requerimientos funcionales
- Profesional
- TestCase
- DOCUMENTO 15: RECEPCIÓN VIRTUAL OMNICANAL
- 3. HISTORIAS DE USUARIO POR ÉPICA
- Modulos implementados
- auth_client
- DOCUMENTO 5: DIAGRAMAS DE FLUJO
- 3. Pantallas propuestas
- DOCUMENTO 0: DESCRIPCIÓN GENERAL DEL PROYECTO
- git-helper.ps1
- views.py
- permissions.py
- views.py
- DOCUMENTO 13: APP MÓVIL Y API REST
- test_fase1.py
- 5. BACKEND Y ESQUEMA DE DATOS
- XMedical - Sistema de Gestión Clínica Multi-tenant
- 4. TRD — DOCUMENTO DE REQUERIMIENTOS TÉCNICOS
- Consulta
- Informe de verificación operativa — XMedical
- 1. PRD — DOCUMENTO DE REQUERIMIENTOS DEL PRODUCTO
- 2. FLUJO DE LA APLICACIÓN
- APIPacientesTests
- 3. DISEÑO UI/UX
- 6. PLAN DE IMPLEMENTACIÓN
- Guía de Configuración - XMedical
- ConsultaWizardTests
- epidemiologia.py
- Prompts divididos para XMedical Fase 2
- Preclinica
- Guía rápida de uso (visión 0.1b)
- Informe de verificación — XMedical
- Cita
- locustfile.py
- tests.py
- PacienteFunctionalTests
- PreclinicaAlertasTests
- Visión de producto redefinida
- Que probar con cada usuario
- CitaFunctionalTests
- xmedical_tags.py
- README.md
- decorators.py
- Checklist UAT — XMedical
- Cursor Cloud specific instructions
- Informes de verificación
- OpenAPITests
- Checklist de seguridad — XMedical
- generate_report.sh
- test_referencias.py
- RBACStrictTests
- DocumentoOCRLog
- Documentación XMedical
- Solución de problemas
- run_all_verifications.sh
- verify_smoke.sh
- CoreConfig
- 0004_enable_rls.py
- 0005_referencias_rls.py
- 0006_qr_rls.py
- 0007_variables_clinicas_rls.py
- 0008_notificaciones_rls.py
- 0009_pacientes_ocr_rls.py
- 0010_portal_paciente_rls.py
- 0011_ia_predictiva_rls.py
- IaPredictivaConfig
- uv_lib.sh
- verify_infra.sh
- verify_security_headers.sh
- wizard.js
- conftest.py
- test_flujo_enfermera.py
- test_flujo_medico_wizard.py
- test_flujo_recepcion.py
- test_login.py
- test_superadmin_backup.py
- ApiConfig
- AuthAppConfig
- CitasConfig
- ConsultaConfig
- DashboardsConfig
- NotificacionesConfig
- PacientesConfig
- PortalPacienteConfig
- PreclinicaConfig
- QrConfig
- ReferenciasConfig
- VariablesClinicasConfig
- verify_security_static.sh
- verify_ssl.sh
- 0001_initial.py
- 0002_tema_vital_default.py
- 0001_initial.py
- 0002_fase1_cierre.py
- 0001_initial.py
- 0001_initial.py
- 0002_backuplog.py
- 0003_fase1_cierre.py
- 0001_initial.py
- 0001_initial.py
- 0001_initial.py
- 0002_contacto_extendido.py
- 0003_documentoocrlog.py
- 0001_initial.py
- 0001_initial.py
- 0001_initial.py
- 0001_initial.py
- bajar_xmedical.sh
- levantar_xmedical.sh
- run_tests.sh
- sync_uv.sh
- verify_security_zap.sh
- setup_venv.sh
- start_xmedical.sh
- xmedical
- ocr_views.py
- Informe de verificación — XMedical
- Carpeta de evidencia — XMedical
- _post_chat_completion
- XMedical · Atlas del sistema
- 3. TIPOS DE PRUEBAS
- can_manage_pacientes
- riesgo_cronico.py
- Prototipo navegable · aspecto Atlas
- 0003_remove_tema_vital.py
- DashboardServicesTests
- RoleRoutingTests
- EpidemiologiaViewsTests
- IaPredictivaConfig

## God Nodes (most connected - your core abstractions)
1. `Cita` - 73 edges
2. `auth_client()` - 59 edges
3. `Institucion` - 55 edges
4. `Paciente` - 52 edges
5. `Profesional` - 48 edges
6. `current_institucion()` - 48 edges
7. `Consulta` - 40 edges
8. `AIConfigurationError` - 29 edges
9. `Preclinica` - 28 edges
10. `Especialidad` - 27 edges

## Surprising Connections (you probably didn't know these)
- `test_ai_client_not_available_without_keys()` --indirect_call--> `AIConfigurationError`  [INFERRED]
  tests/test_ai_services.py → apps/core/ai_services.py
- `test_ollama_provider_requires_model()` --indirect_call--> `AIConfigurationError`  [INFERRED]
  tests/test_ai_services.py → apps/core/ai_services.py
- `test_openai_provider_requires_api_key()` --indirect_call--> `AIConfigurationError`  [INFERRED]
  tests/test_ai_services.py → apps/core/ai_services.py
- `WizardOllamaIntegrationTests` --uses--> `AIConfigurationError`  [INFERRED]
  tests/test_wizard_ia_fase3.py → apps/core/ai_services.py
- `WizardOllamaIntegrationTests` --uses--> `AIClient`  [INFERRED]
  tests/test_wizard_ia_fase3.py → apps/core/ai_services.py

## Import Cycles
- 1-file cycle: `xmedical/celery.py -> xmedical/celery.py`

## Communities (205 total, 57 thin omitted)

### Community 0 - "AIConfigurationError"
Cohesion: 0.12
Nodes (17): AIConfigurationError, Falta configuracion o credenciales para el proveedor IA., OCRResult, _parse_ai_json(), parse_document_text(), _parse_documento(), _parse_fecha(), Exception (+9 more)

### Community 1 - "time"
Cohesion: 0.05
Nodes (55): CitaFlexibleForm, CitaForm, FlexibleAgendamientoService, Exception, No hay turnos libres en el rango solicitado., SinTurnosDisponiblesError, add_months(), build_month() (+47 more)

### Community 2 - "views.py"
Cohesion: 0.08
Nodes (32): AnamnesisForm, DiagnosticoForm, ExamenFisicoForm, Meta, MotivoForm, PlanForm, cie10_search(), ConsultaWizardView (+24 more)

### Community 3 - "UserPreference"
Cohesion: 0.07
Nodes (27): LogoutSerializer, XMedicalTokenObtainPairSerializer, LoginView, LogoutView, APIView, RefreshView, UserPreferenceAdmin, Meta (+19 more)

### Community 4 - "urls.py"
Cohesion: 0.08
Nodes (24): CitaSerializer, CitaUpdateSerializer, Meta, CitaViewSet, ConsultaCreateSerializer, ConsultaSerializer, Meta, ConsultaViewSet (+16 more)

### Community 5 - "ausentismo.py"
Cohesion: 0.26
Nodes (14): administracion_dashboard_data(), get_predictiva_config(), nivel_desde_probabilidad(), calcular_probabilidad_ausentismo(), guardar_prediccion_ausentismo(), predicciones_alerta(), reentrenar_ausentismo_institucion(), _tasa_cancelacion_institucion() (+6 more)

### Community 6 - "views.py"
Cohesion: 0.10
Nodes (24): current_institucion(), DocumentoIdentidadForm, Meta, PacienteForm, PacienteOCRReviewForm, PacientePublicForm, PacienteOCRReviewView, PacienteOCRUploadView (+16 more)

### Community 7 - "views.py"
Cohesion: 0.16
Nodes (21): get_profesional(), ContrarreferenciaAdmin, ReferenciaAdmin, ContrarreferenciaForm, Meta, ReferenciaAgendarForm, ReferenciaForm, ReferenciaRespuestaForm (+13 more)

### Community 8 - "DOCUMENTO 7: SEGURIDAD"
Cohesion: 0.04
Nodes (44): 10.1 Clasificación de incidentes, 10.2 Procedimiento de respuesta, 10.3 Contactos de emergencia, 10. RESPUESTA A INCIDENTES, 11. CUMPLIMIENTO NORMATIVO, 12. APROBACIÓN, 1. VISIÓN GENERAL, 2. CLASIFICACIÓN DE LA INFORMACIÓN (+36 more)

### Community 9 - "models.py"
Cohesion: 0.12
Nodes (14): Pruebas API REST (API-01..API-06)., Pruebas funcionales de autenticación (FUN-A*)., Pruebas funcionales de citas (FUN-C*)., DocumentoOCRLogAdmin, PacienteAdmin, DocumentoOCRLog, Meta, Paciente (+6 more)

### Community 10 - "QRService"
Cohesion: 0.12
Nodes (23): DocumentoQRAdmin, DocumentoQR, Exception, QRExpiradoError, QRNoEncontradoError, QRService, QRServiceError, QRYaUsadoError (+15 more)

### Community 11 - "services.py"
Cohesion: 0.10
Nodes (23): LogNotificacionAdmin, RecordatorioMedicamentoAdmin, LogNotificacion, RecordatorioMedicamento, cita_datetime(), _citas_candidatas(), citas_para_recordatorio(), enviar_recordatorio_cita() (+15 more)

### Community 12 - "DOCUMENTO 1: VISIÓN DEL PRODUCTO (ACTUALIZADO)"
Cohesion: 0.05
Nodes (38): 10. CAPACIDADES CLAVE DEL SISTEMA, 11. MÉTRICAS DE ÉXITO, 12. POSICIONAMIENTO ESTRATÉGICO, 13. CONCEPTOS CLAVE DEL DOMINIO (38 términos), 14. TECNOLOGÍAS CONFIRMADAS, 15. TIPOS DE INSTITUCIÓN SOPORTADOS, 16. HOJA DE RUTA DE EVOLUCIÓN, 17. RIESGOS Y MITIGACIONES (+30 more)

### Community 13 - "DOCUMENTO 2: ALCANCE DEL MVP POR FASES (ACTUALIZADO CON MULTI-TENANT)"
Cohesion: 0.05
Nodes (38): 10. RIESGOS DEL MVP (ACTUALIZADOS), 11. ALCANCE DEL PILOTO (validación) - ACTUALIZADO, 12. ENTREGABLES POR FASE (ACTUALIZADOS), 13. MÉTRICAS DE ÉXITO POR FASE (ACTUALIZADAS), 14. ESTRUCTURA DE PARAMETRIZACIÓN (MVP) - ACTUALIZADA, 15. HOJA DE RUTA DE EVOLUCIÓN COMPLETA (ACTUALIZADA), 16. APROBACIÓN, 1. DEFINICIÓN DEL MVP (+30 more)

### Community 14 - "Flujos Funcionales y Casos de Uso"
Cohesion: 0.05
Nodes (37): Actor, Alternativa A — Importar, Alternativa B — Capturar, Alternativas, Alternativas de duración, Casos de uso, CU-001. Crear proyecto, CU-002. Configurar proveedor (+29 more)

### Community 15 - "3. Pruebas iniciales"
Cohesion: 0.05
Nodes (37): 1. Estrategia de implementación, 2. Fases, 3. Pruebas iniciales, 4. Matriz de trazabilidad inicial, 5. Riesgos, 6. Versiones posteriores, Ciclo 0.1b (en curso — MVP redefinido), CP-001. Crear proyecto válido (+29 more)

### Community 16 - "Análisis de Interfaz de Usuario — XMedical"
Cohesion: 0.05
Nodes (37): 10. Problemas técnicos y de rendimiento, 11. Priorización de mejoras, 12. Stack recomendado para las mejoras, 1. Arquitectura de navegación, 2. Página de inicio (home) y landing, 3. Sistema de diseño y CSS, 4. Formularios, 5. Dashboards (+29 more)

### Community 17 - "DOCUMENTO 12: SPRINT BACKLOG"
Cohesion: 0.06
Nodes (35): 10. HITOS DEL SPRINT, 11.1 Entregables técnicos, 11.2 Entregables funcionales, 11. ENTREGABLES DEL SPRINT, 12. APROBACIÓN, 1. VISIÓN GENERAL, 2.1 Equipo de desarrollo (recomendado para MVP), 2.2 Capacidad ajustada por sprint (4 semanas = 160 horas) (+27 more)

### Community 18 - "Informe de verificación — XMedical"
Cohesion: 0.06
Nodes (32): 1. Resumen ejecutivo, 2.1 Correcciones de código, 2.2 Pruebas automatizadas, 2.3 Evidencia, 2.4 Endurecimiento Fase 1 (2026-07), 2. Implementado (2026-07), 3. Warnings aceptados (sin acción inmediata), 4. Planificado — Fase 1 (corto plazo, 1–2 semanas) (+24 more)

### Community 19 - "DOCUMENTO 8: MODELO DE NEGOCIO"
Cohesion: 0.06
Nodes (34): 10. ESTRATEGIA DE RETENCIÓN, 11. ANÁLISIS FODA (SWOT), 12. APROBACIÓN, 1. VISIÓN GENERAL, 2. BUSINESS MODEL CANVAS, 3. PROPUESTA DE VALOR POR SEGMENTO (DETALLADA), 4.1 Tamaño de mercado, 4.2 Competencia (+26 more)

### Community 20 - "TenantMiddleware"
Cohesion: 0.14
Nodes (8): XMedicalJWTAuthentication, reset_current_request(), set_current_request(), set_institucion_rls(), TenantMiddleware, CoreFunctionalTests, TenantMiddlewareTests, JWTAuthentication

### Community 21 - "DOCUMENTO 11: PLAN DE DESPLIEGUE"
Cohesion: 0.06
Nodes (32): 10. CRONOGRAMA DE DESPLIEGUE (FASE 1 - MVP), 11. APROBACIÓN, 1. VISIÓN GENERAL, 2.1 Entornos, 2.2 Estrategia de despliegue (Blue-Green), 2.3 Pipeline CI/CD (GitHub Actions), 2. ESTRATEGIA DE DESPLIEGUE, 3.1 Requisitos mínimos (MVP - 1 tenant) (+24 more)

### Community 22 - "DOCUMENTO 4: ARQUITECTURA DE ALTO NIVEL"
Cohesion: 0.06
Nodes (31): 10. DIAGRAMA DE SECUENCIA: CONSULTA MÉDICA, 11. MONITOREO Y OBSERVABILIDAD, 12. APROBACIÓN, 1.0 Estado de implementación (julio 2026), 1.1 Diagrama de arquitectura de alto nivel, 1. VISIÓN GENERAL DE LA ARQUITECTURA, 2. DECISIONES ARQUITECTÓNICAS CLAVE, 3.1 Capa de Presentación (Frontend) (+23 more)

### Community 23 - "tenant_transfer.py"
Cohesion: 0.28
Nodes (8): AlertaRiesgoCronicoAdmin, DemandaCitaAdmin, PrediccionAusentismoAdmin, AlertaRiesgoCronico, DemandaCita, Meta, PrediccionAusentismo, Pruebas de modelos predictivos (Fase 3).

### Community 24 - "Documento de Requerimientos Técnicos (TRD)"
Cohesion: 0.07
Nodes (29): 10. Manejo de errores, 11. Registro de actividad, 12.1 Estrategia para FFmpeg, 12. Empaquetado y distribución, 1. Objetivo técnico, 2. Arquitectura propuesta, 3. Tecnologías propuestas, 4.10 ImageManager / ImageService (v0.2 medios) (+21 more)

### Community 25 - "DOCUMENTO 10: PLAN DE PRUEBAS"
Cohesion: 0.10
Nodes (21): 10. MAPA DE CASOS IMPLEMENTADOS, 11. APROBACIÓN, 1. VISIÓN GENERAL, 2. ESTRATEGIA DE PRUEBAS, 4. HERRAMIENTAS DE PRUEBAS, 5. AMBIENTES DE PRUEBAS, 6.1 Por tipo de prueba, 6.2 Por severidad de bugs (+13 more)

### Community 26 - "current_institucion"
Cohesion: 0.19
Nodes (5): institution_filter_context(), Return institutions visible for list screens, with multi-select for superadmins., selected_instituciones(), hilo_del_dia(), Ocupación de la clínica. Cada cita activa cae en una estación; Medir repite la s

### Community 27 - "DOCUMENTO 9: INTEGRACIONES"
Cohesion: 0.07
Nodes (28): 10. APROBACIÓN, 1. VISIÓN GENERAL, 2. MAPA DE INTEGRACIONES, 3.1 Email (Recordatorios y notificaciones), 3.2 IA - Visión Artificial (Validación de Documentos), 3.3 IA - LLM (Sugerencia Diagnóstica), 3.4 Almacenamiento (Archivos), 3. INTEGRACIONES ACTUALES (MVP - Fase 2) (+20 more)

### Community 28 - "7. Servicios internos"
Cohesion: 0.07
Nodes (27): 1. Objetivo, 2. Entidades principales, 3.1 Tabla `PROJECT`, 3.2 Tabla `SCENE`, 3.3 Tabla `AUDIO_ASSET`, 3.4 Tabla `VIDEO_ASSET`, 3.5 Tabla `PROVIDER_CONFIG`, 3.6 Tabla `EXPORT` (+19 more)

### Community 29 - "backup_utils.py"
Cohesion: 0.15
Nodes (14): create_global_backup(), _mirror_to_remote(), restore_fixture(), rotate_old_backups(), run_scheduled_backups(), timestamp(), backup_database(), limpiar_logs() (+6 more)

### Community 30 - "3. TABLAS COMPLETAS"
Cohesion: 0.07
Nodes (26): 1. VISIÓN GENERAL, 2. DIAGRAMA ENTIDAD-RELACIÓN, 3.10 referencia, 3.11 log_auditoria, 3.1 institucion (Tenant), 3.2 especialidad, 3.3 profesional, 3.4 horario (+18 more)

### Community 31 - "9. Requerimientos funcionales"
Cohesion: 0.08
Nodes (25): 10. Requerimientos no funcionales, 11. Reglas de negocio, 12. Criterios de aceptación del MVP (redefinido 0.1b), 1. Introducción, 2. Objetivo general, 3. Objetivos específicos, 4. Problema que se desea resolver, 5. Usuarios objetivo (+17 more)

### Community 32 - "Profesional"
Cohesion: 0.15
Nodes (16): BackupLogAdmin, EspecialidadAdmin, HorarioAdmin, InstitucionAdmin, LogAuditoriaAdmin, ProfesionalAdmin, BackupLog, Especialidad (+8 more)

### Community 33 - "TestCase"
Cohesion: 0.09
Nodes (11): AuthBypassTests, ClickjackingTests, CookieSecurityTests, CSRFTests, IDORTests, TestCase, RateLimitTests, RBACTests (+3 more)

### Community 34 - "DOCUMENTO 15: RECEPCIÓN VIRTUAL OMNICANAL"
Cohesion: 0.08
Nodes (24): 10. MODELO DE DATOS PROPUESTO, 11. SEGURIDAD Y PRIVACIDAD, 12. CONFIGURACIÓN (VARIABLES DE ENTORNO PREVISTAS), 13. CASOS DE USO (EJEMPLOS), 14. CONSIDERACIONES Y RIESGOS, 15. PLAN DE IMPLEMENTACIÓN POR FASES, 16. DECISIONES PENDIENTES (A DEFINIR), 17. REFERENCIAS (+16 more)

### Community 35 - "3. HISTORIAS DE USUARIO POR ÉPICA"
Cohesion: 0.08
Nodes (24): 1. INTRODUCCIÓN, 2. ÉPICAS DEL PROYECTO, 3. HISTORIAS DE USUARIO POR ÉPICA, 4. RESUMEN DE HISTORIAS POR ÉPICA, 5. DESGLOSE POR PRIORIDAD Y SPRINT, 6. APROBACIÓN, DOCUMENTO 3: HISTORIAS DE USUARIO, RESUMEN DEL DOCUMENTO (+16 more)

### Community 36 - "Modulos implementados"
Cohesion: 0.08
Nodes (24): 10. Configuracion visual por usuario, 11. Superadmin, 12. Respaldos y restauraciones, 1. Instituciones, 2. Especialidades, 3. Profesionales y roles, 4. Pacientes, 5. Citas y agenda (+16 more)

### Community 37 - "auth_client"
Cohesion: 0.12
Nodes (7): auth_client(), RBACStrictTests, TenantIsolationTests, SmokeHttpTests, DashboardViewsTests, EpidemiologiaViewsTests, TestCase

### Community 38 - "DOCUMENTO 5: DIAGRAMAS DE FLUJO"
Cohesion: 0.08
Nodes (23): 1. VISIÓN GENERAL, 2.1 Flujo de Autenticación Multi-tenant, 2.2 Flujo de Registro de Paciente (Recepcionista), 2.3 Flujo de Agendamiento de Cita (Específico), 2.4 Flujo de Consulta Médica (7 pasos guiados), 2.5 Flujo de Referencia a Especialista (1er → 2do nivel), 2.6 Flujo del Paciente (Autoagendamiento Web), 2. USER FLOWS (FLUJOS DE USUARIO) (+15 more)

### Community 39 - "3. Pantallas propuestas"
Cohesion: 0.09
Nodes (22): 1. Objetivo, 2. Estructura general, 3. Pantallas propuestas, 4. Navegación, 5. Estados visuales, 6. Mensajes de interfaz, 7. Principios de usabilidad, 8. Accesibilidad básica (+14 more)

### Community 40 - "DOCUMENTO 0: DESCRIPCIÓN GENERAL DEL PROYECTO"
Cohesion: 0.09
Nodes (22): 10. GLOSARIO DE TÉRMINOS CLAVE (NUEVOS), 1. ¿QUÉ ES XMEDICAL?, 2. ¿QUÉ PROBLEMA RESUELVE?, 3. ¿QUIÉNES SON LOS USUARIOS?, 4. ¿CUÁLES SON LOS NIVELES DE ATENCIÓN?, 5. ¿QUÉ TECNOLOGÍAS USA?, 6. ¿CUÁLES SON LAS CLASIFICACIONES CLÍNICAS SOPORTADAS?, 7. ¿CUÁL ES EL ALCANCE POR FASES? (+14 more)

### Community 41 - "git-helper.ps1"
Cohesion: 0.28
Nodes (19): Action-Branch(), Action-Commit(), Action-Diff(), Action-Fetch(), Action-Log(), Action-Pull(), Action-Push(), Action-Stash() (+11 more)

### Community 42 - "views.py"
Cohesion: 0.19
Nodes (29): bankVitals(), bed(), bench(), board(), box(), chair(), clinicRoomConsult(), clinicRoomLabs() (+21 more)

### Community 43 - "permissions.py"
Cohesion: 0.15
Nodes (3): TestCase, WizardAutosaveTests, WizardIASuggestionTests

### Community 44 - "views.py"
Cohesion: 0.14
Nodes (16): _enriquecer_con_cie10(), ia_diagnostico_disponible(), _parse_sugerencias_json(), IA lista para sugerencias en el wizard (config + proveedor + feature)., Sugiere diagnosticos usando motivo, anamnesis y examen fisico.      Returns:, sugerir_diagnosticos(), diagnostico_ia_habilitado(), True si la institución tiene IA activa y la feature de diagnóstico sugerido. (+8 more)

### Community 45 - "DOCUMENTO 13: APP MÓVIL Y API REST"
Cohesion: 0.10
Nodes (19): 10. PLAN DE IMPLEMENTACIÓN, 11. REFERENCIAS, 1. OBJETIVO, 2. ESTADO ACTUAL vs. PLANIFICADO, 3. ARQUITECTURA OBJETIVO, 4.1 Nueva app Django: `apps/api/`, 4.2 Dependencias a añadir, 4.3 Patrón recomendado: servicios compartidos (+11 more)

### Community 46 - "test_fase1.py"
Cohesion: 0.18
Nodes (10): get_current_request(), _json_safe(), log_audit(), log_ia_usage(), Registra uso de IA sin almacenar prompts clínicos., serialize_instance(), audit_delete(), audit_save() (+2 more)

### Community 47 - "5. BACKEND Y ESQUEMA DE DATOS"
Cohesion: 0.11
Nodes (17): 10. Integraciones externas, 11. Manejo de errores, 12. Auditoría y trazabilidad, 13. Referencias, 1. Arquitectura general, 2. Módulos del backend (app `apps/recepcion_virtual/`), 3. Entidades principales, 4. Modelo de datos (relaciones) (+9 more)

### Community 48 - "XMedical - Sistema de Gestión Clínica Multi-tenant"
Cohesion: 0.11
Nodes (18): Acceso al sistema, Arquitectura, Características principales, Documentación, Estructura del proyecto, Instalación rápida, Licencia, Módulos Django (+10 more)

### Community 49 - "4. TRD — DOCUMENTO DE REQUERIMIENTOS TÉCNICOS"
Cohesion: 0.12
Nodes (16): 10. Registro de auditoría, 11. Escalabilidad, 12. Restricciones técnicas, 13. Requisitos no funcionales (resumen), 14. Referencias, 1. Tipo de aplicación, 2. Tecnologías propuestas, 3. Compatibilidad (panel web) (+8 more)

### Community 50 - "Consulta"
Cohesion: 0.09
Nodes (21): CitaAdmin, Meta, Cita, Meta, TurnoDisponible, ConsultaAdmin, DiagnosticoAdmin, DiagnosticoInline (+13 more)

### Community 51 - "Informe de verificación operativa — XMedical"
Cohesion: 0.09
Nodes (21): 10. Cómo reproducir estas pruebas, 11. Plantilla para futuras revisiones, 1. Resumen ejecutivo, 2. Infraestructura, 3. Red y SSL, 4. Rutas públicas (sin autenticación), 5. Autenticación y roles, 6. Base de datos (+13 more)

### Community 52 - "1. PRD — DOCUMENTO DE REQUERIMIENTOS DEL PRODUCTO"
Cohesion: 0.12
Nodes (15): 10. Reglas de negocio importantes, 11. Criterios de éxito (indicadores), 12. Prioridades, 13. Referencias, 1. Nombre provisional, 1. PRD — DOCUMENTO DE REQUERIMIENTOS DEL PRODUCTO, 2. Problema que resuelve, 3. Objetivo principal (+7 more)

### Community 53 - "2. FLUJO DE LA APLICACIÓN"
Cohesion: 0.12
Nodes (15): 10. Referencias, 1. Flujo de alto nivel (mensaje entrante), 2. FLUJO DE LA APLICACIÓN, 2. Flujo de "registro" (opt-in del canal), 3. Flujo de identificación ("inicio de sesión" del paciente), 4.1 Paciente — recordatorio y confirmación (CU-01), 4.2 Paciente — agendamiento (CU-05, Fase 2), 4.3 Recepcionista humano — handoff (+7 more)

### Community 54 - "APIPacientesTests"
Cohesion: 0.15
Nodes (5): APITestCase, APIAuthTests, APICitasTests, APIPacientesTests, APIRateLimitTests

### Community 55 - "3. DISEÑO UI/UX"
Cohesion: 0.13
Nodes (14): 1. Principios de diseño, 2. Mapa de pantallas / superficies, 3.1 Bandeja de conversaciones, 3.2 Detalle de conversación, 3. DISEÑO UI/UX, 3. Wireframes de baja fidelidad (panel web), 4. Diseño para computadora y móvil, 5. Componentes reutilizables (+6 more)

### Community 56 - "6. PLAN DE IMPLEMENTACIÓN"
Cohesion: 0.13
Nodes (14): 10. Capacitación y manuales, 11. Mantenimiento inicial, 12. Referencias, 1. Alcance de la primera versión (MVP), 2. Fases de desarrollo, 3. Módulos por implementar y dependencias, 4. Priorización, 5. Entregables por fase (+6 more)

### Community 57 - "Guía de Configuración - XMedical"
Cohesion: 0.12
Nodes (16): Checklist de preparación, Checklist final, Con Docker (recomendado), Configuración IA local (Ollama) — planificado, Guía de Configuración - XMedical, Inicio con Docker completo, Paso 1: Clonar y configurar entorno, Paso 2: Levantar PostgreSQL y Redis (+8 more)

### Community 58 - "ConsultaWizardTests"
Cohesion: 0.14
Nodes (3): CIE10SearchTests, ConsultaWizardTests, TestCase

### Community 59 - "epidemiologia.py"
Cohesion: 0.30
Nodes (7): _config_efectiva(), detectar_alertas_brote(), epidemiologia_dashboard_data(), get_epidemiologia_config(), resumen_diagnosticos_periodo(), tendencias_diagnosticos(), EpidemiologiaServicesTests

### Community 60 - "Prompts divididos para XMedical Fase 2"
Cohesion: 0.04
Nodes (47): 10. COMPARATIVA: CLOUD vs. LOCAL, 11. REFERENCIAS, 1. OBJETIVO, 2. ESTADO ACTUAL vs. OBJETIVO, 3.1 Flujo de configuración (UI), 3. ARQUITECTURA, 4.1 Backend — `OllamaProvider`, 4.2 Variables de entorno (+39 more)

### Community 61 - "Preclinica"
Cohesion: 0.13
Nodes (21): AIConfig, BaseAIProvider, build_provider(), get_ai_config(), _get_json(), OllamaProvider, OpenAIProvider, OpenRouterProvider (+13 more)

### Community 62 - "Guía rápida de uso (visión 0.1b)"
Cohesion: 0.17
Nodes (11): Capturar, Cómo abrir un proyecto, Cómo crear un proyecto, Cómo montar el audio (máx. 3 pistas), Cómo obtener el video, Dónde quedan los archivos, Exportar, Guía rápida de uso (visión 0.1b) (+3 more)

### Community 63 - "Informe de verificación — XMedical"
Cohesion: 0.17
Nodes (11): 10. Incidencias abiertas, 1. Resumen ejecutivo, 2. Archivos de evidencia, 3. Infraestructura (INF-*), 4. SSL (SSL-*), 5. Humo HTTP (SMK-*), 6. Tests Django (extracto), 7. Deploy check (+3 more)

### Community 64 - "Cita"
Cohesion: 0.23
Nodes (17): Get-AceSet(), Get-Ancestors(), Get-HResultChain(), Get-IntegritySid(), Get-NormalizedPath(), Get-ObjectFacts(), Get-OwnDaclSddl(), Get-RepairRefusal() (+9 more)

### Community 65 - "locustfile.py"
Cohesion: 0.22
Nodes (5): HttpUser, AnonymousUser, MedicoUser, Escenarios de carga Locust (LOAD-*)., RecepcionUser

### Community 66 - "tests.py"
Cohesion: 0.14
Nodes (11): DashboardServicesTests, HiloTests, TestCase, medico_con_horario(), test_buscar_disponibilidad_excluye_citas_ocupadas(), test_buscar_disponibilidad_respeta_jornada_manana(), test_cita_form_valida_horario(), cardiologo() (+3 more)

### Community 68 - "PreclinicaAlertasTests"
Cohesion: 0.27
Nodes (3): PreclinicaAlertasTests, PreclinicaFunctionalTests, TestCase

### Community 69 - "Visión de producto redefinida"
Cohesion: 0.20
Nodes (9): 1. Decisión, 2. Decisiones de alcance (acordadas), 3. Modelo mental del usuario, 4. Matriz de orígenes, 5. Fuera de alcance (cerrar scope), 6. Trazabilidad, 7. Criterio de éxito del MVP redefinido, 8. Prioridades post-MVP (v0.2) (+1 more)

### Community 70 - "Que probar con cada usuario"
Cohesion: 0.20
Nodes (10): Acceso, Admin, Credenciales, Datos incluidos, Enfermera, Medico, Que probar con cada usuario, Recepcionista (+2 more)

### Community 72 - "xmedical_tags.py"
Cohesion: 0.31
Nodes (3): _can_access(), _nav_item(), sidebar_nav()

### Community 74 - "decorators.py"
Cohesion: 0.28
Nodes (18): bind(), buildChapterNav(), buildOverview(), buildQR(), closeOverview(), goTo(), init(), nextSlide() (+10 more)

### Community 75 - "Checklist UAT — XMedical"
Cohesion: 0.25
Nodes (8): Admin institución (`admin.demo`), Checklist UAT — XMedical, Credenciales demo, Enfermería (`enfermera.demo`), Médico (`medico.demo`), Recepción (`recepcion.demo`), Responsive (manual), Superadmin (`superadmin.demo`)

### Community 76 - "Cursor Cloud specific instructions"
Cohesion: 0.29
Nodes (5): Configuración obligatoria (`.env`), Cursor Cloud specific instructions, Pruebas, Servicios y cómo levantarlos, Servidor de desarrollo

### Community 77 - "Informes de verificación"
Cohesion: 0.23
Nodes (10): EnfermeraRequiredMixin, alertas_activas_paciente(), Meta, PreclinicaForm, get_scoped_cita(), PreclinicaListView, PreclinicaRegistroView, ListView (+2 more)

### Community 79 - "Checklist de seguridad — XMedical"
Cohesion: 0.33
Nodes (6): Acceso y roles, Checklist de seguridad — XMedical, Configuración y secretos, Datos e infraestructura, Escaneos automatizados, Transporte y headers

### Community 81 - "test_referencias.py"
Cohesion: 0.24
Nodes (13): AccessMixin, RBAC centralizado por rol de profesional (SEC-P01)., role_required(), RoleRequiredMixin, user_has_role(), AdministracionDashboardView, EnfermeriaDashboardView, EpidemiologiaDashboardView (+5 more)

### Community 82 - "RBACStrictTests"
Cohesion: 0.20
Nodes (9): AIClient, build_cloud_fallback_provider(), Any, Proveedor cloud de respaldo cuando Ollama falla (OpenRouter > OpenAI)., Cliente unificado para llamadas IA con configuracion global o por institucion., Ejecuta complete(); si Ollama falla y fallback_cloud, usa proveedor cloud., test_ai_client_not_available_without_keys(), test_ai_client_uses_institution_model() (+1 more)

### Community 84 - "Documentación XMedical"
Cohesion: 0.40
Nodes (5): Documentación XMedical, Documentos de producto, Estado de implementación (2026-07), Guías operativas, Planificación por módulo

### Community 85 - "Solución de problemas"
Cohesion: 0.21
Nodes (4): AusentismoPredictivoTests, DashboardPredictivoIntegrationTests, DemandaPredictivaTests, TestCase

### Community 86 - "run_all_verifications.sh"
Cohesion: 0.70
Nodes (4): log(), run_step(), run_all_verifications.sh script, XMEDICAL_EVIDENCE_DIR

### Community 87 - "verify_smoke.sh"
Cohesion: 0.70
Nodes (4): check_code(), check_redirect_login(), record(), verify_smoke.sh script

### Community 98 - "IaPredictivaConfig"
Cohesion: 0.20
Nodes (7): Pruebas del wizard de consulta (FUN-Q*)., Pruebas de autosave y sugerencias IA en wizard (Fase 2)., Utilidades compartidas para tests de XMedical., PreclinicaAdmin, Preclinica, Pruebas funcionales y unitarias de preclínica (FUN-PR*)., Pruebas de variables clinicas por especialidad (Fase 2).

### Community 99 - "uv_lib.sh"
Cohesion: 0.67
Nodes (3): uv_lib.sh script, uv_ensure(), uv_sync_venv()

### Community 100 - "verify_infra.sh"
Cohesion: 0.83
Nodes (3): check_active(), record(), verify_infra.sh script

### Community 101 - "verify_security_headers.sh"
Cohesion: 0.83
Nodes (3): headers(), record(), verify_security_headers.sh script

### Community 102 - "wizard.js"
Cohesion: 0.19
Nodes (16): current(), facesHtml(), fitHilo(), loadAvatar(), openMap(), renderHilo(), renderNav(), runCounts() (+8 more)

### Community 104 - "test_flujo_enfermera.py"
Cohesion: 0.50
Nodes (3): Page, E2E-02: enfermera — preclínica., test_e2e02_flujo_enfermera()

### Community 105 - "test_flujo_medico_wizard.py"
Cohesion: 0.50
Nodes (3): Page, E2E-03: médico — wizard consulta (pasos visibles)., test_e2e03_flujo_medico_wizard()

### Community 106 - "test_flujo_recepcion.py"
Cohesion: 0.50
Nodes (3): Page, E2E-01: recepcionista — alta paciente y agendar cita., test_e2e01_flujo_recepcion()

### Community 107 - "test_login.py"
Cohesion: 0.50
Nodes (3): Page, E2E-05: logout — sesión cerrada., test_e2e05_logout()

### Community 108 - "test_superadmin_backup.py"
Cohesion: 0.50
Nodes (3): Page, E2E-04: superadmin — panel global., test_e2e04_superadmin_panel()

### Community 189 - "ocr_views.py"
Cohesion: 0.11
Nodes (21): default_ai_settings(), _default_model_for_provider(), get_institution_ai_settings(), get_ollama_vision_client(), ocr_ia_habilitado(), ocr_ollama_configured(), Any, Configuración IA por institución (Institucion.configuracion['ai']). (+13 more)

### Community 190 - "Informe de verificación — XMedical"
Cohesion: 0.13
Nodes (21): _clear_tenant_data(), collect_tenant_objects(), _collect_users(), _convert_field_value(), _deserialize_record(), export_tenant_package(), import_tenant_package(), _mute_predictive_signals() (+13 more)

### Community 191 - "Carpeta de evidencia — XMedical"
Cohesion: 0.22
Nodes (14): create_institution_backup(), export_tenant_json(), log_tenant_operation(), AuditoriaListView, DashboardView, home(), ListView, LoginRequiredMixin (+6 more)

### Community 192 - "_post_chat_completion"
Cohesion: 0.28
Nodes (5): _extract_message_content(), _extract_ollama_content(), _post_chat_completion(), _post_json(), Vision: POST /api/chat con imágenes base64 (LLaVA, moondream, etc.).

### Community 193 - "XMedical · Atlas del sistema"
Cohesion: 0.22
Nodes (8): Abrir, Archivos, Controles, Estructura del deck, Modo captura / QA, Notas, Personalizar, XMedical · Atlas del sistema

### Community 194 - "3. TIPOS DE PRUEBAS"
Cohesion: 0.22
Nodes (9): 3.1 Pruebas Unitarias, 3.2 Pruebas de Integración, 3.3 Pruebas de API, 3.4 Pruebas de UI (End-to-End), 3.5 Pruebas de Rendimiento / Carga, 3.6 Pruebas de Seguridad, 3.7 Pruebas de Aceptación (UAT), 3.8 Pruebas de Recuperación (Disaster Recovery) (+1 more)

### Community 195 - "can_manage_pacientes"
Cohesion: 0.29
Nodes (8): AdminRequiredMixin, ConfiguracionIAModelosView, ConfiguracionIAProbarView, ConfiguracionIAView, _ollama_from_request_data(), LoginRequiredMixin, View, _resolve_institucion()

### Community 196 - "riesgo_cronico.py"
Cohesion: 0.27
Nodes (7): evaluar_riesgo_diabetes(), evaluar_riesgo_hta(), evaluar_riesgos_cronicos(), _imc_reciente(), _texto_riesgo_familiar(), _ultimas_preclinicas(), RiesgoCronicoTests

### Community 197 - "Prototipo navegable · aspecto Atlas"
Cohesion: 0.40
Nodes (4): Abrir, Avatares, Prototipo navegable · aspecto Atlas, Recorrer

### Community 199 - "DashboardServicesTests"
Cohesion: 0.40
Nodes (5): Error de conexión a PostgreSQL, Error: "No module named django", Puerto 8000 ocupado, Recargar datos de prueba, Solución de problemas

### Community 200 - "RoleRoutingTests"
Cohesion: 0.12
Nodes (5): AuthTests, ClinicalRouteTests, FixtureLoadedTests, TestCase, RoleRoutingTests

### Community 201 - "EpidemiologiaViewsTests"
Cohesion: 0.67
Nodes (3): AIProviderError, Exception, Error base para integraciones IA.

## Knowledge Gaps
- **881 isolated node(s):** `Meta`, `Meta`, `Meta`, `Meta`, `Migration` (+876 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **57 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Paciente` connect `models.py` to `Profesional`, `views.py`, `IaPredictivaConfig`, `urls.py`, `views.py`, `QRService`, `views.py`, `test_fase1.py`, `Consulta`, `tenant_transfer.py`, `Informe de verificación — XMedical`, `Carpeta de evidencia — XMedical`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `Cita` connect `Consulta` to `Profesional`, `time`, `IaPredictivaConfig`, `views.py`, `urls.py`, `ausentismo.py`, `views.py`, `models.py`, `QRService`, `services.py`, `views.py`, `Informes de verificación`, `test_fase1.py`, `tenant_transfer.py`, `Informe de verificación — XMedical`, `Carpeta de evidencia — XMedical`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `current_institucion()` connect `views.py` to `time`, `views.py`, `UserPreference`, `can_manage_pacientes`, `views.py`, `models.py`, `QRService`, `Informes de verificación`, `current_institucion`, `Carpeta de evidencia — XMedical`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Cita` (e.g. with `CitaAdmin` and `CitaFlexibleForm`) actually correct?**
  _`Cita` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Institucion` (e.g. with `BackupLogAdmin` and `EspecialidadAdmin`) actually correct?**
  _`Institucion` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Paciente` (e.g. with `DocumentoOCRLogAdmin` and `PacienteAdmin`) actually correct?**
  _`Paciente` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Profesional` (e.g. with `BackupLogAdmin` and `EspecialidadAdmin`) actually correct?**
  _`Profesional` has 11 INFERRED edges - model-reasoned connections that need verification._