# Spec 001 · Fundaciones

Estado: aprobada · SHA aprobado: `ce6b8707321c37ede89be0272dbbeb752f5dc546` (Arquitecto, 2026-11-25)
Autor: Product Analyst · Requisitos que cubre: RF-38 (base de cuentas y roles), RNF-09, RNF-13; base técnica de RNF-01 (umbrales del ADR de calidad, Constitución art. 23) y de las specs 002–010
**Sensible: sí** (auth del CMS)

Origen: propuesta «Spec 001 · Fundaciones» v2 de MEG-9 con los cambios de v3, v4 y v5 (manda la v5 si se contradicen) y las dos sugerencias del Code Reviewer sobre `714e575`. Base: ADR-001 (aceptado) y `docs/arquitectura/arquitectura.md` (vigente). Esta spec no los contradice.

## Problema y objetivo
El equipo (agentes y Board) necesita un repo que arranque, despliegue en staging y rechace cualquier integración que rompa un sensor. Hoy no hay código. Al terminar existe la base sobre la que se construyen las specs 002–010, sin funcionalidad de negocio: scaffold, base de datos, CI con sensores, staging en Railway, copias de seguridad probadas y los comandos que usan los agentes.

## Requisitos (EARS)

### Scaffold y stack
| ID | Requisito |
|---|---|
| R1 | THE SYSTEM SHALL partir de la plantilla `blank` de Payload 3.94.2 con TypeScript estricto y npm, usando `@payloadcms/db-postgres` y sin `@payloadcms/db-mongodb`, y SHALL fijar las dependencias de ejecución par con estas versiones o rangos: `payload` y todos los `@payloadcms/*` 3.94.2; `next` ≥ 16.4.5 < 17; `react` y `react-dom` 19; `graphql` ^16.8.1; `sharp`. |
| R2 | THE SYSTEM SHALL no incluir Lexical (ni el paquete `@payloadcms/richtext-lexical` ni `editor: lexicalEditor()`) y SHALL regenerar el import map sin referencias a él. |
| R3 | THE SYSTEM SHALL tener GraphQL deshabilitado (`graphQL: { disable: true }`), sin las rutas `api/graphql` ni `graphql-playground`, conservando `graphql` solo como dependencia par. |
| R4 | THE SYSTEM SHALL fijar Node en la misma versión exacta (≥ 24.22.3 < 25) en `.nvmrc`, en CI (`node-version-file: .nvmrc`), en Railway y en `engines` (`">=24.22.3 <25"`). |
| R5 | THE SYSTEM SHALL organizar `src/` según `docs/arquitectura/mapa-de-codigo.md` y SHALL incluir una ruta `/` mínima de comprobación (R16) y un `.env.example` con todas las variables sin valores reales. |

### Datos y entorno local
| ID | Requisito |
|---|---|
| R6 | WHEN un desarrollador ejecuta `docker compose up -d db`, THE SYSTEM SHALL ofrecer un PostgreSQL local con el que `npm run dev` arranca Next y Payload en `:3000`. |
| R6b | THE SYSTEM SHALL usar una sola versión mayor de PostgreSQL, la que ofrezca Railway y admita `@payloadcms/db-postgres` (fijada en la tarea de scaffold), idéntica en `docker compose`, en el servicio de CI y en Railway. |
| R7 | THE SYSTEM SHALL versionar la primera migración (`payload migrate:create`) y generar los tipos (`payload generate:types`) mediante un script. |
| R8 | WHEN se despliega, THE SYSTEM SHALL ejecutar `migrate` en el arranque y SHALL no usar `push` en producción ni en staging. |

