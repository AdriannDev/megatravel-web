# Roadmap

Estado: aprobado por el Board (MEG-25)

**Antes de la 001:** `auditoria` de arranque (Auditor) → `stack` MEG-27 (Arquitecto: ADR del stack y del hosting según RNF-01 y RNF-02; el Board decide las piezas con una tarjeta de 4 capas) → 001.

## Specs
| NNN | Spec | Prioridad | Depende de | Sensible (seguridad) | Estado |
|---|---|---|---|---|---|
| 001 | **Fundaciones:** repo, app esqueleto, CI y sensores (lint, tipos, duplicación, knip, tests). Lo demás pasa a 001b, 005, 003 y Board (spec 001 §4) | Must | ADR de stack | Sí | hecha |
| 001b | **Datos y acceso al CMS:** base de datos (Postgres en Railway, Drizzle y migraciones), autenticación del CMS y comprobación de roles en el servidor (RF-24, RF-28, RNF-05), entornos, deploy en Railway y preview de `develop`, backups de la BD con restauración probada (RNF-16 BD). Aceptada por el Board en MEG-31 | Must | 001 | Sí | en curso |
| 002 | **Modelo de contenido y API:** programas, salidas, tarifas, suplementos, bloques libres, taxonomías, cupos con historial, estados y publicación programada, caducidad a 30 días, retirada automática y manual, precio «desde», permisos por rol y concurrencia (RF-11, RF-18 a RF-23, RF-25 a RF-27, RF-30, RF-33, RF-35, RF-46, RF-47, RF-51, RNF-04, RNF-14) | Must (RF-51 Could) | 001b | Sí (permisos) | pendiente |
| 003 | **Web: listado, buscador y filtros** (RF-01 a RF-04) | Must | 002 | No | pendiente |
| 004 | **Web: detalle del programa** con bloques, tarifas, cupos, Cotizar/WhatsApp, contacto y compartir; inventario contra Figma (RF-06 a RF-10, RF-12 a RF-16) | Must | 002 | No | pendiente |
| 005 | **Medios y promoción:** subida y enlace de fotos y videos, optimización, galería, banners y videos en portada; almacenamiento en R2 y backups de medios (RF-05, RF-36, RF-38, RF-39, RNF-16 medios) | Must | 002 | No | pendiente |
| 006 | **Documentos:** adjuntos descargables, condiciones y documento generado sin marca (RF-17, RF-41, RF-42) | Must | 002 | No | pendiente |
| 007 | **SEO y analítica:** URLs amigables, meta, sitemap, Open Graph, analítica y aviso de cookies si aplica (RNF-15) | Must | 003, 004 | No | pendiente |
| — | **Hito: llega el prototipo del CMS.** Las specs 008 a 010 no empiezan antes (RNF-18). | — | Board | — | pendiente |
| 008 | **CMS (UI): usuarios y roles** (RF-29) | Must | 002, hito | Sí | pendiente |
| 009 | **CMS (UI): gestión de programas:** formularios de carga, vista previa, duplicar y punto de control de automatizaciones (RF-31, RF-32, RF-34, RF-48) | Must | 002, hito | No | pendiente |
| 010 | **CMS (UI): gestión de marketing y medios:** banners, videos, flyers, galería y collage (RF-37, RF-40) | Must | 005, hito | No | pendiente |
| 011 | **Importación y carga inicial:** importación en lote, spike de prellenado desde Word y carga de los ~70 programas (RF-43 a RF-45); el formato de importación se fija aquí con los datos mínimos | Must (RF-44 Could) | 009 | No | pendiente |
| — | **Lanzamiento v1:** dictamen pre-merge, merge a `main` por el Board | — | 001–011 | — | pendiente |
| 012 | **v1.1: sincronización de cupos desde Google Drive** (RF-49) | v1.1 | 002, 009 | Sí (credenciales de Google) | pendiente |
| — | **Futuro: chatbot** de consultas (RF-50), sin número ni fecha | Won't (v1) | 002 | — | — |

**Paralelismo posible:** 003, 004, 005 y 006 dependen solo de la 002 y pueden ir en olas paralelas. Las specs 008 a 010 pueden ir en paralelo cuando llegue el prototipo.

**Preguntas para el ADR de stack (MEG-27):**
- ¿Una app Next.js con el CMS dentro o un monorepo con dos apps?
- Base de datos y ORM.
- Autenticación y roles.
- Almacenamiento de medios: ¿basta la capa gratuita de R2 para unos 10 GB de video, o conviene enlazar YouTube o Vimeo?
- Librería de componentes del CMS y editor de texto enriquecido.
- ¿Seguimos en Railway?
- Cómo se refresca el contenido publicado (RNF-07).
- Tareas programadas: publicación, caducidad y retirada.
- Control de ediciones concurrentes (RF-33).

## Ruta corta
Cambios de una frase y 1–2 archivos, sin spec (siguen pasando por su revisión de 1 stage).

| Fecha | Issue | Cambio | SHA |
|---|---|---|---|
