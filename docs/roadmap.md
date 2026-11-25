# Roadmap · Megatravel Web

Estado: **borrador** (2026-11-25). Product y Arquitecto lo confirman al cerrar la spec 000 y el ADR-001.

## Specs
| NNN | Spec | Prioridad | Depende de | Sensible (seguridad) | Estado |
|---|---|---|---|---|---|
| 000 | Descubrimiento: brief validado, requisitos EARS, inventario de contenido y URLs actuales | Must | — | — | Pendiente |
| 001 | Fundaciones: ADR de stack y CMS, scaffold, CI con sensores, `stop_check_command`, preview, rama `develop` | Must | 000 | Sí (auth del CMS) | Pendiente |
| 002 | Sistema de diseño: tokens, componentes base, guía visual de la web y del CMS | Must | 001 | — | Pendiente |
| 003 | Modelo de contenido y CMS base: programas, salidas, zonas, banners, home; roles y vista previa | Must | 001 | Sí | Pendiente |
| 004 | Editor de programas a medida (subida de fotos, itinerario, hoteles, tarifas, suplementos, tours) | Must | 002, 003 | Sí (subida de archivos, fotos de pasajeros) | Pendiente |
| 005 | Home de contenido (hero video/imagen, beneficios, buscador por zonas, carruseles, bloques editoriales, banners con contador) | Must | 002, 003 | — | Pendiente |
| 006 | Plantilla de listado (Bloqueos, Circuitos, zonas; filtros, chips de promoción, banners) | Must | 002, 003 | — | Pendiente |
| 007 | Detalle de programa (barra fija, salidas por mes con disponibilidad, incluye/no incluye, itinerario, hoteles, tarifas, suplementos, tours, fotos, condiciones, enlace a Meganet) | Must | 004 | — | Pendiente |
| 008 | Migración de datos desde la web actual (sobre exportaciones; sin tocar producción) | Must | 003 | — | Pendiente |
| 009 | Rendimiento, SEO (redirecciones de URLs actuales), accesibilidad y analítica | Should | 005–007 | — | Pendiente |
| 010 | Lanzamiento: cambio de dominio, plan de rollback, runbook | Must | 008, 009 | Sí | Pendiente |

Orden sugerido: una spec en implementación a la vez al principio (000 → 001 → 002/003); cuando el equipo tenga métricas de CP5, se puede llevar en paralelo una spec de backend y otra de frontend.

## Primera tanda de issues (las crea el Board en Paperclip)

### CP0 · Arranque del proyecto — Auditor
Ejecuta el checkpoint CP0 con la skill `checkpoint-auditoria` sobre `~/dev/megatravel-web`. Comprueba perfil M en `docs/00-proyecto.md`, configuración de los 12 agentes contra `/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md` §3, permisos, `core.hooksPath`, Graphify y tamaño de AGENTS.md. Informe en `docs/auditoria/CP0.md`.

### Spec 000 · Brief y requisitos — Product Analyst (revisión: Arquitecto)
Objetivo: validar y completar `docs/producto/brief.md` y escribir `docs/producto/requisitos.md` en EARS. Resuelve con el Board los `[NEEDS CLARIFICATION]` del brief (pregúntalos en este issue). Inventaria el contenido y las URLs de la web actual leyendo, solo lectura, `/mnt/c/Users/KelingMireyaMachacua/CLAUDE PROYECTOS/megatravel/bloqueosweb/docs/datos-y-api.md` y `docs/arquitectura.md`. Lectura mínima: brief, constitución, plantilla de requisitos. Cierra con handoff.

### Investigación de stack y CMS — Researcher (revisión: Arquitecto)
Objetivo: comparar opciones para la web y el CMS a medida con criterios explícitos (rendimiento, edición a medida y vista previa, roles, subida de imágenes y video, coste de hosting, madurez, soporte de IA, facilidad de migrar desde Payload 3 + PostgreSQL). Incluir al menos: Next.js + Payload 3 (stack actual), Next.js + CMS propio sobre PostgreSQL, y 1–2 alternativas actuales. Fuentes con URL y fecha. Entrega en `docs/investigacion/stack-y-cms.md` con recomendación de 3–5 líneas al inicio.

### ADR-001 · Stack y CMS — Arquitecto (revisión: Code Reviewer) · bloqueado por Spec 000 e Investigación
Objetivo: decidir stack, CMS, base de datos y hosting en `docs/arquitectura/adr/ADR-001-stack-y-cms.md`; completar `docs/arquitectura/arquitectura.md` (capas y dependencias permitidas) y `mapa-de-codigo.md`; proponer la spec 001.

## Ruta corta
Cambios de una frase y 1–2 archivos, sin spec (siguen pasando por Code Reviewer).

| Fecha | Issue | Cambio | SHA |
|---|---|---|---|
