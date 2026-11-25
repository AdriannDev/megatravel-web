# Arquitectura

Estado: **propuesta** con ADR-001 (2026-11-25). Se vuelve vigente cuando el Code Reviewer acepte ADR-001.

## Vista general
Una sola aplicación Next.js 16 que contiene la web pública y el CMS (Payload 3). Sin servicios propios adicionales.

```
Asesor ──HTTPS──▶ Railway: app Next.js + Payload ──▶ PostgreSQL (Railway)
Editor ──HTTPS──▶   ├─ /           web pública (Server Components, caché de Next)
                    ├─ /admin      panel de Payload con tema y vistas a medida
                    ├─ /api        REST de Payload (solo panel y vista previa)
                    └─ /preview    vista previa autenticada, noindex
                         │
                         └──S3 API──▶ Cloudflare R2 (imágenes, video, fotos de pasajeros)
Navegador ──▶ R2 (medios públicos) · Meganet (reservas, enlace saliente) · Café Megatravel (descriptivo)
```

- **Lectura pública**: las rutas de `src/app/(frontend)` llaman a la Local API de Payload (`getPayload` + `find`/`findGlobal`) en el servidor y pasan datos planos por props a los componentes. Sin repositorios ni DTOs (arts. 4–5).
- **Campos públicos (RNF-10)**: las lecturas públicas usan `overrideAccess: false` sin usuario, para que el control de acceso de campo de Payload oculte los campos de gestión (motivos, notas, usuarios, historial). Un test de contrato lo verifica.
- **Escritura**: solo desde el panel de Payload. La autorización vive en `src/access` (matriz rol × acción, RF-37/RF-38) y se aplica en servidor en cada colección.
- **Caché y vigencia (RF-07, RF-18, RF-23)**. Garantía: ninguna respuesta pública muestra un banner, unos cupos o una salida después de su límite, **tampoco la primera solicitud posterior al límite con la caché ya caliente**. Cómo se cumple:
  - Se cachea la **lectura**, no la página: el resultado de la Local API, sin filtrar por vigencia, se guarda en la caché de datos de Next con etiquetas por colección o global. Los hooks `afterChange`/`afterDelete` de Payload invalidan esas etiquetas al publicar. La duración de esta caché no influye en la vigencia.
  - La **vigencia se evalúa al servir cada solicitud**: funciones puras de `src/lib` reciben la hora de la solicitud y filtran los datos leídos (inicio incluido, fin excluido; cupos con la validez configurada, 72 h por defecto; corte a las 00:00 America/Lima). Las páginas que muestran datos con límite se renderizan por solicitud: no usan ISR (`revalidate`) ni caché de ruta completa, porque ISR sirve la versión anterior a la primera solicitud tras el intervalo. La API concreta de Next (p. ej. `'use cache'` + `cacheTag` en la lectura y `connection()` antes de leer la hora) la fija la spec 001.
  - Ninguna caché compartida guarda el HTML de esas páginas: salen sin `s-maxage` (comportamiento por defecto de Next en rutas dinámicas). Poner una CDN o un proxy con caché delante de ellas requiere ADR.
  - Coste aceptado: un render de servidor por solicitud sobre datos ya cacheados en el proceso, sin consulta a PostgreSQL. La spec 009 lo mide contra RNF-01.
  - **Prueba obligatoria** en la spec que implemente cada regla (banners RF-07, cupos RF-18, salidas RF-23): con la caché precalentada por una primera solicitud, **la primera respuesta posterior al límite** ya no muestra el elemento. El fixture fija el límite a pocos segundos de la hora real, así que no se simula el reloj del servidor. Además, tests unitarios de la función de `src/lib` en los bordes.
  - RF-23 sigue marcado `[NEEDS CLARIFICATION]` en `requisitos.md` (el Board no confirmó si se mantiene el retiro automático). Si se confirma, usa este mismo mecanismo. Si no, la regla no se implementa y la salida se retira a mano. En ningún caso hay cron.
- **Vista previa (RF-39/40)**: Live Preview de Payload + Draft Mode de Next en `/preview`, solo con sesión del CMS, `noindex` y sin caché.
- **Redirecciones (RF-45, RF-45b, RF-45c)**: en `next.config` o en `src/proxy.ts` (el antiguo middleware de Next, renombrado en Next 16), según lo que fije la spec 009.

