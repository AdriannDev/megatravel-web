# ADR-001 · Stack, CMS, base de datos y hosting

Estado: **propuesto** · Arquitecto · 2026-11-25 · revisión: Code Reviewer (MEG-9). Fecha de revisión de la decisión: al cerrar la spec 004 (editor de programas) y la spec 009 (rendimiento).

## Contexto
Megatravel Web necesita una web pública rápida (home, listados, detalle; RNF-01: Core Web Vitals en verde en móvil y ≥ 80 de rendimiento) y un CMS a medida para Editor, Marketing y Administrador, con roles validados en servidor, vista previa, historial, subida de imágenes, video y fotos de pasajeros que se borran de verdad (RF-26 a RF-43, RF-34b, RNF-07 a RNF-10). La migración parte de exportaciones de la web actual (Next.js 16 + Payload 3 + PostgreSQL en Railway, RF-47) y la web actual no se toca (art. 20, RNF-14). El Board prefiere Next.js, React, Tailwind, PostgreSQL y Railway, sin tope fijo de costo pero con gasto óptimo (RNF-12).

Entradas: `docs/producto/brief.md` y `docs/producto/requisitos.md` (aprobados, SHA `0dfccfe`, MEG-7) y `docs/investigacion/stack-y-cms.md` (MEG-8).

## Opciones consideradas

### CMS y aplicación
| Opción | A favor | En contra |
|---|---|---|
| **A. Next.js 16 + Payload 3 en la misma app + PostgreSQL** | Una sola app y un solo servicio. La web lee con la Local API en el mismo proceso, sin llamadas de red. Ya resuelve autenticación con hash y caducidad de sesión, control de acceso por operación, documento y campo (RF-38, RNF-10), borradores y versiones (RF-41b), Live Preview (RF-39), subidas con variantes y adaptador S3/R2 (RF-34, RF-34b) y migraciones de esquema. El panel admite vistas y componentes React propios (RF-43). Es el stack de la web actual: menor esfuerzo de migración y modelo de datos conocido. Licencia MIT. | El diseño propio del panel tiene un límite: lo que no cubran las vistas y componentes personalizados obliga a construir esa pantalla aparte. Acopla el contenido al modelo de Payload. Ciclo de versiones rápido con requisito de rango de Next (Payload 3.94.2 exige Next ≥ 16.4.5 y < 17). |
| B. Next.js + CMS propio sobre PostgreSQL | Control total del panel y del esquema. | Hay que construir y asegurar lo que Payload ya da: sesiones, hash de contraseñas, matriz de permisos en servidor, borradores, vista previa, subidas, variantes de imagen, borrado en almacenamiento, migraciones, historial. Contradice el art. 1 (lo mínimo) y multiplica la superficie de seguridad (specs 001, 003, 004 son sensibles). Mayor esfuerzo de migración. |
| C. Next.js + Strapi 5 Community + PostgreSQL | Panel maduro, RBAC y biblioteca de medios. | Segundo servicio que operar y pagar; la web consulta por API de red (peor caché fría). La vista previa junto al editor es de los planes de pago (Growth, USD 45/mes). Migración con transformación completa del modelo. Personalización del panel con menos encaje con el diseño propio (no confirmado). |

### Hosting
| Opción | A favor | En contra |
|---|---|---|
| **Railway (Pro): un servicio Next.js + Payload y PostgreSQL gestionado** | Preferencia del Board y plataforma que el equipo ya opera con la web actual. Proceso de larga duración: encaja con Payload (subidas, `sharp`, conexiones persistentes a PostgreSQL). Entornos separados (staging, producción) en el mismo proyecto. Facturación por consumo. | Suelo de USD 20/mes en Pro. Sin CDN de páginas integrada: el rendimiento depende del render de servidor con consultas indexadas y de servir medios desde R2. |
| Vercel + PostgreSQL gestionado externo (p. ej. Neon) | Plataforma nativa de Next.js, CDN global y previews por PR. | Dos proveedores y dos facturas; ejecución serverless que obliga a usar pooling de conexiones con Payload y limita tiempo y memoria en subidas e imágenes. Fuera de la preferencia del Board. Costo no estudiado por el Researcher. |