### Cuentas, auth y medios (Sensible)
| ID | Requisito |
|---|---|
| R9 | THE SYSTEM SHALL definir la colección `usuarios` con la auth de Payload y un campo `rol` con los valores Editor, Marketing y Administrador. |
| R10 | WHEN un usuario autenticado sin rol Administrador intenta crear una cuenta, cambiar un `rol` o borrar una cuenta, THE SYSTEM SHALL rechazarlo en el servidor (RF-38), también por la API REST. |
| R10b | WHEN un visitante sin sesión hace `GET`, `POST`, `PATCH` o `DELETE` sobre `/api/usuarios`, THE SYSTEM SHALL rechazarlo y SHALL no listar ningún correo (art. 13). |
| R10c | THE SYSTEM SHALL crear el primer Administrador en el despliegue (en el arranque, después de `migrate`) con credenciales de Paperclip Secrets, antes de que staging reciba tráfico, de modo que `/admin/create-first-user` nunca quede abierto. El campo `rol` SHALL ser obligatorio y nunca tomar por defecto Administrador. |
| R11 | WHEN un visitante sin sesión accede a `/admin`, THE SYSTEM SHALL exigir login. |
| R12 | THE SYSTEM SHALL guardar las contraseñas con hash (el de Payload) y SHALL configurar `tokenExpiration: 7200` (2 h) y `maxLoginAttempts: 5` con `lockTime: 600000` (10 min) en `usuarios` (RNF-09). La app SHALL no arrancar si falta `PAYLOAD_SECRET` o `DATABASE_URI` (sin valor por defecto vacío) y SHALL emitir la cookie de sesión con `secure: true` en staging y producción. |
| R13 | WHEN una cuenta acumula 5 intentos fallidos de login, THE SYSTEM SHALL bloquearla durante 10 minutos y SHALL rechazar incluso la contraseña correcta mientras dure el bloqueo. |
| R14 | WHEN transcurren 2 horas desde la emisión del token sin renovarlo, THE SYSTEM SHALL rechazar la sesión y pedir login. |
| R15 | THE SYSTEM SHALL definir la colección `medios` con `@payloadcms/storage-s3` hacia un bucket propio de Cloudflare R2, aceptando solo `image/jpeg`, `image/png`, `image/webp` e `image/avif` (sin SVG), con lectura pública, escritura solo con sesión y un campo `alt` obligatorio (del que depende R18). |
| R15b | IF en staging o producción faltan las variables de R2, THEN THE SYSTEM SHALL no arrancar, sin pasar en silencio al disco local (en Railway no persiste). En local y CI SHALL usar el almacenamiento local de Payload con `storage-s3` desactivado. |

### Caché de datos
| ID | Requisito |
|---|---|
| R16 | THE SYSTEM SHALL leer PostgreSQL con la Local API en cada solicitud pública, con `overrideAccess: false` y sin usuario (RNF-10), sin caché de datos, sin ISR y sin full route cache. La ruta `/` SHALL mostrar el documento de `medios` más reciente por `createdAt` (su imagen y su `alt`) y, si no hay ninguno, un texto fijo de «sin medios». |
| R17 | THE SYSTEM SHALL no importar `next/cache`, no usar la directiva `"use cache"`, no exportar `revalidate` en `src/**` y no activar `cacheComponents` en `next.config.ts`. |
| R18 | WHEN se publica un cambio por la REST del CMS con sesión y llega el 2xx, THE SYSTEM SHALL mostrar el valor nuevo en la primera solicitud pública iniciada después (G3). |
| R19 | THE SYSTEM SHALL exigir un ADR para habilitar cualquier caché de datos. |