## Capas y dependencias permitidas
La spec 001 traduce cada fila a una regla `forbidden` de dependency-cruiser y cada regla global a otra.

**Cómo se lee la tabla**
- La columna "Puede depender de" es **exhaustiva**: todo lo que no aparece está prohibido. Cada fila es una regla con `from.path` = la carpeta, `from.pathNot` = los tests (`\.test\.tsx?$`, que tienen su propia fila) y `to.pathNot` = la lista. Añadir una dependencia a una capa exige cambiar esta tabla en la misma spec y que el Arquitecto lo apruebe.
- Las rutas son relativas a la raíz del repo. Los paquetes son los de `node_modules` y se escriben sin subruta (`next` incluye `next/cache`, `next/image`, etc.), salvo donde la fila indica una subruta. "Node" son los módulos integrados de Node.js.
- `@payload-config` es el alias de `src/payload.config.ts`. dependency-cruiser lo resuelve con el `tsconfig.json` y lo trata como ese archivo.
- Las importaciones de solo tipos (`import type`) **no cuentan** como dependencia: el escaneo usa `tsPreCompilationDeps: false`, que descarta los imports de tipos al compilar. ESLint exige `import type` en todo import usado solo como tipo, para que no se cuele como dependencia de ejecución. Por eso `payload-types.ts` y los tipos de `payload` se pueden usar en cualquier capa.
- Alcance del escaneo: `depcruise src scripts tests`. Los archivos de configuración de la raíz (`next.config.ts`, `postcss.config.mjs`, `eslint.config.mjs`, `vitest.config.ts`, `playwright.config.ts`, `.dependency-cruiser.cjs`) quedan fuera del escaneo. Solo pueden importar los paquetes de su herramienta (y `@payloadcms/next` en `next.config.ts`) y se revisan en el diff.

| Capa | Carpeta (origen de la regla) | Puede depender de (exhaustivo) |
|---|---|---|
| Utilidades de dominio | `src/lib/` | `src/lib/` |
| Control de acceso | `src/access/` | `src/access/`, `src/lib/` |
| Modelo de contenido | `src/collections/`, `src/globals/` | `src/collections/`, `src/globals/`, `src/access/`, `src/lib/`; `payload`, `next/cache` (invalidar etiquetas en hooks). El panel a medida se referencia por ruta de texto en la config, no por import. |
| Configuración de Payload | `src/payload.config.ts` | `src/collections/`, `src/globals/`, `src/access/`, `src/lib/`; `payload`, `@payloadcms/db-postgres`, `@payloadcms/storage-s3`, `sharp`; Node `path` y `url` |
| Panel a medida | `src/admin/` | `src/admin/` (incluidos sus CSS), `src/components/`, `src/lib/`; `react`, `next`, `@payloadcms/ui`, `@payloadcms/next` (plantillas de vista) |
| UI pública | `src/components/` | `src/components/`, `src/lib/`; `react`, `next` |
| Rutas públicas | `src/app/(frontend)/` | `src/app/(frontend)/`, `src/components/`, `src/lib/`, `src/styles/` (CSS global desde el layout), `src/payload.config.ts` (`@payload-config`); `payload`, `next`, `react`; `@payloadcms/live-preview-react` cuando la spec de vista previa lo instale |
| Proxy de Next (redirecciones) | `src/proxy.ts` | `src/lib/`; `next` |
| Estilos | `src/styles/` | Solo archivos CSS (tokens y `@import "tailwindcss"`). dependency-cruiser no analiza CSS; lo que sí controla es quién importa esta carpeta (solo `src/app/(frontend)/`). |
| Scripts | `scripts/` | `scripts/`, `src/lib/`, `src/payload.config.ts` (`@payload-config`); `payload`; Node `fs`, `path`, `url` |
| Tests | `src/**/*.test.ts(x)`, `tests/` | Sin regla de capa: cualquier archivo de `src/`, `tests/`, paquetes de ejecución, herramientas de test que fije el ADR-002 y Node. Aplican las reglas globales. |
| Generado por Payload | `src/app/(payload)/`, `src/migrations/`, `src/payload-types.ts` | Fuera de las reglas de capa como origen (no se edita a mano). Aplican las reglas globales. Ninguna capa los importa, salvo los tipos de `payload-types.ts`. |