### Medios (imágenes, video, fotos de pasajeros)
| Opción | A favor | En contra |
|---|---|---|
| **Cloudflare R2 (bucket nuevo) con `@payloadcms/storage-s3`; video como MP4 en R2 con imagen póster** | Egreso sin cargo y franquicia de 10 GB-mes; S3 compatible (reversible); Megatravel ya usa R2. Borrar el documento borra el objeto (RF-34b, se prueba en la spec 004). Sin servicio de video extra. | El video no se transcodifica ni adapta al ancho de banda; el editor sube un MP4 ya optimizado. Las copias del bucket se organizan aparte (RNF-13). |
| Volumen de Railway | Sin proveedor extra. | Egreso facturado, almacenamiento atado al servicio, copias y escalado peores. |
| Cloudflare Stream para video | Streaming adaptativo. | USD 5 por 1.000 min almacenados + USD 1 por 1.000 min entregados; una dependencia más sin necesidad demostrada. Se reconsidera solo si el hero de video rompe RNF-01. |

## Decisión
Se elige **A**: una única aplicación **Next.js 16 (App Router) + React 19 + Payload 3 + PostgreSQL**, con **Tailwind CSS 4** en la web pública, desplegada en **Railway Pro** (un servicio de app + PostgreSQL gestionado) y medios en **Cloudflare R2** con un bucket propio de este proyecto. Payload es el CMS y el framework de datos: la web lo usa directamente con su Local API, sin repositorios, DTOs ni capa propia encima (arts. 4 y 5). El "CMS a medida" (RF-43) se logra con el tema, componentes y vistas personalizadas del panel de Payload, no con un panel nuevo. B se descarta por coste y riesgo de seguridad sin beneficio para la v1; C por un segundo servicio y vista previa de pago.

### Dependencias de ejecución autorizadas por este ADR
| Paquete | Para qué |
|---|---|
| `next`, `react`, `react-dom` | Framework de la web y del panel. |
| `payload`, `@payloadcms/next`, `@payloadcms/ui` | CMS en la misma app; `ui` solo para componentes del panel a medida. |
| `@payloadcms/db-postgres` | Adaptador de PostgreSQL y migraciones. |
| `@payloadcms/storage-s3` | Subidas a R2 (API S3). |
| `sharp` | Variantes de imagen de Payload y optimización de `next/image` en self-hosting. |
| `tailwindcss`, `@tailwindcss/postcss` | Estilos de la web pública a partir de tokens (spec 002). |
| `typescript` | Tipos (dev). |

Dependencias que estos paquetes exigen como pares: quedan cubiertas y la spec 001 las lista con versión. En particular, `graphql` (`^16.8.1`) es dependencia par de `payload` y de `@payloadcms/next`, así que **se instala aunque la API GraphQL esté desactivada**: la config usa `graphQL: { disable: true }` y el scaffold elimina las rutas `src/app/(payload)/api/graphql/` y `graphql-playground/` de la plantilla.

Autorizados **solo cuando una spec los necesite**, sin ADR nuevo (paquetes oficiales de Payload, MIT). No se instalan en la spec 001:
- `@payloadcms/richtext-lexical`: cuando haga falta texto con formato (p. ej. condiciones del programa).
- `@payloadcms/live-preview-react`: en la spec de vista previa (RF-39).

Quien los instale actualiza en la misma spec la tabla de capas de `arquitectura.md`. Las herramientas de calidad (lint, tests, jscpd, knip, dependency-cruiser, Lighthouse CI, escaneo de secretos) se deciden en el **ADR-002 · Calidad y sensores** de la spec 001. Cualquier otra dependencia necesita su ADR.

Versiones de partida (MEG-8, 2026-11-25): Payload **3.94.x**, Next.js **16.4.x (≥ 16.4.5)**, Node.js **24 LTS ≥ 24.22.3** (ver el scaffold, abajo), npm (incluido en Node, sin gestor extra). La versión mayor de PostgreSQL será la que ofrezca Railway y soporte el adaptador; la spec 001 la fija en `package.json`/`engines` y en `arquitectura.md`.