### Calidad y sensores
| ID | Requisito |
|---|---|
| R20 | THE SYSTEM SHALL tener un ADR-002 que registre y justifique ESLint (`eslint-config-next`), Prettier (si se usa), Vitest, Playwright, jscpd, knip, dependency-cruiser, Lighthouse CI y gitleaks, con un número exacto para cada umbral (art. 23): jscpd (porcentaje máximo de duplicación), Lighthouse móvil ≥ 80, LCP ≤ 2,5 s y CLS ≤ 0,1 en laboratorio, INP ≤ 200 ms (p75 de campo; se mide en la spec 009) y cobertura si se adopta. Los umbrales de RNF-01 valen para home, listado y detalle. |
| R21 | THE SYSTEM SHALL tener un `.dependency-cruiser.cjs` traducido fila a fila de la tabla de capas de `arquitectura.md`: una regla `forbidden` por fila con `from.path`, `from.pathNot` de tests y `to.pathNot` con la lista exhaustiva de permitidos, más todas las reglas globales de `arquitectura.md`, una regla por cada una: sin ciclos; sin módulos sin resolver ni paquetes no declarados; sin `devDependencies` fuera de tests; nadie fuera de los tests importa un test (`*.test.ts(x)`, `tests/`); `pg`/`drizzle-orm`/`@payloadcms/drizzle` solo en `src/migrations/`; fuera de `scripts/`, nadie importa `scripts/`; `sin-cache-de-datos` (nadie importa `next/cache`); y nadie importa de `bloqueosweb` (art. 20). |
| R22 | THE SYSTEM SHALL analizar con `depcruise src scripts tests`, con `tsPreCompilationDeps: false` y el alias `@payload-config` resuelto por tsconfig, y ESLint SHALL exigir `import type`. |
| R23 | WHEN un archivo de `src/**` declara `"use client"` y no es `*.client.{ts,tsx}`, `error.tsx`, `global-error.tsx` ni está en `src/app/(payload)/`, THE SYSTEM SHALL rechazarlo con ESLint `no-restricted-syntax` (`Program > ExpressionStatement[directive='use client']`). |
| R24 | WHEN un archivo `*.client.{ts,tsx}`, `error.tsx` o `global-error.tsx` alcanza (`to.reachable: true`) `src/payload.config.ts`, `collections`, `globals`, `access`, `migrations`, `payload`, `@payloadcms/db-postgres`, `@payloadcms/storage-s3` o `@payloadcms/next`, THE SYSTEM SHALL rechazarlo con la regla `cliente-sin-servidor`. |
| R25 | WHEN un archivo de `src/**` contiene la directiva `"use cache"` (al inicio del archivo o dentro de una función), el export `revalidate`, o `fetch` con `cache: 'force-cache'` o `next: { revalidate }`, THE SYSTEM SHALL rechazarlo con ESLint `no-restricted-syntax`. |
| R26 | THE SYSTEM SHALL probar cada sensor con fixtures guardados como texto en `tests/sensores/`, que el test escribe en un árbol temporal en su ruta real de `src/`, ignorado por git y excluido de los sensores, ejecutando el mismo `.dependency-cruiser.cjs` y `eslint.config.mjs` y comprobando el nombre de la regla que rechaza cada caso. Habrá un fixture por cada regla de fila de la tabla de capas y uno por cada regla global. |

### CI, despliegue y operación
| ID | Requisito |
|---|---|
| R27 | WHEN hay un push o PR hacia `develop`, THE SYSTEM SHALL ejecutar en CI, en este orden: `npm ci`, `check` (lint, tipos, jscpd, knip, dependency-cruiser), tests unitarios y de integración con servicio PostgreSQL, `build` y e2e (Playwright). El escaneo de secretos (gitleaks) SHALL ejecutarse al principio o en paralelo, para que un secreto falle rápido. |
| R28 | THE SYSTEM SHALL ejecutar Lighthouse CI sobre `/` en modo informativo (no bloqueante) hasta la spec 009. |
| R29 | IF un sensor de R27 falla, THEN THE SYSTEM SHALL bloquear la integración en `develop` (protección con CI verde obligatoria, configurada por DevOps). |
| R30 | THE SYSTEM SHALL tener entornos Railway `staging` (desplegado desde `develop`) y `production` (sin desplegar hasta la spec 010), con PostgreSQL gestionado por entorno, `output: 'standalone'` y un proyecto nuevo que no toca el servicio ni la base de `bloqueosweb`. |
| R31 | WHEN se consulta `/api/health`, THE SYSTEM SHALL comprobar la base de datos y responder 200 si responde y 503 si no, sin detalles internos en el cuerpo (mensaje del driver, host, pila) y sin cachear la respuesta. |
| R32 | THE SYSTEM SHALL tener, en staging (producción: spec 010), una copia de seguridad diaria de PostgreSQL con retención de 7 días y una restauración de prueba documentada en `docs/` con fecha y resultado (RNF-13). La copia de R2 se documenta y prueba en la spec 010. |
| R33 | THE SYSTEM SHALL tener `stop_check_command` (`npm run check:fast`) en `.claude/hooks/hooks.config.json` y la sección Comandos de `AGENTS.md` rellena solo con comandos verificados. |

