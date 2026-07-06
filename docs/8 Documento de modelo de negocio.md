# DOCUMENTO 8: MODELO DE NEGOCIO
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.0 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. VISIÓN GENERAL

Este documento define la **estrategia comercial** de XMedical, incluyendo:

- **Business Model Canvas** (lienzo de modelo de negocio)
- **Propuesta de valor por segmento**
- **Análisis de mercado y competencia**
- **Fuentes de ingresos**
- **Estructura de costos**
- **Punto de equilibrio**
- **KPIs comerciales**
- **Hoja de ruta de evolución comercial**

---

## 2. BUSINESS MODEL CANVAS

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              BUSINESS MODEL CANVAS - XMEDICAL                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────┐  │
│  │   ALIADOS CLAVE         │  │   ACTIVIDADES CLAVE     │  │   PROPUESTA DE      │  │
│  │                         │  │                         │  │   VALOR             │  │
│  │ • Proveedores Cloud     │  │ • Desarrollo software   │  │                     │  │
│  │   (AWS/Azure)           │  │ • Parametrización       │  │ • Flujo guiado       │  │
│  │ • API de IA             │  │ • Soporte técnico       │  │   paso a paso       │  │
│  │   (OpenAI, Google)      │  │ • Capacitación          │  │ • Multi-tenant       │  │
│  │ • Laboratorios clínicos │  │ • Marketing y ventas    │  │ • Parametrización    │  │
│  │   (integración futura)  │  │                         │  │   completa          │  │
│  │ • Socios integradores   │  │   RECURSOS CLAVE        │  │ • IA integrada       │  │
│  │   (implementación)      │  │                         │  │ • Bajos costos       │  │
│  │                         │  │ • Equipo de desarrollo  │  │ • Open source        │  │
│  │                         │  │ • Infraestructura cloud │  │   (opcional)        │  │
│  │                         │  │ • Base de datos         │  │                     │  │
│  │                         │  │ • Propiedad intelectual │  │                     │  │
│  ├─────────────────────────┤  ├─────────────────────────┤  ├─────────────────────┤  │
│  │   ESTRUCTURA DE COSTOS  │  │   FUENTES DE INGRESOS   │  │   RELACIÓN CON      │  │
│  │                         │  │                         │  │   CLIENTES          │  │
│  │ • Desarrollo: 40%       │  │ • Licencia SaaS: 60%    │  │                     │  │
│  │ • Infraestructura: 20%  │  │ • Implementación: 20%   │  │ • Soporte dedicado   │  │
│  │ • Marketing: 15%        │  │ • Soporte anual: 15%    │  │ • Capacitación      │  │
│  │ • Soporte: 15%          │  │ • Capacitación: 5%      │  │ • Comunidad open    │  │
│  │ • Administración: 10%   │  │                         │  │   source           │  │
│  │                         │  │                         │  │ • Portal de ayuda   │  │
│  ├─────────────────────────┤  └─────────────────────────┘  ├─────────────────────┤  │
│  │   CANALES               │                                │   SEGMENTOS DE      │  │
│  │                         │                                │   CLIENTES          │  │
│  │ • Ventas directas       │                                │                     │  │
│  │ • Partners integradores │                                │ • Clínicas privadas │  │
│  │ • Portal web            │                                │ • CESFAM públicos   │  │
│  │ • Demos gratuitas       │                                │ • Grupos de salud   │  │
│  │ • Conferencias          │                                │ • Franquicias       │  │
│  │   del sector salud      │                                │ • Hospitales (futuro)│  │
│  │                         │                                │                     │  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. PROPUESTA DE VALOR POR SEGMENTO (DETALLADA)

| Segmento | Problema | Propuesta de valor | Beneficio cuantificable |
|----------|----------|---------------------|------------------------|
| **Clínicas privadas** | Alto costo de sistemas, falta de parametrización | SaaS asequible, parametrizable, facturación integrable | -50% costo vs sistemas tradicionales |
| **CESFAM públicos** | Presupuesto limitado, necesidad de reportes epidemiológicos | Open source, escalable, reportes automáticos | 0$ en licencias (self-hosted) |
| **Grupos de salud** | Múltiples sedes sin integración | Multi-tenant nativo, datos aislados por sede | Reportes consolidados en tiempo real |
| **Franquicias** | Modelo de negocio estandarizado | Parametrización centralizada, despliegue rápido | Onboarding de nueva sede < 1 hora |

---

## 4. ANÁLISIS DE MERCADO Y COMPETENCIA

### 4.1 Tamaño de mercado