### Scaffold de partida: plantilla `blank` de Payload 3.94.2 adaptada
La plantilla oficial no se usa tal cual. Trae cosas que este ADR no autoriza ([manifiesto](https://github.com/payloadcms/payload/blob/v3.94.2/templates/blank/package.json), [config](https://github.com/payloadcms/payload/blob/v3.94.2/templates/blank/src/payload.config.ts)). La spec 001 aplica estos cambios y los comprueba en el diff:
- **Base de datos**: sustituye `@payloadcms/db-mongodb` (`mongooseAdapter`) por `@payloadcms/db-postgres` (`postgresAdapter`).
- **Editor**: retira `@payloadcms/richtext-lexical` de `package.json` y la línea `editor: lexicalEditor()` de la config. En 3.94.2 `editor` es opcional en `Config` y sin campos `richText` no se usa. Regenera el import map (`payload generate:importmap`) para que no quede ninguna referencia al editor.
- **GraphQL**: `graphQL: { disable: true }`, sin las dos rutas de GraphQL. `graphql` se queda como dependencia par.
- **Herramientas de desarrollo** de la plantilla (`cross-env`, `tsx`, ESLint, Vitest, Playwright…): se quedan solo las que justifique el ADR-002. El resto se retira.
- **Node.js**: Payload 3.94.2 y `@payloadcms/next` exigen `^22.23.5 || ^24.22.3 || >=26.13.1`. Dentro de Node 24 LTS el mínimo es **24.22.3**. La misma versión se fija en los tres sitios:
  - local: `.nvmrc` con la versión exacta (24.22.3 o el último parche de la 24 disponible al crear el scaffold);
  - CI: `actions/setup-node` con `node-version-file: .nvmrc`;
  - Railway: la misma versión en la configuración de build.
  `package.json` declara `"engines": { "node": ">=24.22.3 <25" }`. La spec 001 pega en el handoff la versión efectiva que muestran el log de CI y el de build de Railway.

### Lo que no se usa en la v1 (y por qué)
- Motor de búsqueda externo: el catálogo son cientos de salidas; los filtros (RF-09) se resuelven con consultas de Payload sobre PostgreSQL.
- Cron de retiro: la vigencia (corte RF-23, fin de banner RF-07, cupos RF-18) se evalúa al servir cada solicitud. En v1 las lecturas públicas van a PostgreSQL sin caché de datos y ninguna página pública usa ISR. Caché de datos de Next: no se usa en v1 para ningún contenido (un sensor rechaza `next/cache` y `"use cache"`); habilitarla requiere un ADR con las pruebas de caché caliente y de orden. Las garantías G1, G2 y G3 y sus pruebas están en `arquitectura.md`.
- API GraphQL de Payload y `/api/public/catalog`: no hay consumidor. GraphQL se desactiva (`graphql` sigue instalado como dependencia par) y el catálogo no se crea, salvo que una spec lo pida.
- Librería de validación aparte (Zod u otras): se usan las validaciones de campo de Payload y funciones puras en `src/lib`.

### Costo mensual estimado (RNF-12)
| Concepto | Estimación |
|---|---|
| Railway Pro (incluye USD 20 de consumo): app + PostgreSQL de producción | USD 20–21 (el plan cubre los primeros USD 20 de consumo; consumo estimado USD 14,6–20,6 con 1,2–1,8 GB RAM, 0,1 vCPU, 2 GB volumen, 5 GB egreso; MEG-8) |
| Entorno de staging en Railway (encendido solo durante revisiones) | USD 0–5 adicionales sobre el consumo |
| R2: imágenes y video dentro de la franquicia de 10 GB-mes | USD 0–2 |
| **Total estimado** | **USD 20–28/mes**, sin impuestos. No medido: se verifica con tráfico real en la spec 009 y se anota aquí. |

## Consecuencias
- Positivas: un solo despliegue y un solo lenguaje; autenticación, permisos, vista previa, versiones y subidas vienen del framework y se configuran, no se construyen; la migración puede reutilizar el modelo de programas y salidas de la web actual; costo cercano al suelo de Railway Pro.
- Negativas / deuda aceptada:
  - Dependencia fuerte de Payload (modelo, panel, migraciones). Las actualizaciones de Payload y Next van juntas y se prueban en CI.
  - El diseño propio del CMS está limitado a lo que permiten las vistas y componentes de Payload. Si el editor de programas (spec 004) no cabe en una vista personalizada, esa pantalla se construye como ruta propia de la misma app usando la Local API (salida escalonada), con su ADR.
  - Video sin transcodificación: el editor debe subir MP4 optimizado; la spec 005 fija peso y formato máximos.
  - Las copias de seguridad de R2 se resuelven aparte de las de PostgreSQL (RNF-13; procedimiento y restauración de prueba en las specs 001 y 010).
- Cómo revertir:
  - **CMS**: los datos viven en tablas PostgreSQL normales (exportables con `pg_dump`) y los medios en un bucket S3 compatible. La web pública consulta Payload solo en las rutas de `src/app/(frontend)`; los componentes de `src/components` reciben datos por props y no importan Payload (regla de capas). Cambiar de CMS implica reescribir esas consultas y el modelo editorial, no la UI pública. Mientras no haya contenido migrado (antes de la spec 008), revertir cuesta solo el trabajo de las specs 003–004.
  - **Hosting**: Next.js se construye en modo `standalone` y corre en cualquier contenedor Node; mover a otro proveedor es restaurar el volcado de PostgreSQL, apuntar las variables de entorno y cambiar el DNS. R2 no cambia.
  - **Medios**: el adaptador S3 apunta a cualquier almacenamiento compatible; mover objetos con herramientas S3 estándar y cambiar variables.

## Fuentes
Todas consultadas el 2026-11-25 (Lima) por el Researcher; detalle y enlaces en `docs/investigacion/stack-y-cms.md`.
- Payload: [Admin](https://payloadcms.com/docs/admin/overview) · [Vistas personalizadas](https://payloadcms.com/docs/custom-components/custom-views) · [Live Preview](https://payloadcms.com/docs/live-preview/overview) · [Control de acceso](https://payloadcms.com/docs/access-control/overview) · [Borradores](https://payloadcms.com/docs/versions/drafts) · [Uploads](https://payloadcms.com/docs/upload/overview) · [Adaptadores de almacenamiento](https://payloadcms.com/docs/upload/storage-adapters) · [Local API](https://payloadcms.com/docs/local-api/overview) · [PostgreSQL](https://payloadcms.com/docs/database/postgres) · [Migraciones](https://payloadcms.com/docs/database/migrations) · [Release 3.94.2](https://github.com/payloadcms/payload/releases/tag/v3.94.2) · [Manifiesto `@payloadcms/next`](https://github.com/payloadcms/payload/blob/v3.94.2/packages/next/package.json) · [Licencia](https://github.com/payloadcms/payload/blob/main/LICENSE.md)
- Next.js: [Self-hosting](https://nextjs.org/docs/app/guides/self-hosting) · [ISR](https://nextjs.org/docs/app/guides/incremental-static-regeneration) · [Draft Mode](https://nextjs.org/docs/app/guides/draft-mode) · [Video](https://nextjs.org/docs/app/guides/videos) · [Tailwind con Next.js](https://tailwindcss.com/docs/installation/framework-guides/nextjs)
- Strapi: [Preview](https://docs.strapi.io/cms/features/preview) · [Precios](https://strapi.io/pricing-cms) · [Transfer](https://docs.strapi.io/cms/features/data-management/transfer)
- Hosting y medios: [Railway, tarifas](https://railway.com/pricing) · [Railway, planes](https://docs.railway.com/pricing/plans) · [R2, precios](https://developers.cloudflare.com/r2/pricing/) · [Stream, precios](https://developers.cloudflare.com/stream/pricing/) · [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- Vercel + PostgreSQL externo: alternativa del Arquitecto, no investigada por el Researcher; su costo es **no confirmado**.