### Comandos (scripts de `package.json`)
| AGENTS.md | Comando | Qué hace |
|---|---|---|
| Instalar | `npm ci` | Instala desde el lockfile |
| Desarrollo | `docker compose up -d db && npm run dev` | PostgreSQL local + Next/Payload en `:3000` |
| Tests rápidos (por zona) | `npm run test -- <ruta>` | Vitest solo sobre la ruta indicada |
| Sensores rápidos | `npm run check:fast` | `lint` + `typecheck` + `jscpd` + `knip` + `depcruise`, sin tests ni build; < 60 s y sin base de datos |
| CI completa | `npm run ci` | `check:fast` + `test` + `build` + `test:e2e` |
| Build | `npm run build` | `payload generate:types` comprobado + `next build` |

Otros scripts: `typecheck` (`tsc --noEmit`), `depcruise` (`depcruise src scripts tests`), `payload` (CLI), `migrate:create`, `test:e2e`. El hook de parada tiene timeout de 600 s; `check:fast` debe tardar mucho menos.

## Criterios de aceptación
| Req. | Criterio (observable) |
|---|---|
| R1 | `npm ls` termina sin errores de dependencias par y `package.json` muestra las versiones o rangos de R1. |
| R1–R3 | Dado el repo, cuando se inspecciona `package.json`, entonces no aparecen `@payloadcms/richtext-lexical` ni `@payloadcms/db-mongodb`, el import map no menciona Lexical y `GET /api/graphql` devuelve 404. |
| R4 | Las tres líneas con la misma versión de Node (`.nvmrc`, log de CI, log de build de Railway) se pegan en el handoff. |
| R6b | Las tres versiones de PostgreSQL (`docker compose`, servicio de CI, Railway) se pegan en el handoff y coinciden en la versión mayor. |
| R5 | `npm run build` termina y `GET /` responde 200; `.env.example` lista todas las variables que lee el código y gitleaks pasa. |
| R6–R8 | Dado un clon limpio con Docker, `docker compose up -d db && npm run dev` sirve `:3000`; la migración inicial está versionada; el arranque de staging ejecuta `migrate` y el log no muestra `push`. |
| R9–R10 | Dado un usuario Editor o Marketing con sesión, cuando hace `POST /api/usuarios`, `PATCH` del `rol` o `DELETE` de una cuenta, entonces la API devuelve 403 y los datos no cambian. Un Administrador sí puede. Test de autorización en servidor. |
| R10b | Test de autorización: sin sesión, `GET`, `POST`, `PATCH` y `DELETE` sobre `/api/usuarios` se rechazan y la respuesta no contiene ningún correo. |
| R10c | Desde el primer despliegue, `GET /api/usuarios/init` en staging devuelve `initialized: true`; una cuenta creada sin `rol` es rechazada. |
| R11 | `GET /admin` sin sesión muestra el login (e2e de humo). |
| R12 | En la BD el campo de contraseña no contiene el texto original (solo hash y sal); la configuración de `usuarios` contiene `tokenExpiration: 7200`, `maxLoginAttempts: 5` y `lockTime: 600000`. Con `PAYLOAD_SECRET` o `DATABASE_URI` ausentes, el arranque falla; en staging la cookie de sesión lleva `Secure`. El Code Reviewer lo revisa en su bloque de seguridad. |
| R13 | Dado un usuario, cuando falla el login 5 veces seguidas, entonces el 6.º intento con la contraseña correcta es rechazado; pasados los 10 minutos (el test ajusta `lockTime` por configuración de test, sin simular el reloj) el login correcto funciona. |
| R14 | Dado un token emitido con `tokenExpiration` reducido en el entorno de test, cuando pasa ese plazo, entonces `GET /api/usuarios/me` devuelve usuario nulo. El valor de producción (7200) se comprueba en la configuración. |
| R15 | Subir un PNG a `medios` en staging deja el objeto en el bucket R2 y devuelve su URL; subir un SVG o sin `alt` es rechazado; sin sesión, la escritura es rechazada y la lectura es pública. En local y CI el test usa el almacenamiento local. |
| R15b | Con las variables de R2 ausentes y entorno staging o producción, el arranque falla; en local y CI no. |
| R16–R17 | La salida de `next build` marca `/` como dinámica (`ƒ`); `/` sin medios muestra el texto fijo y, con varios, el más reciente; las lecturas usan `overrideAccess: false`. Un test de contrato comprueba que, tras publicar por REST, la primera respuesta pública devuelve el valor nuevo; `grep` y revisión del diff confirman que no hay `next/cache`, `"use cache"`, export `revalidate` ni `cacheComponents` en `next.config.ts`. |
| R18 | **G3 en e2e de CI y contra el build de producción** (`next build` + `next start`, nunca `next dev`): con `/` servida una vez, se actualiza por REST con sesión el `alt` del documento de `medios` que muestra `/`; la primera petición a `/` iniciada tras el 2xx muestra el `alt` nuevo. Así también se detecta una ruta prerenderizada en `next build`. No depende de esperas por tiempo. |
| R19 | `arquitectura.md` (y el ADR-001) indican que habilitar caché requiere ADR; ese ADR deberá repetir la prueba de R18 con entrada caliente y esperar de forma determinista a que termine el intento de escritura del valor anterior. |
| R20 | `docs/arquitectura/adr/ADR-002-*.md` existe, cada herramienta lleva justificación y cada umbral (incluido INP y el de jscpd) un número, para home, listado y detalle. |
| R21–R22 | Un fixture por cada regla de fila de la tabla de capas (p. ej. `src/components` → `payload`) y uno por cada regla global (ciclo, paquete no declarado, `devDependency` fuera de tests, `pg`/`drizzle-orm` fuera de `src/migrations/`, importación de `scripts/`, importación de un test, importación de `bloqueosweb`) falla en CI con el nombre de su regla. |
| R23–R24 | Los fixtures fallan en su regla: (a) `src/app/(frontend)/x.client.tsx` importa `@payload-config` → `cliente-sin-servidor`; (b) ese archivo importa un módulo de servidor de su carpeta que importa `payload` → `cliente-sin-servidor`; (c) un archivo de `src/app/(frontend)/` sin sufijo `.client` declara `"use client"` → `no-restricted-syntax`; (d) `error.tsx` importa `payload` → `cliente-sin-servidor`. |
| R25 | Fixtures: un archivo con `import … from "next/cache"` falla por `sin-cache-de-datos`; uno con `"use cache"` al inicio y otro con `"use cache"` dentro de una función fallan por `no-restricted-syntax`; uno con `fetch` y `cache: 'force-cache'` o `next: { revalidate }` falla por `no-restricted-syntax`; **uno con `export const revalidate = …` falla por `no-restricted-syntax`**. |
| R26 | Un fixture de control permitido pasa los tres análisis; incluye `import type { … } from 'payload'` en `src/components/`, para probar que `tsPreCompilationDeps: false` descarta los imports de solo tipos. Cada fixture comprueba el nombre de la regla, no solo que falle. Los fixtures no aparecen en `git status` ni en `npm run check:fast`. |
| R27–R29 | Un PR con código duplicado, un export muerto, un error de tipos o un secreto falla en el paso correspondiente; con todo verde, `npm ci && npm run ci` pasa en limpio en CI y en local con PostgreSQL de Docker. Con CI roja, el merge a `develop` está bloqueado. |
| R28 | Lighthouse CI publica el informe de `/` sin fallar el job. |
| R30–R31 | Staging sirve `/` y `/api/health` (200 con BD arriba) desde `develop`; con la BD inaccesible `/api/health` devuelve 503 con un cuerpo sin mensaje del driver, host ni pila, y con cabecera de no caché. Producción no recibe tráfico. |
| R32 | Captura o log de Railway con la programación diaria, la retención de 7 días y la última copia. Documento en `docs/` con la fecha y el resultado de una restauración de prueba de PostgreSQL en una base aparte, con una comprobación de datos tras restaurar. |
| R33 | `npm run check:fast` pasa en limpio en menos de 60 s sin base de datos; `hooks.config.json` y `AGENTS.md` quedan rellenos y cada comando lleva su salida pegada en el handoff. |

