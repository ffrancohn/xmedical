# Informe de verificación — XMedical

**Fecha:** 2026-07-06  
**Carpeta de evidencia:** `evidencia/2026-07-06_022323`  
**Generado por:** `scripts/run_all_verifications.sh`

## 1. Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| PASS | 24 |
| FAIL | 0 |
| Tests Django | PASS |
| Django check | PASS |

## 2. Archivos de evidencia

| Archivo | Contenido |
|---------|-----------|
| [01-infraestructura.txt](01-infraestructura.txt) | INF-01..08 |
| [02-ssl.txt](02-ssl.txt) | SSL-01..08 |
| [03-humo-http.txt](03-humo-http.txt) | SMK-01..06 |
| [04-django-check.txt](04-django-check.txt) | `manage.py check` |
| [05-django-deploy-check.txt](05-django-deploy-check.txt) | `check --deploy` |
| [06-django-tests.txt](06-django-tests.txt) | Suite Django completa |
| [07-cobertura-report.txt](07-cobertura-report.txt) | Cobertura |
| [07-cobertura-html/index.html](07-cobertura-html/index.html) | Cobertura visual |

## 3. Infraestructura (INF-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
| INF-01 | Gunicorn activo | PASS |
| INF-02 | Apache activo | PASS |
| INF-03 | PostgreSQL Docker | PASS |
| INF-04 | Redis Docker | PASS |
| INF-05 | Gunicorn puerto 8000 | PASS |
| INF-06 | Apache puerto 443 | PASS |
| INF-07 | Logs sin traceback | PASS |
| INF-08 | Backups escribible | PASS |

## 4. SSL (SSL-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
| SSL-01 | DNS A | PASS |
| SSL-02 | HTTPS responde | PASS |
| SSL-03 | HTTP a HTTPS | PASS |
| SSL-04 | Certificado valido | PASS |
| SSL-05 | Certbot dominio | PASS |
| SSL-06 | Renovacion dry-run | PASS |
| SSL-07 | Header HSTS | PASS |
| SSL-08 | www alias | PASS |

## 5. Humo HTTP (SMK-*)

| ID | Prueba | Resultado |
|----|--------|-----------|
| SMK-01 | Home | PASS |
| SMK-02 | Login | PASS |
| SMK-03 | Admin | PASS |
| SMK-04 | Dashboard protegido | PASS |
| SMK-05 | Pacientes protegido | PASS |
| SMK-06 | Static admin CSS | PASS |

## 6. Tests Django (extracto)

