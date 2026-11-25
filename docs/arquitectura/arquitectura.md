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
- **Caché y vigencia (RF-07, RF-18, RF-23)**. Dos garantías:
  - **G1 · Límite de tiempo.** Ninguna respuesta pública muestra un banner, unos cupos o una salida después de su límite, **tampoco la primera solicitud posterior al límite con la caché caliente**.
  - **G2 · Publicación de datos con límite.** Cuando el CMS confirma al editor una escritura de un banner, unos cupos o una salida (respuesta 2xx de la REST de Payload), **la primera respuesta pública posterior usa lo publicado**. Vale también si el editor adelanta un límite a una hora ya pasada o si hubo una lectura concurrente durante la escritura.
  - **G3 · Publicación del resto del contenido.** Lo publicado aparece en la web en milisegundos tras la confirmación, y una lectura concurrente nunca deja en caché la versión anterior de forma duradera.

  Por qué no basta con invalidar en un hook: Payload ejecuta `afterChange` y `afterOperation` **dentro de la transacción**, antes del commit (`commitTransaction` es el último paso de la operación en 3.94.2). Una lectura pública concurrente ve aún la fila anterior ya confirmada y puede repoblar la caché con ella después de la invalidación. Además, `revalidateTag(tag, 'max')` sirve la versión anterior a la siguiente solicitud mientras revalida en segundo plano. Cómo se cumple:
  - **Datos con límite: sin caché de datos.** Las lecturas de banners, de cupos y de salidas no pasan por la caché de datos de Next: la ruta las lee de PostgreSQL con la Local API en cada solicitud. PostgreSQL solo devuelve filas confirmadas, así que la primera lectura posterior al commit ya ve el límite publicado (G2) sin depender de cuándo se invalide nada. Es la opción más simple que cumple G2. Cachear estas lecturas requiere un ADR que demuestre la invalidación posterior al commit con la prueba de G2.
  - **Vigencia evaluada al servir (G1).** Funciones puras de `src/lib` reciben la hora de la solicitud y filtran los datos leídos: inicio incluido, fin excluido; cupos con la validez configurada, 72 h por defecto; corte a las 00:00 America/Lima. Las páginas que muestran datos con límite se renderizan por solicitud: no usan ISR (`revalidate`) ni caché de ruta completa, porque ISR sirve la versión anterior a la primera solicitud tras el intervalo.
  - **Resto del contenido: caché de datos con etiquetas.** Programas, zonas, destinos, home y configuración se leen con caché de datos de Next y etiquetas por colección o global. La invalidación cumple dos condiciones:
    - **expiración inmediata**: `revalidateTag(tag, { expire: 0 })`, nunca `'max'` ni otro perfil con ventana de contenido anterior. `updateTag` no sirve, porque solo existe en Server Actions y la REST de Payload es un Route Handler;
    - **efectiva después del commit**: el hook invalida y vuelve a invalidar cuando la respuesta de la REST ha terminado, es decir, después de `commitTransaction`. Mecanismo candidato: `after()` de `next/server` llamado desde el hook. La spec 001 fija la API concreta y demuestra que funciona dentro del Route Handler de Payload. Si no la demuestra, este contenido tampoco usa caché de datos.

    Así se cumple G3: la única ventana es la que va de la confirmación al editor a la segunda invalidación.
  - **Una sola instancia.** La caché de datos de Next vive en la memoria del proceso y `revalidateTag` solo invalida esa instancia. Railway corre una réplica. Escalar a varias réplicas requiere ADR (manejador de caché compartido con coordinación de etiquetas).
  - **Escrituras fuera de Next.** Los scripts de `scripts/` escriben con la Local API fuera de una solicitud de Next y no pueden invalidar etiquetas. Un script que escriba contenido cacheado en un entorno con tráfico reinicia el servicio al terminar o invalida por una ruta autenticada que fije su spec (spec 008).
  - **Sin caché compartida del HTML.** Las páginas con límites salen sin `s-maxage` (comportamiento por defecto de Next en rutas dinámicas). Poner una CDN o un proxy con caché delante de ellas requiere ADR.
  - **Coste aceptado**: un render de servidor y unas consultas indexadas a PostgreSQL por solicitud en las páginas con límites. La spec 009 lo mide contra RNF-01. Si no se cumple, se abre ADR; no se relajan G1 ni G2.
  - **Pruebas obligatorias** en la spec que implemente cada regla (banners RF-07, cupos RF-18, salidas RF-23). Todas precalientan con una primera solicitud pública, para que cualquier caché que intervenga esté caliente, y no simulan el reloj del servidor:
    - **G1 (vencimiento)**: el fixture fija el límite a pocos segundos de la hora real; **la primera respuesta posterior al límite** ya no muestra el elemento.
    - **G2 (publicación)**: desde la REST del CMS, con sesión de editor, se adelanta el límite a una hora ya pasada (el fin del banner, la validez de los cupos o la fecha de corte); **la primera respuesta pública tras la respuesta 2xx del CMS** ya no muestra el elemento. Una variante lanza una lectura pública concurrente mientras la escritura está abierta (p. ej. un hook de prueba que retrasa el commit) y comprueba lo mismo.
    - Tests unitarios de la función de `src/lib` en los bordes.

    La spec 001 demuestra G3 sobre una colección cacheada: precalentar, editar desde la REST con una lectura concurrente durante la escritura y comprobar que, terminada la segunda invalidación, la lectura pública devuelve el valor nuevo y no vuelve a la versión anterior.
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
| Modelo de contenido | `src/collections/`, `src/globals/` | `src/collections/`, `src/globals/`, `src/access/`, `src/lib/`; `payload`, `next/cache` (invalidar etiquetas en hooks), `next/server` (solo `after`, para invalidar después del commit). El panel a medida se referencia por ruta de texto en la config, no por import. |
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