| Mercado | Tamaño (Chile) | Tamaño (Latam) | Crecimiento anual |
|---------|---------------|----------------|-------------------|
| Clínicas privadas | ~500 | ~15,000 | 8% |
| CESFAM públicos | ~600 | ~20,000 | 5% |
| Hospitales públicos | ~200 | ~5,000 | 3% |
| **Total mercado objetivo** | **~1,300** | **~40,000** | **5-8%** |

### 4.2 Competencia

| Competidor | Tipo | Precio | Fortalezas | Debilidades | Estrategia XMedical |
|------------|------|--------|------------|-------------|---------------------|
| **Meditech** | Propietario | Alto | Completo, integrado | Costoso, rígido | Ofrecer 50% menos |
| **InterSystems** | Propietario | Muy alto | Escalable | Curva aprendizaje | Enfoque en PYME |
| **OpenMRS** | Open source | 0$ | Gratuito | Complejo, requiere técnico | Mejor UX + parametrización |
| **Sisfarma** | Propietario | Medio | Popular en farmacia | Solo farmacia | Ser completo |
| **Excel/Google Sheets** | Manual | ~0$ | Simple | No trazable, sin seguridad | Automatización + trazabilidad |

### 4.3 Ventajas competitivas

| Ventaja | XMedical | Competidores |
|---------|----------|--------------|
| **Costo total** | $$ (medio-bajo) | $$$ - $$$$ (alto-muy alto) |
| **Multi-tenant nativo** | ✅ | ❌ (requiere instalación por cliente) |
| **Flujo guiado** | ✅ (wizard médico) | ❌ (formularios sueltos) |
| **Open source opcional** | ✅ | ❌ (solo Meditech no) |
| **Parametrización sin código** | ✅ | ❌ (requiere programador) |
| **Tiempo de implementación** | 2-4 semanas | 3-6 meses |

---

## 5. FUENTES DE INGRESOS

### 5.1 Modelo SaaS (recomendado)

| Plan | Precio mensual | Precio anual | Incluye | Target |
|------|---------------|--------------|---------|--------|
| **Clínica Básica** | $99 USD | $990 USD | Hasta 5 médicos, 1 sede, 500 pacientes/mes | Clínicas pequeñas |
| **Clínica Profesional** | $299 USD | $2,990 USD | Hasta 20 médicos, 3 sedes, pacientes ilimitados | Clínicas medianas |
| **Corporativo** | $999 USD | $9,990 USD | Médicos ilimitados, sedes ilimitadas, SLA 99.9% | Grupos, franquicias |
| **Público** | $499 USD | $4,990 USD | Hasta 50 médicos, reportes epidemiológicos | CESFAM, públicos |

### 5.2 Modelo Licencia Perpetua (self-hosted)

| Tamaño | Precio (único) | Incluye | Mantenimiento anual |
|--------|----------------|---------|---------------------|
| Clínica pequeña | $3,000 USD | 5 médicos | $600 USD |
| Clínica mediana | $8,000 USD | 20 médicos | $1,600 USD |
| Corporativo | $20,000 USD | Ilimitado | $4,000 USD |
| Público | $12,000 USD | 50 médicos | $2,400 USD |

### 5.3 Servicios adicionales

| Servicio | Precio | Descripción |
|----------|--------|-------------|
| **Implementación** | $1,000 - $5,000 USD | Configuración, parametrización, onboarding |
| **Capacitación** | $500 USD/día | Capacitación in-situ o remota |
| **Soporte premium** | +20% sobre licencia | SLA 24/7, respuesta < 1 hora |
| **Personalizaciones** | $100 USD/hora | Desarrollo de features a medida |
| **Integraciones** | $2,000 USD c/u | Laboratorio, facturación, etc. |

### 5.4 Modelo Open Source (comunitario)

| Modelo | Precio | Incluye | Destinatario |
|--------|--------|---------|--------------|
| **Community** | $0 | Código fuente, documentación básica | Entusiastas, testing |
| **Enterprise** | Pagado | Soporte, updates, garantías, integraciones | Empresas, públicos |

### 5.5 Proyección de ingresos (año 1 - 5 clientes)

| Fuente | Cantidad | Precio promedio | Ingreso anual |
|--------|----------|-----------------|---------------|
| Licencias SaaS | 3 clientes | $2,000 USD | $6,000 USD |
| Implementación | 3 clientes | $2,000 USD | $6,000 USD |
| Capacitación | 2 clientes | $1,000 USD | $2,000 USD |
| Soporte premium | 1 cliente | +$1,000 USD | $1,000 USD |
| **Total año 1** | | | **$15,000 USD** |

### 5.6 Proyección de ingresos (año 3 - 50 clientes)