```
test_fun_a02_login_invalido (apps.auth_app.tests.AuthFunctionalTests.test_fun_a02_login_invalido) ... ok
test_fun_a03_logout (apps.auth_app.tests.AuthFunctionalTests.test_fun_a03_logout) ... ok
test_fun_a04_registro_profesional (apps.auth_app.tests.AuthFunctionalTests.test_fun_a04_registro_profesional) ... ok
test_fun_a05_preferencias_visuales (apps.auth_app.tests.AuthFunctionalTests.test_fun_a05_preferencias_visuales) ... ok
test_fun_p01_listar_pacientes (apps.pacientes.tests.PacienteFunctionalTests.test_fun_p01_listar_pacientes) ... ok
test_fun_p02_crear_paciente (apps.pacientes.tests.PacienteFunctionalTests.test_fun_p02_crear_paciente) ... ok
test_fun_p03_documento_duplicado (apps.pacientes.tests.PacienteFunctionalTests.test_fun_p03_documento_duplicado) ... ok
test_fun_p04_detalle_paciente (apps.pacientes.tests.PacienteFunctionalTests.test_fun_p04_detalle_paciente) ... ok
test_fun_p05_editar_paciente (apps.pacientes.tests.PacienteFunctionalTests.test_fun_p05_editar_paciente) ... ok
test_fun_p06_historia_redirect (apps.pacientes.tests.PacienteFunctionalTests.test_fun_p06_historia_redirect) ... ok
test_paciente_str (apps.pacientes.tests.PacienteFunctionalTests.test_paciente_str) ... ok
test_fun_c01_listar_citas (apps.citas.tests.CitaFunctionalTests.test_fun_c01_listar_citas) ... ok
test_fun_c02_agendar_cita (apps.citas.tests.CitaFunctionalTests.test_fun_c02_agendar_cita) ... ok
test_fun_c03_slot_duplicado (apps.citas.tests.CitaFunctionalTests.test_fun_c03_slot_duplicado) ... ok
test_fun_c04_cancelar_cita (apps.citas.tests.CitaFunctionalTests.test_fun_c04_cancelar_cita) ... ok
test_fun_c05_calendario_contexto (apps.citas.tests.CitaFunctionalTests.test_fun_c05_calendario_contexto) ... ok
test_fun_pr03_alerta_pa_alta (apps.preclinica.tests.PreclinicaAlertasTests.test_fun_pr03_alerta_pa_alta) ... ok
test_fun_pr04_alerta_fiebre (apps.preclinica.tests.PreclinicaAlertasTests.test_fun_pr04_alerta_fiebre) ... ok
test_fun_pr05_alerta_spo2_baja (apps.preclinica.tests.PreclinicaAlertasTests.test_fun_pr05_alerta_spo2_baja) ... ok
test_fun_pr01_lista_cola (apps.preclinica.tests.PreclinicaFunctionalTests.test_fun_pr01_lista_cola) ... ok
test_fun_pr02_registrar_signos (apps.preclinica.tests.PreclinicaFunctionalTests.test_fun_pr02_registrar_signos) ... ok
test_cie10_mvp_filtra_por_codigo (apps.consulta.tests.CIE10SearchTests.test_cie10_mvp_filtra_por_codigo) ... ok
test_fun_q01_paso1_revisar_preclinica (apps.consulta.tests.ConsultaWizardTests.test_fun_q01_paso1_revisar_preclinica) ... ok
test_fun_q02_paso2_motivo (apps.consulta.tests.ConsultaWizardTests.test_fun_q02_paso2_motivo) ... ok
test_fun_q03_paso3_anamnesis (apps.consulta.tests.ConsultaWizardTests.test_fun_q03_paso3_anamnesis) ... ok
test_fun_q04_paso4_examen_fisico (apps.consulta.tests.ConsultaWizardTests.test_fun_q04_paso4_examen_fisico) ... ok
test_fun_q05_paso5_diagnostico (apps.consulta.tests.ConsultaWizardTests.test_fun_q05_paso5_diagnostico) ... ok
test_fun_q06_paso6_plan (apps.consulta.tests.ConsultaWizardTests.test_fun_q06_paso6_plan) ... ok
test_fun_q07_paso7_finalizar (apps.consulta.tests.ConsultaWizardTests.test_fun_q07_paso7_finalizar) ... ok
test_fun_q08_busqueda_cie10 (apps.consulta.tests.ConsultaWizardTests.test_fun_q08_busqueda_cie10) ... ok
test_fun_q09_historia_clinica (apps.consulta.tests.ConsultaWizardTests.test_fun_q09_historia_clinica) ... ok
test_api_01_login_placeholder (apps.api.tests.test_future.APIFutureTests.test_api_01_login_placeholder) ... skipped 'API REST no implementada aún'
test_openapi_schema_available (apps.api.tests.test_openapi.OpenAPIRegressionTests.test_openapi_schema_available) ... skipped 'API REST no implementada aún'

----------------------------------------------------------------------
Ran 60 tests in 16.931s

OK (skipped=2)
Destroying test database for alias 'default' ('test_xmedical')...
Installed 21 object(s) from 1 fixture(s)
```

Ver salida completa: [06-django-tests.txt](06-django-tests.txt)

## 7. Deploy check

```
System check identified some issues:

WARNINGS:
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W021) You have not set the SECURE_HSTS_PRELOAD setting to True. Without this, your site cannot be submitted to the browser preload list.

System check identified 2 issues (0 silenced).
```

## 8. Cobertura

