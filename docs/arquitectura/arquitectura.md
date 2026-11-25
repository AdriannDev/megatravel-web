# Arquitectura

Estado: **vigente** con ADR-001 aceptado (`714e575`, MEG-9) (2026-11-25).

## Vista general
Una sola aplicación Next.js 16 que contiene la web pública y el CMS (Payload 3). Sin servicios propios adicionales.

```
Asesor ──HTTPS──▶ Railway: app Next.js + Payload ──▶ PostgreSQL (Railway)
Editor ──HTTPS──▶   ├─ /           web pública (Server Components, render por solicitud)
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
- **Caché y vigencia (RF-07, RF-18, RF-23)**. Tres garantías:
  - **G1 · Límite de tiempo.** Ninguna respuesta pública muestra un banner, unos cupos o una salida después de su límite, **tampoco la primera solicitud posterior al límite con la caché caliente**.
  - **G2 · Publicación de datos con límite.** Cuando el CMS confirma al editor una escritura de un banner, unos cupos o una salida (respuesta 2xx de la REST de Payload), **la primera respuesta pública posterior usa lo publicado**. Vale también si el editor adelanta un límite a una hora ya pasada o si hubo una lectura concurrente durante la escritura.
  - **G3 · Publicación del resto del contenido.** Tras la confirmación al editor, las solicitudes públicas que empiezan después devuelven lo publicado. **Ninguna lectura concurrente deja en caché la versión anterior**, tampoco una que leyó el valor anterior antes del commit y termina después de la invalidación.

  Por qué no basta con invalidar: Payload ejecuta `afterChange` y `afterOperation` **dentro de la transacción**, antes del commit (`commitTransaction` es el último paso de la operación en 3.94.2). Una lectura pública concurrente ve aún la fila anterior ya confirmada. Si esa lectura escribe su resultado en la caché **después** de la última invalidación, la versión anterior queda guardada aunque se invalide después del commit: `unstable_cache` de Next 16.4.6 guarda la entrada al terminar la lectura sin comprobar si hubo una invalidación entretanto ([código](https://github.com/vercel/next.js/blob/v16.4.6/packages/next/src/server/web/spec-extension/unstable-cache.ts#L1643-L1688), [reporte](https://github.com/vercel/next.js/issues/102007)). Invalidar después del commit tampoco basta: `after()` de `next/server` se ejecuta cuando la respuesta ya se envió ([documentación](https://nextjs.org/docs/app/api-reference/functions/after)), así que una solicitud que llega entre el 2xx y la invalidación lee la entrada anterior caliente e incumple G3. Además, `revalidateTag(tag, 'max')` sirve la versión anterior a la siguiente solicitud mientras revalida en segundo plano. Cómo se cumple:
  - **v1 sin caché de datos.** Todas las lecturas públicas (programas, zonas, destinos, home, configuración, banners, cupos y salidas) van a PostgreSQL con la Local API en cada solicitud: no pasan por la caché de datos de Next. PostgreSQL solo devuelve filas confirmadas, así que la primera lectura posterior al commit ya ve lo publicado y no queda ninguna copia anterior que invalidar. Esto cumple G2 y G3 sin depender del orden de la invalidación. Es la opción más simple. No hay una opción de caché condicionada a una prueba dentro de la spec 001.
  - **Vigencia evaluada al servir (G1).** Funciones puras de `src/lib` reciben la hora de la solicitud y filtran los datos leídos: inicio incluido, fin excluido; cupos con la validez configurada, 72 h por defecto; corte a las 00:00 America/Lima. Las páginas públicas se renderizan por solicitud: no usan ISR (`revalidate`) ni caché de ruta completa, porque ISR sirve la versión anterior a la primera solicitud tras el intervalo y su invalidación tiene la misma carrera con el commit.
  - **Sensores que lo mantienen.** Regla global de dependency-cruiser `sin-cache-de-datos`: nadie importa `next/cache`. ESLint `no-restricted-syntax` rechaza la directiva `"use cache"` y la exportación `revalidate` en `src/**`. `next.config.ts` no activa `cacheComponents` (se revisa en el diff, porque queda fuera del escaneo).
  - **Habilitar caché de datos requiere ADR**, para cualquier contenido. El ADR debe resolver la réplica única (la caché vive en la memoria del proceso y `revalidateTag` solo invalida esa instancia), las escrituras de `scripts/` fuera de una solicitud de Next (spec 008) y demostrar en la compilación de producción (`next build` + `next start`), sin depender de tiempos:
    - **Caché caliente:** con la entrada anterior ya en caché, la primera solicitud pública iniciada después del 2xx del CMS, sin esperar ninguna señal de invalidación, devuelve lo publicado. Con `after()` + `revalidateTag` esta prueba no pasa, por lo dicho arriba.
    - **Orden de la carrera:** una lectura obtiene el valor anterior y se pausa; se publica por REST y se espera el 2xx; se libera la lectura; se espera de forma determinista a que termine su intento de escritura en la caché (no basta con que devuelva el resultado); las solicitudes siguientes devuelven lo publicado.
    - **G2** con sus pruebas, si el contenido tiene límites.
  - **Sin caché compartida del HTML.** Las páginas públicas salen sin `s-maxage` (comportamiento por defecto de Next en rutas dinámicas). Poner una CDN o un proxy con caché delante de ellas requiere ADR.
  - **Coste aceptado**: un render de servidor y unas consultas indexadas a PostgreSQL por solicitud. La spec 009 lo mide contra RNF-01. Si no se cumple, se abre ADR; no se relajan G1, G2 ni G3.
  - **Pruebas obligatorias.** Todas precalientan con una primera solicitud pública, para que cualquier caché que intervenga esté caliente, y no simulan el reloj del servidor:
    - **Lectura inmediata tras publicar (G3)**, spec 001: con `/` ya servido una vez, se actualiza por la REST del CMS, con sesión, el `alt` del documento de `medios` que muestra `/`; **la primera solicitud a `/` iniciada tras el 2xx** muestra el valor nuevo. La spec 003 repite la prueba en cada colección y global públicos.
    - **G1 (vencimiento)**, banners y cupos, en las specs de RF-07 y RF-18: el fixture fija el límite a pocos segundos de la hora real; **la primera respuesta posterior al límite** ya no muestra el elemento.
    - **G1 (vencimiento)**, salidas (RF-23, si se confirma): el corte solo cae a las 00:00 America/Lima, así que no se puede fijar a pocos segundos de la hora real. La spec de RF-23 acuerda una prueba determinista que se pueda ejecutar a cualquier hora y conserve la medianoche como límite. Propuesta: el fixture calcula la fecha actual en Lima al arrancar y crea una salida con corte en la fecha de hoy (ya retirada) y otra con corte mañana (visible); si la prueba arranca a menos de un minuto de la medianoche de Lima, espera a que pase antes de calcular. Los bordes exactos (23:59:59,999 y 00:00:00 en Lima) los cubren los tests unitarios de la función pura.
    - **G2 (publicación)**, en las mismas specs: desde la REST del CMS, con sesión de editor, se adelanta el límite a una hora ya pasada (el fin del banner, la validez de los cupos o la fecha de corte); **la primera respuesta pública tras la respuesta 2xx del CMS** ya no muestra el elemento. Una variante lanza una lectura pública concurrente mientras la escritura está abierta (p. ej. un hook de prueba que retrasa el commit) y comprueba lo mismo.
    - Tests unitarios de la función de `src/lib` en los bordes.
  - RF-23 sigue marcado `[NEEDS CLARIFICATION]` en `requisitos.md` (el Board no confirmó si se mantiene el retiro automático). Si se confirma, usa este mismo mecanismo. Si no, la regla no se implementa y la salida se retira a mano. En ningún caso hay cron.
- **Vista previa (RF-39/40)**: Live Preview de Payload + Draft Mode de Next en `/preview`, solo con sesión del CMS, `noindex` y sin caché.
- **Redirecciones (RF-45, RF-45b, RF-45c)**: en `next.config` o en `src/proxy.ts` (el antiguo middleware de Next, renombrado en Next 16), según lo que fije la spec 009.

## Capas y dependencias permitidas
La spec 001 traduce cada fila a una regla `forbidden` de dependency-cruiser y cada regla global a otra.

**Cómo se lee la tabla**
- La columna "Puede depender de" es **exhaustiva**: todo lo que no aparece está prohibido. Cada fila es una regla con `from.path` = la carpeta, `from.pathNot` = los tests (`\.test\.tsx?$`, que tienen su propia fila) y `to.pathNot` = la lista. Añadir una dependencia a una capa exige cambiar esta tabla en la misma spec y que el Arquitecto lo apruebe.
- Las rutas son relativas a la raíz del repo. Los paquetes son los de `node_modules` y se escriben sin subruta (`next` incluye `next/image`, `next/navigation`, etc.; `next/cache` lo prohíbe la regla global `sin-cache-de-datos`), salvo donde la fila indica una subruta. "Node" son los módulos integrados de Node.js.
- `@payload-config` es el alias de `src/payload.config.ts`. dependency-cruiser lo resuelve con el `tsconfig.json` y lo trata como ese archivo.
- Las importaciones de solo tipos (`import type`) **no cuentan** como dependencia: el escaneo usa `tsPreCompilationDeps: false`, que descarta los imports de tipos al compilar. ESLint exige `import type` en todo import usado solo como tipo, para que no se cuele como dependencia de ejecución. Por eso `payload-types.ts` y los tipos de `payload` se pueden usar en cualquier capa.
- Alcance del escaneo: `depcruise src scripts tests`. Los archivos de configuración de la raíz (`next.config.ts`, `postcss.config.mjs`, `eslint.config.mjs`, `vitest.config.ts`, `playwright.config.ts`, `.dependency-cruiser.cjs`) quedan fuera del escaneo. Solo pueden importar los paquetes de su herramienta (y `@payloadcms/next` en `next.config.ts`) y se revisan en el diff.

| Capa | Carpeta (origen de la regla) | Puede depender de (exhaustivo) |
|---|---|---|
| Utilidades de dominio | `src/lib/` | `src/lib/` |
| Control de acceso | `src/access/` | `src/access/`, `src/lib/` |
| Modelo de contenido | `src/collections/`, `src/globals/` | `src/collections/`, `src/globals/`, `src/access/`, `src/lib/`; `payload`. El panel a medida se referencia por ruta de texto en la config, no por import. |
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
- `sin-cache-de-datos`: nadie importa `next/cache` (v1 sin caché de datos; ver «Caché y vigencia»).
- Ningún archivo importa de `bloqueosweb` ni se conecta a su base (art. 20).

**Frontera cliente/servidor.** dependency-cruiser no puede seleccionar un módulo por la directiva `"use client"`, así que la frontera se convierte en una regla de rutas con dos sensores:
1. **Convención de nombre (ESLint).** Todo archivo con `"use client"` se llama `*.client.ts` o `*.client.tsx`. Lo comprueba la regla `no-restricted-syntax` de ESLint (núcleo, sin plugin) con el selector `Program > ExpressionStatement[directive='use client']`, activa en `src/**` salvo `**/*.client.{ts,tsx}`, `src/app/(payload)/` y los dos archivos especiales que Next obliga a ser de cliente: `error.tsx` y `global-error.tsx`. Un `"use client"` en otro archivo rompe `lint`. El resto de archivos especiales de Next (`page`, `layout`, `route`…) no son módulos de cliente.
2. **Alcance transitivo (dependency-cruiser).** Regla `cliente-sin-servidor` con `from.path` = `(\.client\.tsx?|/(global-)?error\.tsx)$` y `to.reachable: true`. Prohíbe alcanzar, directamente o a través de otros módulos, `src/payload.config.ts`, `src/collections/`, `src/globals/`, `src/access/`, `src/migrations/` y los paquetes `payload`, `@payloadcms/db-postgres`, `@payloadcms/storage-s3` y `@payloadcms/next`. No se sigue dentro de `node_modules` (`doNotFollow`), así que `@payloadcms/ui` está permitido en el panel.

Pruebas de los sensores en la spec 001. Cada caso es un archivo que el sensor debe rechazar en CI y que las reglas de carpeta permitirían por sí solas:
- (a) `src/app/(frontend)/x.client.tsx` importa `@payload-config` (regla `cliente-sin-servidor`);
- (b) `src/app/(frontend)/x.client.tsx` importa un módulo de servidor de la misma carpeta que importa `payload` (regla `cliente-sin-servidor`, por alcance transitivo);
- (c) un archivo de `src/app/(frontend)/` sin sufijo `.client` declara `"use client"` (ESLint, `no-restricted-syntax`);
- (d) un caso por regla de fila, como `src/components/x.tsx` → `payload` (regla de la fila de UI pública).

Cómo se ejecutan sin romper la CI normal:
- Los casos se guardan como **texto**, no como código analizable: cadenas dentro del test o archivos con extensión no analizada (p. ej. `.fixture`) en `tests/sensores/`. Así `lint`, `typecheck`, `depcruise`, `knip` y `jscpd` del repo no los ven.
- El test escribe cada caso en un **árbol temporal** con su ruta real de `src/`, por ejemplo `src/app/(frontend)/x.client.tsx`. El árbol vive bajo una carpeta del repo ignorada por git y excluida de los sensores, para resolver `node_modules` y el alias `@payload-config` con un `tsconfig.json` del árbol.
- Sobre ese árbol, el test ejecuta las **mismas configuraciones** del repo (`.dependency-cruiser.cjs` y `eslint.config.mjs`) con la API de cada herramienta.
- Para cada caso, el test comprueba **el nombre de la regla** que lo rechaza (`cliente-sin-servidor`, `no-restricted-syntax`, la regla de la fila) y no solo que haya algún error.
- Un **caso de control** permitido (p. ej. `x.client.tsx` que importa `src/lib/`) debe pasar sin errores, para probar que los rechazos vienen de la regla y no del árbol.

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