## Valores de auth y su justificación (R12–R14)
- **`tokenExpiration: 7200` (2 h).** El CMS lo usan pocas personas, en sesiones de edición de ~1 h con la ficha abierta. 2 h cubre una sesión normal sin forzar login a mitad de una edición y acota el riesgo de un token robado o de un equipo desatendido (RNF-09 exige caducar sesiones). Más largo (p. ej. 24 h) amplía la ventana de uso de un token robado sin beneficio para este volumen. Más corto (p. ej. 15 min) pierde trabajo en formularios largos. Payload renueva el token con la actividad.
- **`maxLoginAttempts: 5` y `lockTime: 600000` (10 min).** Cinco fallos toleran errores humanos normales; el bloqueo de 10 min frena la fuerza bruta (a lo sumo 30 intentos por hora y cuenta) sin dejar a un editor fuera de la cuenta más de 10 min ni exigir intervención del Administrador. Se acepta que un atacante pueda bloquear una cuenta con fallos a propósito; el coste es de 10 min y se prefiere a la fuerza bruta sin límite.
- Si el Code Reviewer o el Board piden otros valores, se cambian aquí antes de aprobar; no cambia la estructura de la spec.

## Comportamiento que no debe cambiar
- ADR-001 y `docs/arquitectura/arquitectura.md`: esta spec no los contradice. Si hace falta cambiarlos, se pide en un comentario del issue.
- La web actual de `bloqueosweb` (servicio, base de datos y dominio): no se toca ni se importa de ella (art. 20). Cada punto tiene test o revisión en el diff.
- Las reglas de `arquitectura.md` (capas, autorización en servidor, sin caché de datos): los sensores las expresan sin relajarlas; cualquier cambio posterior de la tabla de capas actualiza el cruiser en el mismo cambio.
- El historial y las ramas de documentación previas (specs 000, ADR-001, arquitectura): quedan igual.
- Producción: sin despliegue ni tráfico hasta la spec 010.