```
Name                                                   Stmts   Miss  Cover
--------------------------------------------------------------------------
apps/__init__.py                                           0      0   100%
apps/api/__init__.py                                       0      0   100%
apps/api/tests/__init__.py                                 0      0   100%
apps/api/tests/test_future.py                              5      1    80%
apps/api/tests/test_openapi.py                             5      1    80%
apps/auth_app/__init__.py                                  0      0   100%
apps/auth_app/admin.py                                     6      0   100%
apps/auth_app/apps.py                                      4      0   100%
apps/auth_app/forms.py                                    24      0   100%
apps/auth_app/migrations/0001_initial.py                   7      0   100%
apps/auth_app/migrations/__init__.py                       0      0   100%
apps/auth_app/models.py                                    9      1    89%
apps/auth_app/tests.py                                    40      0   100%
apps/auth_app/urls.py                                      3      0   100%
apps/auth_app/views.py                                    38      4    89%
apps/citas/__init__.py                                     0      0   100%
apps/citas/admin.py                                        7      0   100%
apps/citas/apps.py                                         4      0   100%
apps/citas/forms.py                                       16      0   100%
apps/citas/migrations/0001_initial.py                      6      0   100%
apps/citas/migrations/__init__.py                          0      0   100%
apps/citas/models.py                                      19      1    95%
apps/citas/tests.py                                       41      0   100%
apps/citas/urls.py                                         3      0   100%
apps/citas/views.py                                      102     12    88%
apps/consulta/__init__.py                                  0      0   100%
apps/consulta/admin.py                                    14      0   100%
apps/consulta/apps.py                                      4      0   100%
apps/consulta/forms.py                                    22      0   100%
apps/consulta/migrations/0001_initial.py                   6      0   100%
apps/consulta/migrations/__init__.py                       0      0   100%
apps/consulta/models.py                                   26      2    92%
apps/consulta/tests.py                                    72      0   100%
apps/consulta/urls.py                                      3      0   100%
apps/consulta/views.py                                    67     10    85%
apps/consulta/wizard.py                                    2      0   100%
apps/core/__init__.py                                      0      0   100%
apps/core/admin.py                                        23      0   100%
apps/core/apps.py                                          4      0   100%
apps/core/backup_utils.py                                 49      0   100%
apps/core/context_processors.py                           15      1    93%
apps/core/middleware.py                                   17      0   100%
apps/core/migrations/0001_initial.py                       7      0   100%
apps/core/migrations/0002_backuplog.py                     6      0   100%
apps/core/migrations/__init__.py                           0      0   100%
apps/core/models.py                                       63      2    97%
apps/core/test_utils.py                                    8      0   100%
apps/core/tests.py                                       123      0   100%
apps/core/tests_backup.py                                 50      0   100%
apps/core/urls.py                                          3      0   100%
apps/core/views.py                                       105     20    81%
apps/pacientes/__init__.py                                 0      0   100%
apps/pacientes/admin.py                                    7      0   100%
apps/pacientes/apps.py                                     4      0   100%
apps/pacientes/forms.py                                    8      0   100%
apps/pacientes/migrations/0001_initial.py                  6      0   100%
apps/pacientes/migrations/0002_contacto_extendido.py       4      0   100%
apps/pacientes/migrations/__init__.py                      0      0   100%
apps/pacientes/models.py                                  25      0   100%
apps/pacientes/tests.py                                   43      0   100%
apps/pacientes/urls.py                                     3      0   100%
apps/pacientes/views.py                                   59      1    98%
apps/preclinica/__init__.py                                0      0   100%
apps/preclinica/admin.py                                   6      0   100%
apps/preclinica/apps.py                                    4      0   100%
apps/preclinica/forms.py                                  16      1    94%
apps/preclinica/migrations/0001_initial.py                 6      0   100%
apps/preclinica/migrations/__init__.py                     0      0   100%
apps/preclinica/models.py                                 31      2    94%
apps/preclinica/tests.py                                  41      0   100%
apps/preclinica/urls.py                                    3      0   100%
apps/preclinica/views.py                                  52      4    92%
--------------------------------------------------------------------------
TOTAL                                                   1346     63    95%
Wrote HTML report to /var/www/xmedical/docs/informes/evidencia/2026-07-06_022323/07-cobertura-html/index.html
```

## 9. Comandos para reproducir

```bash
cd /var/www/xmedical
./scripts/run_all_verifications.sh
```

## 10. Incidencias abiertas

- Revisar filas FAIL en tablas anteriores y archivos `*-exit-code.txt` si existen.