**Reglas globales** (origen: todo el escaneo)
- Sin dependencias circulares.
- Sin módulos sin resolver ni paquetes que no estén en `package.json`.
- Ningún archivo fuera de los tests importa un paquete de `devDependencies` ni un test (`*.test.ts(x)`, `tests/`). Fuera de `scripts/`, nadie importa `scripts/`.
- Acceso a datos **solo por Payload**: `pg`, `drizzle-orm` y `@payloadcms/drizzle` solo se importan desde `src/migrations/`. SQL propio requiere ADR.
- Ningún archivo importa de `bloqueosweb` ni se conecta a su base (art. 20).

**Frontera cliente/servidor.** dependency-cruiser no puede seleccionar un módulo por la directiva `"use client"`, así que la frontera se convierte en una regla de rutas con dos sensores:
1. **Convención de nombre (ESLint).** Todo archivo con `"use client"` se llama `*.client.ts` o `*.client.tsx`. Lo comprueba la regla `no-restricted-syntax` de ESLint (núcleo, sin plugin) con el selector `Program > ExpressionStatement[directive='use client']`, activa en `src/**` salvo `**/*.client.{ts,tsx}`, `src/app/(payload)/` y los dos archivos especiales que Next obliga a ser de cliente: `error.tsx` y `global-error.tsx`. Un `"use client"` en otro archivo rompe `lint`. El resto de archivos especiales de Next (`page`, `layout`, `route`…) no son módulos de cliente.
2. **Alcance transitivo (dependency-cruiser).** Regla `cliente-sin-servidor` con `from.path` = `(\.client\.tsx?|/(global-)?error\.tsx)$` y `to.reachable: true`. Prohíbe alcanzar, directamente o a través de otros módulos, `src/payload.config.ts`, `src/collections/`, `src/globals/`, `src/access/`, `src/migrations/` y los paquetes `payload`, `@payloadcms/db-postgres`, `@payloadcms/storage-s3` y `@payloadcms/next`. No se sigue dentro de `node_modules` (`doNotFollow`), así que `@payloadcms/ui` está permitido en el panel.

Pruebas de la frontera en la spec 001: fixtures que el sensor debe rechazar en CI. Cada uno es un caso que las reglas de carpeta permitirían por sí solas:
- (a) `src/app/(frontend)/x.client.tsx` importa `@payload-config`;
- (b) `src/app/(frontend)/x.client.tsx` importa un módulo de servidor de la misma carpeta que importa `payload`;
- (c) un archivo de `src/app/(frontend)/` sin sufijo `.client` declara `"use client"` (lo rechaza ESLint).

## Datos
- **PostgreSQL** gestionado en Railway, una base por entorno. El esquema lo define la config de Payload; los cambios se versionan con `payload migrate:create` en `src/migrations/` y se aplican en el despliegue. En producción no se usa `push` de esquema.
- **Modelo principal** (detalle en la spec 003): programas, salidas, zonas, destinos, orígenes, navieras, promociones, banners, medios, fotos de pasajeros, usuarios del CMS, historial; globals de home y configuración. Fecha de salida como fecha de calendario `AAAA-MM-DD`; precios en USD.
- **Medios** en un bucket R2 propio (no el de la web actual). Las fotos de pasajeros se eliminan del bucket, con sus variantes, al retirarlas (RF-34b).
- **Copias (RNF-13)**: volcados de PostgreSQL programados y copia del bucket R2; procedimiento y restauración de prueba en la spec 001 (base) y la spec 010 (runbook).
- **Migración (RF-47, spec 008)**: scripts en `scripts/` que leen exportaciones y escriben con la Local API; idempotentes por identidad MTPE + origen + fecha.

## Entornos
| Entorno | Para qué | Cómo se despliega |
|---|---|---|
| Local | Desarrollo y tests | `npm run dev` con PostgreSQL local (contenedor `postgres` vía Docker Compose, a fijar en la spec 001) y R2 de desarrollo o almacenamiento local de Payload |
| CI | Sensores y tests en cada push y PR | GitHub Actions con servicio PostgreSQL efímero |
| Staging | Revisión del Board y QA con datos de prueba | Railway, entorno `staging`, despliegue automático desde `develop` |
| Producción | Web pública en el dominio actual (tras la spec 010) | Railway, entorno `production`, despliegue desde `main` (solo humano, tras CP4) |

## Decisiones
Ver `adr/`. ADR-001: stack, CMS, base de datos y hosting. ADR-002 (spec 001): calidad y sensores.