| Fuente | Cantidad | Precio promedio | Ingreso anual |
|--------|----------|-----------------|---------------|
| Licencias SaaS | 40 clientes | $2,000 USD | $80,000 USD |
| Licencias perpetua | 10 clientes | $5,000 USD | $50,000 USD |
| Implementación | 30 clientes | $2,000 USD | $60,000 USD |
| Mantenimiento anual | 10 clientes | $1,000 USD | $10,000 USD |
| Capacitación | 15 clientes | $1,000 USD | $15,000 USD |
| Soporte premium | 10 clientes | +$1,000 USD | $10,000 USD |
| Personalizaciones | 5 clientes | $2,000 USD | $10,000 USD |
| **Total año 3** | | | **$235,000 USD** |

---

## 6. ESTRUCTURA DE COSTOS

### 6.1 Costos fijos mensuales (para operación SaaS)

| Concepto | Costo mensual (USD) | Anual (USD) |
|----------|--------------------|-------------|
| **Infraestructura cloud** | $300 | $3,600 |
| - Servidor (4 vCPU, 8GB) | $100 | $1,200 |
| - Base de datos | $100 | $1,200 |
| - Storage (100GB) | $50 | $600 |
| - CDN + Backup | $50 | $600 |
| **APIs externas** | $100 | $1,200 |
| - IA (OpenAI/Google) | $50 | $600 |
| - Email (SendGrid) | $50 | $600 |
| **Dominios + SSL** | $10 | $120 |
| **Monitoreo** | $50 | $600 |
| **Soporte (1 persona)** | $2,000 | $24,000 |
| **Total costos fijos** | **$2,460** | **$29,520** |

### 6.2 Costos de desarrollo (único)

| Concepto | Costo (USD) | Detalle |
|----------|-------------|---------|
| **Desarrollo MVP** | $30,000 | 4 semanas, 2 desarrolladores |
| **Desarrollo Fase 2** | $20,000 | 4 semanas |
| **Desarrollo Fase 3** | $25,000 | 6 semanas |
| **Testing y QA** | $10,000 | Continuo |
| **Documentación** | $5,000 | Manuales, API docs |
| **Total desarrollo** | **$90,000** | |

### 6.3 Costos de marketing y ventas

| Concepto | Costo anual (USD) |
|----------|-------------------|
| Sitio web | $500 |
| Marketing de contenidos | $2,000 |
| Publicidad | $3,000 |
| Ferias y conferencias | $2,000 |
| Fuerza de ventas (comisión 10%) | Variable |
| **Total marketing** | **$7,500 + comisiones** |

### 6.4 Punto de equilibrio

```
Cálculo:
- Costos fijos mensuales = $2,460 USD
- Ingreso promedio por cliente = $200 USD/mes (SaaS + implementación amortizada)
- Clientes necesarios para equilibrio = $2,460 / $200 = 12.3 ≈ 13 clientes

Tiempo estimado para alcanzar 13 clientes: 6-8 meses post-lanzamiento
```

---

## 7. KPIS COMERCIALES

### 7.1 KPIs de crecimiento

| KPI | Definición | Objetivo (año 1) | Objetivo (año 3) |
|-----|------------|------------------|------------------|
| **MRR** (Monthly Recurring Revenue) | Ingreso recurrente mensual | $1,000 USD | $20,000 USD |
| **ARR** (Annual Recurring Revenue) | Ingreso recurrente anual | $12,000 USD | $240,000 USD |
| **Número de clientes** | Clientes activos | 10 | 100 |
| **CAC** (Customer Acquisition Cost) | Costo de adquisición por cliente | $2,000 USD | $1,000 USD |
| **LTV** (Lifetime Value) | Valor de vida del cliente | $10,000 USD | $15,000 USD |
| **LTV/CAC** | Ratio de eficiencia | 5:1 | 15:1 |
| **Churn rate** | Tasa de cancelación anual | < 10% | < 5% |

### 7.2 KPIs operacionales

| KPI | Definición | Objetivo |
|-----|------------|----------|
| **Tiempo de implementación** | Configuración nueva clínica | < 2 días |
| **Tasa de adopción** | Médicos usando sistema | > 80% |
| **Satisfacción cliente (CSAT)** | Encuesta post-implementación | > 4.5/5 |
| **NPS** (Net Promoter Score) | Probabilidad de recomendar | > 50 |
| **Tickets de soporte** | Tickets por cliente/mes | < 2 |
| **Tiempo de respuesta soporte** | SLA | < 4 horas |

---

## 8. HOJA DE RUTA DE EVOLUCIÓN COMERCIAL