## Fuera de alcance
- Tokens y componentes de diseño (spec 002).
- Vista previa (RF-39/40, Live Preview y `/preview`): spec 003.
- Modelo de contenido y matriz completa de roles × acciones (spec 003); aquí solo «cuentas y roles = Administrador».
- Contenido real, migración de datos y dominio de producción.
- Pruebas de G1 (límite de tiempo) y G2 (publicación de datos con límite) y de caché caliente: van a las specs de RF-07, RF-18 y RF-23. La prueba de G3 de cada colección y global público la repite la spec 003.
- Lighthouse CI bloqueante, INP en campo (spec 009).
- Copia de seguridad de R2 (spec 010).
- `plan.md` y `tasks.md` (los escribe el Arquitecto).

## Seguridad y datos
Sensible: sí. Toca auth, roles y subida de archivos. Las tareas llevan «Sensible: sí» y el Code Reviewer aplica su bloque de seguridad. Puntos a revisar: R9–R15 (cuentas, hash, caducidad, bloqueo, subida a R2), autorización en servidor por la REST (R10) y que ningún secreto entre en el repo (`.env.example` sin valores, gitleaks en CI). Datos personales: solo correo y contraseña (hash) de las cuentas del CMS.

## Dependencias del Board
El Board las aporta por Paperclip Secrets, nunca en comentarios; no son requisitos abiertos:
- Cuenta de Railway (proyecto nuevo en el mismo workspace de la web actual) y acceso para staging y producción.
- Cloudflare R2: bucket propio y claves de acceso.
- Dominio: solo para staging si se desea uno propio; el de producción es de la spec 010.

## Dudas
Ninguna.