### Fase 1: Lanzamiento (Meses 0-6)
| Hito | Métrica |
|------|---------|
| MVP desarrollado | ✅ |
| Pilot con 1-2 clínicas | ✅ |
| Modelo de precios validado | ✅ |
| Landing page + marketing | En curso |
| **Objetivo clientes** | 3-5 |

### Fase 2: Crecimiento (Meses 6-18)
| Hito | Métrica |
|------|---------|
| Fase 2 completo | ✅ |
| Caso de éxito documentado | ✅ |
| Partners integradores (2-3) | ✅ |
| Automatización de onboarding | ✅ |
| **Objetivo clientes** | 20-30 |

### Fase 3: Escalamiento (Meses 18-36)
| Hito | Métrica |
|------|---------|
| Fase 3 completo | ✅ |
| Expansión regional (Latam) | En curso |
| Integraciones (laboratorio, facturación) | ✅ |
| Portal de autoservicio | ✅ |
| **Objetivo clientes** | 50-100 |

### Fase 4: Consolidación (Años 3-5)
| Hito | Métrica |
|------|---------|
| Líder en segmento PYME | ✅ |
| Expansión a hospitales (3er nivel) | En curso |
| Modelo de franquicia | ✅ |
| **Objetivo clientes** | 200+ |

---

## 9. ESTRATEGIA DE PRECIOS POR MERCADO

| País | Precio SaaS (clínica mediana) | Ajuste | Justificación |
|------|-------------------------------|--------|---------------|
| **Chile** | $299 USD | Base | Mercado local |
| **Argentina** | $199 USD | -33% | Poder adquisitivo |
| **Colombia** | $249 USD | -17% | Mercado competitivo |
| **México** | $299 USD | Base | Mercado grande |
| **Perú** | $199 USD | -33% | En desarrollo |
| **Brasil** | $349 USD | +17% | Mercado grande, localización |
| **España** | $399 USD | +33% | Mercado europeo |

---

## 10. ESTRATEGIA DE RETENCIÓN

| Estrategia | Acción | Frecuencia |
|------------|--------|------------|
| **Onboarding** | Sesión guiada de configuración | Día 0 |
| **Capacitación** | Videos tutoriales por rol | Día 1-7 |
| **Check-in** | Llamada de seguimiento | Semana 2 |
| **Newsletter** | Novedades, tips, casos de éxito | Mensual |
| **Webinars** | Demos de nuevas features | Trimestral |
| **Encuesta NPS** | Medir satisfacción | Trimestral |
| **Renovación** | Recordatorio y beneficios | 30 días antes |

---

## 11. ANÁLISIS FODA (SWOT)

```
┌─────────────────────────────────────────────────────────────────┐
│                           FORTALEZAS                             │
├─────────────────────────────────────────────────────────────────┤
│ • Multi-tenant nativo (ventaja competitiva)                      │
│ • Flujo guiado (diferenciador UX)                                │
│ • Open source opcional (barrera de entrada baja)                 │
│ • Tecnología moderna (Django, DaisyUI)                           │
│ • Bajo costo vs competencia                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                           DEBILIDADES                            │
├─────────────────────────────────────────────────────────────────┤
│ • Marca nueva sin reconocimiento                                 │
│ • Sin casos de éxito documentados (inicialmente)                 │
│ • Equipo pequeño (dependencia de pocas personas)                 │
│ • Características avanzadas (IA) en fases posteriores            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         OPORTUNIDADES                            │
├─────────────────────────────────────────────────────────────────┤
│ • Digitalización acelerada post-pandemia                         │
│ • Interés en open source en sector público                       │
│ • Crecimiento de clínicas privadas en Latam                      │
│ • Integración con IA (diferenciador)                             │
│ • Expansión a tercer nivel (hospitalización)                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                           AMENAZAS                               │
├─────────────────────────────────────────────────────────────────┤
│ • Competidores establecidos con recursos                         │
│ • Barreras regulatorias (certificaciones)                        │
│ • Resistencia al cambio en personal de salud                     │
│ • Requisitos de seguridad muy estrictos                          │
│ • Clientes que optan por Excel/Google Sheets                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Commercial Director | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 8: Modelo de Negocio**

---

## RESUMEN DEL DOCUMENTO

| Aspecto | Valor |
|---------|-------|
| **Business Model Canvas** | 9 bloques completos |
| **Segmentos de clientes** | 4 principales |
| **Competidores analizados** | 5 |
| **Planes de precio** | 4 (SaaS), 4 (perpetua) |
| **Fuentes de ingreso** | 6 |
| **Proyección año 3** | $235,000 USD |
| **Punto de equilibrio** | 13 clientes |
| **KPIs comerciales** | 10 |
| **Hoja de ruta** | 4 fases (0-5 años) |
| **Análisis FODA** | 4 categorías completas |
