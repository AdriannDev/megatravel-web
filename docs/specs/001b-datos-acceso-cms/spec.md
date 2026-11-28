# Spec 001b · Datos y acceso al CMS

Estado: borrador ([MEG-42](/MEG/issues/MEG-42))
Autor: Arquitecto · Requisitos que cubre: RF-24, RF-28, RNF-05, RNF-16 (BD) · ADR: ADR-001 y ADR-002 (aceptados), **ADR-003 (propuesto: sesiones y hash)**

## 1. Problema y objetivo
La 001 dejó una app sin base de datos, sin login y sin despliegue. `/admin` es un esqueleto abierto a cualquiera. Ninguna spec de contenido (002 en adelante) puede guardar datos ni limitar quién los cambia.

Al terminar esta spec:
- Hay un Postgres en Railway con un esquema versionado por migraciones.
- El CMS solo se abre con email y contraseña. Cada acción se comprueba en el servidor según la sesión y el rol.
- Cada push a `develop` se despliega en una URL de preview con HTTPS.
- La BD tiene un backup diario cuya restauración se ha probado.

## 2. Requisitos
| ID | Requisito (EARS) | Criterio de aceptación (observable) |
|---|---|---|
| R1 | THE SYSTEM SHALL definir el esquema con Drizzle en `src/db/schema.ts` y versionar en `drizzle/` las migraciones SQL que genera drizzle-kit. | En un Postgres 18 vacío, `npm run db:migrate` → exit 0 y crea `users` y `sessions`. `npx drizzle-kit check` → exit 0. Después, `npm run db:generate` no crea archivos (`git status` limpio) |
| R2 | THE SYSTEM SHALL guardar solo estos datos:<br>• por usuario: email único en minúsculas, hash PHC, rol (`marketing`, `producto` o `administrador`), fallos seguidos, `locked_until` y fechas de alta y cambio;<br>• por sesión: el SHA-256 del token, `user_id`, `expires_at` y `created_at` (constitución art. 13). | Un test inserta y lee 1 usuario y 1 sesión. Ninguna columna guarda la contraseña ni el token en claro. Insertar un email repetido (en cualquier combinación de mayúsculas) falla |
| R3 | WHEN se guarda una contraseña, THE SYSTEM SHALL calcular un hash argon2id con los parámetros de ADR-003 y una sal aleatoria. | Test unitario:<br>• el hash empieza por `$argon2id$v=19$m=19456,t=2,p=1$`;<br>• 2 hashes de la misma contraseña son distintos;<br>• `verify` devuelve `true` con la contraseña correcta y `false` con otra |
| R4 | WHEN un usuario envía un email y una contraseña correctos de una cuenta no bloqueada, THE SYSTEM SHALL crear una sesión de 8 h, poner la cookie `__Host-session` (`HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/`) y redirigir a `/admin`. | Test de la Server Action `login`: hay 1 fila en `sessions` cuyo id es distinto del token de la cookie, y la cookie lleva esos atributos. En la preview, `curl -i` del login muestra la cabecera `Set-Cookie` con los atributos |
| R5 | IF el email no existe o la contraseña es incorrecta, THEN THE SYSTEM SHALL responder con el mismo mensaje genérico, no crear ninguna sesión y sumar 1 a los fallos del usuario si existe. | Test: email desconocido y contraseña errónea devuelven exactamente el mismo mensaje. No se crea ninguna sesión. Los fallos del usuario existente suben en 1 |
| R6 | IF una cuenta acumula 5 fallos seguidos, THEN THE SYSTEM SHALL rechazar cualquier login de esa cuenta durante 15 min, incluso con la contraseña correcta, y poner los fallos a 0 en el primer acierto posterior. | Test con reloj simulado:<br>• el 6.º intento, ya con la contraseña correcta, se rechaza con el mensaje genérico;<br>• pasados 15 min y 1 s, se acepta y los fallos vuelven a 0 |
| R7 | WHILE no hay una sesión válida (sin cookie, con un token desconocido o con la sesión caducada), WHEN se pide una página `/admin/**` distinta de `/admin/login`, THE SYSTEM SHALL redirigir a `/admin/login`; WHEN se invoca una Server Action o un Route Handler del CMS, THE SYSTEM SHALL rechazarlo sin modificar datos. | Tests de `verifySession`: cada uno de los 3 casos redirige, y la sesión caducada borra su fila. El test guardián (§6) falla si una página o acción de `src/app/admin/**` no llama a `verifySession` o `requireRole`. En la preview, `curl -i /admin` sin cookie → 307 a `/admin/login` |
| R8 | IF el rol de la sesión no está entre los permitidos por una acción, THEN THE SYSTEM SHALL rechazarla en el servidor sin modificar datos (RF-28). | Test de `requireRole` con una acción de prueba que escribe: con un rol no permitido se lanza `forbidden` y el número de filas es el mismo antes y después. Con un rol permitido, la acción escribe |
| R9 | WHEN un usuario cierra la sesión, THE SYSTEM SHALL borrar la fila de la sesión y la cookie. | Test: después del `logout`, usar el mismo token lleva a `/admin/login` y la fila ya no existe |
| R10 | THE SYSTEM SHALL no escribir en logs ni en errores devueltos contraseñas, tokens, hashes ni emails. | Un test espía `console.*` durante un login correcto, uno fallido y uno bloqueado: ninguno de esos valores aparece en la salida |
| R11 | THE SYSTEM SHALL ofrecer `npm run admin:create -- <email>`, que crea 1 Administrador con una contraseña aleatoria de 20 caracteres o más, la muestra una sola vez por la terminal y falla sin cambiar nada si ya existe un Administrador. | Test: la primera ejecución crea 1 fila con el rol `administrador`. La segunda → exit ≠ 0, y sigue habiendo 1 fila. La contraseña no queda en ningún archivo |
| R12 | WHEN se hace push a `develop`, THE SYSTEM SHALL desplegar en el entorno `develop` de Railway, aplicar las migraciones en el pre-deploy antes de arrancar y servir por HTTPS en la URL de preview de `AGENTS.md`. | Enlace al deploy en Railway. `curl -i https://<preview>/api/health` → 200 (consulta `select 1`). Con una migración rota provocada, el deploy falla y la versión anterior sigue respondiendo (evidencia en el handoff) |
| R13 | IF falta `DATABASE_URL` o `crypto.argon2` no existe, THEN THE SYSTEM SHALL fallar al arrancar con un mensaje que nombra lo que falta, sin mostrar ningún valor. | Test de `src/instrumentation.ts` para los 2 casos. Cada `process.env.X` del código aparece en `.env.example` (comprobado con `grep`) |
| R14 | THE SYSTEM SHALL hacer un backup diario de la BD de `develop` (y de la de producción cuando exista) y tener probada su restauración (RNF-16 BD). | El runbook tiene el procedimiento y la evidencia de 1 restauración en una BD aparte:<br>• fecha;<br>• duración;<br>• el número de filas de `users` y `sessions` coincide con el origen |

## 3. No debe cambiar
- `/` responde 200, sigue siendo pública y nunca pone cookies, porque el sitio público no tiene cuentas (RF-24). El test `src/app/page.test.tsx` sigue en verde, y `curl -i /` en la preview no muestra `Set-Cookie`.
- `/admin` y `/admin/login` llevan `noindex`. El test de `/admin` se adapta y se añade el de `/admin/login`.
- `npm run check` y el job `ci` siguen en verde, con los mismos umbrales que en la 001 (jscpd al 3 %, lint con 0 avisos y knip sin excepciones nuevas). `git diff` de `eslint.config.mjs` y del script `dup` vacío.
- ADR-001, ADR-002, `docs/producto/*`, la spec 001 y `main`: `git diff develop -- <rutas>` vacío.

## 4. Fuera de alcance
| Fuera | Va en |
|---|---|
| Gestión de usuarios desde la UI, cambio y recuperación de contraseña (RF-29) | 008 |
| Permisos concretos de cada rol sobre el contenido (RF-25 a RF-27) | 002 (usa `requireRole` de esta spec) |
| Diseño visual del CMS y del login | 002 y 008 (los tokens llegan en 003) |
| Backups de medios (RNF-16 medios) | 005 |
| Deploy de producción y dominio propio | Lanzamiento (Board) |
| Sensor de capas (dependency-cruiser, ADR-002) | 002. Aquí basta el test guardián (§6), sin dependencias |
| E2E con Playwright | 003 (ADR-002) |
| Doble factor y límite por IP | No pedidos en RNF-05 (ADR-003) |

## 5. Inventario de reutilización
| Necesidad | Consulta graphify | Existe | Ruta | Decisión |
|---|---|---|---|---|
| Esquema y cliente de BD | `database schema drizzle` | no | — | Se crean en `src/db/` |
| Sesión y login | `authentication session login` | no (solo un hook de agentes) | — | Se crean en `src/lib/auth/` (ADR-003) |
| Página del CMS | `admin page layout` | sí | `src/app/admin/page.tsx`, `src/app/layout.tsx` | Se reutiliza: `/admin` añade `verifySession`, y `noindex` pasa a `src/app/admin/layout.tsx` |
| Variables de entorno | `environment variables env example` | no (solo la sección vacía del runbook) | `docs/ops/runbook.md` | Se crea `.env.example` y se rellena el runbook |

## 6. Diseño
**Prerrequisitos (sin ellos no arranca la ola indicada):**

| ID | Qué | Dueño | Ola |
|---|---|---|---|
| P1 | Proyecto de Railway con el repo de GitHub conectado, e invitación a DevOps (rol con permiso de deploy) | Board | 2 |
| P2 | **Plan de Railway y método de backup.** Pro incluye backups de volumen programados (según el personal de Railway en su foro, no confirmado en la doc oficial). Con Hobby: `pg_dump` diario a R2 con el cron de Railway, como prevé ADR-001 | Board | 4 |
| P3 | Solo si P2 es Hobby: bucket de R2 para backups, separado del de medios, con claves solo de escritura. Se cargan como variables de Railway y no pasan por el issue | Board y DevOps | 4 |
| P4 | Email del primer Administrador. DevOps le entrega la contraseña de R11 por un canal acordado fuera de Paperclip y de GitHub | Board | 4 |

**Datos:**
- `users`: `id` uuid, `email` text único en minúsculas, `password_hash`, `role` (enum `marketing`, `producto`, `administrador`), `failed_attempts` int, `locked_until` timestamptz nulo, `created_at` y `updated_at`.
- `sessions`: `id` (el SHA-256 en hex del token, clave primaria), `user_id` (FK con borrado en cascada), `expires_at` y `created_at`.
- Las fechas son `timestamptz` en UTC.

**Módulos:**
- `src/db/client.ts`: 1 `Pool` de `pg` y la instancia de Drizzle.
- `src/lib/auth/password.ts`: `hashPassword` y `verifyPassword`. Solo importa `node:crypto`.
- `src/lib/auth/session.ts`: crear, validar y borrar sesiones.
- `src/lib/auth/dal.ts`: `verifySession()` (devuelve `{ userId, role }` o redirige) y `requireRole(...roles)` (lanza `forbidden`). Los marca `server-only` por convención: no se importan desde `"use client"`.
- `src/app/admin/login/actions.ts`: las Server Actions `login` y `logout`. Validan la entrada en el servidor (art. 12).
- Toda consulta pasa por Drizzle, con parámetros y nunca con SQL concatenado.

**Test guardián:** `src/app/admin/guard.test.ts` recorre `src/app/admin/**/page.tsx` y los archivos `"use server"`, salvo `login/`. Falla si alguno no llama a `verifySession(` o `requireRole(`. Sustituye al sensor de capas hasta la 002.

**Tests con BD:** usan `TEST_DATABASE_URL` y aplican las migraciones antes de empezar. En la CI, un *service container* `postgres:18`. En local, cada agente necesita un Postgres 18. Sin `TEST_DATABASE_URL`, los tests fallan con un mensaje claro y no se saltan. DevOps lo documenta en «Gotchas».

**Entornos (Railway):**
- `develop` despliega la rama `develop` con su propio Postgres. Su URL `*.up.railway.app` va a `AGENTS.md`.
- `production` lo crea DevOps con su Postgres y sus variables, sin despliegue automático hasta el lanzamiento.
- El *pre-deploy command* (Settings → Deploy) ejecuta `npm run db:migrate`. Si falla, el deploy no avanza.
- Se configura desde el panel y no con `railway.json`, porque Railway da Config as Code por obsoleto.
- `DATABASE_URL` es una variable de referencia al Postgres del mismo entorno. No hay secreto de sesión.

**Mapa de código:** hay filas nuevas para «Acceso a datos» (`src/db/`, `drizzle/`) y «Autenticación» (`src/lib/auth/`).

## 7. Complejidad justificada
| Excepción | Motivo | Alternativa descartada | ADR |
|---|---|---|---|
| Autenticación propia (≈ 200 líneas) en lugar de una librería | Cubre RNF-05 sin dependencias, y Node 24 ya trae argon2id | Better Auth, Auth.js, iron-session y bcrypt | ADR-003 |
| Postgres como *service container* en la CI | Probar R1 y de R4 a R9 contra un Postgres real, sin dependencias | PGlite: es una dependencia nueva y no es el mismo motor | — (no añade dependencias) |

## 8. API (esbozo)
| Método y ruta | Propósito | Permisos | Nuevo/cambia |
|---|---|---|---|
| `GET /admin/login` | Formulario de login. Si ya hay sesión, redirige a `/admin` | público, `noindex` | nuevo |
| Server Action `login(prevState, formData)` | R4 a R6 | público | nuevo |
| Server Action `logout()` | R9 | sesión válida | nuevo |
| `GET /admin` | Portada del CMS | sesión válida, cualquier rol | cambia |
| `GET /api/health` | Healthcheck de Railway con `select 1`: devuelve 200 o 503, sin detalles | público | nuevo |

Backend entrega el contrato exacto (tipos del estado del formulario y mensajes) en `api.md` (T4).

## 9. UX
N/A. El login es un formulario semántico con `label`s, `autocomplete="username"` y `autocomplete="current-password"`, y el error en `role="alert"`. No lleva diseño: los tokens llegan en 003 y la UI del CMS en 002 y 008.

## 10. Tareas
Las tareas de Backend las revisa el Auditor. Las de Frontend y DevOps, el Arquitecto. El lockfile y los archivos generados por drizzle-kit (`drizzle/meta/*`) no cuentan en las 400 líneas, como en la 001.

| ID | Tarea | Dueño | Tipo | Criterios | Archivos previstos | Verificación | Ola | Sensible |
|---|---|---|---|---|---|---|---|---|
| T1 | Instala `drizzle-orm`, `drizzle-kit` y `pg` (ADR-001), y añade:<br>• los scripts `db:generate` y `db:migrate`;<br>• el cliente de BD;<br>• `/api/health`;<br>• `.env.example`;<br>• Postgres 18 en la CI. | DevOps | tarea | R12 (health), R13 (`.env.example`) | `package.json`, `package-lock.json`, `drizzle.config.ts`, `src/db/client.ts`, `src/app/api/health/route.ts`, `src/app/api/health/route.test.ts`, `.env.example`, `.github/workflows/ci.yml` (8) | `npm ci && npm run check && npm run build` → exit 0, y el job `ci` en verde con el servicio Postgres. knip pasa sin `ignoreDependencies`. Si hace falta `@types/pg`, se para y se pide un ADR | 1 | no |
| T2 | Esquema `users` y `sessions`, primera migración y módulo de contraseñas | Backend | tarea | R1, R2, R3 | `src/db/schema.ts`, `src/db/schema.test.ts`, `drizzle/0000_*.sql`, `drizzle/meta/_journal.json`, `drizzle/meta/0000_snapshot.json`, `src/lib/auth/password.ts`, `src/lib/auth/password.test.ts` (7) | `npm run db:migrate` en un Postgres vacío, `npx drizzle-kit check` y `npm run check` → exit 0. `db:generate` deja `git status` limpio | 2 | sí |
| T3 | Entornos `develop` y `production` en Railway, deploy de `develop` con pre-deploy de migraciones, comprobación al arrancar, y URL de preview en `AGENTS.md` | DevOps | tarea | R12, R13 | `src/instrumentation.ts`, `src/instrumentation.test.ts`, `AGENTS.md` (solo la URL de preview, «Comandos» y «Gotchas»), `docs/ops/runbook.md` (4) | Enlace al deploy. `curl -i <preview>/api/health` → 200. Migración rota provocada → el deploy anterior sigue sirviendo. Test de R13. La versión de Node en el log de Railway es ≥ 24.7. Requiere P1 | 2 | sí |
| T4 | Sesiones, DAL, límite de intentos, Server Actions `login` y `logout`, y contrato `api.md` | Backend | tarea | R4 a R10 | `src/lib/auth/session.ts`, `src/lib/auth/session.test.ts`, `src/lib/auth/dal.ts`, `src/lib/auth/dal.test.ts`, `src/app/admin/login/actions.ts`, `src/app/admin/login/actions.test.ts`, `docs/specs/001b-datos-acceso-cms/api.md` (7) | `npm run check` → exit 0, con los tests de R4 a R10 contra el Postgres de la CI. Fallo provocado de R6 (umbral a 6) en el handoff | 3 | sí |
| T5 | Script `admin:create` para el primer Administrador | Backend | tarea | R11 | `scripts/admin-create.ts`, `scripts/admin-create.test.ts`, `package.json` (solo `scripts`), `tsconfig.json` (solo si Node lo necesita para importar `.ts`) (4) | `npm run admin:create -- a@b.test` 2 veces contra un Postgres de prueba: exit 0 y después exit ≠ 0, con 1 fila. `npm run check` → exit 0 | 3 | sí |
| T6 | Página `/admin/login`, logout en `/admin`, `noindex` en el layout del CMS y test guardián | Frontend | tarea | R7 (guardián y redirección), R9 (botón), §3 | `src/app/admin/layout.tsx`, `src/app/admin/page.tsx`, `src/app/admin/page.test.tsx`, `src/app/admin/login/page.tsx`, `src/app/admin/login/login-form.tsx`, `src/app/admin/login/page.test.tsx`, `src/app/admin/guard.test.ts` (7) | `npm run check` y `npm run build` → exit 0. Con una página de prueba sin `verifySession`, el guardián falla (en el handoff). En la preview, `curl -i /admin` → 307 | 4 | sí |
| T7 | Backups de la BD y restauración probada. DevOps crea en `develop` el primer Administrador (P4) | DevOps | tarea | R14 | `docs/ops/runbook.md` y, solo con Hobby, `ops/backup/backup.sh` y `ops/backup/Dockerfile` (1 a 3) | Evidencia del R14 en el runbook. Captura o log del backup programado. Requiere P2, P3 y P4 | 4 | sí |
| T8 | Mapa de código: filas «Acceso a datos» y «Autenticación» | Arquitecto | tarea | §6 «Mapa de código» | `docs/arquitectura/mapa-de-codigo.md` (1) | Las filas apuntan a archivos que existen | 4 | no |

**Orden:**
1. Ola 1: T1.
2. Ola 2: T2 y T3, que no comparten archivos.
3. Ola 3: T4 y T5, que dependen de T2.
4. Ola 4: T6, que depende de `api.md` de T4; T7, que depende de T3 y T5; y T8.

**Gotchas:**
- Si drizzle-kit queda en `devDependencies` y Railway las poda antes del pre-deploy, `db:migrate` falla (no confirmado). DevOps lo comprueba en T3. Si pasa, mueve drizzle-kit a `dependencies`, sin dependencias nuevas.
- El script de T5 se ejecuta con Node 24 (*type stripping*). Los módulos que importa (`password.ts`, `client.ts` y `schema.ts`) usan solo imports relativos con extensión `.ts`, nunca el alias `@/`.

## Fuentes (consultadas el 2026-11-28)
- Railway, backups: https://docs.railway.com/reference/backups. El plan necesario no está confirmado en la doc oficial. Según el personal de Railway en el foro, los backups son solo de Pro: https://station.railway.com/questions/pro-plan-gb-of-shared-disk-automatic-ce34c794
- Railway, entornos: https://docs.railway.com/reference/environments · precios: https://railway.com/pricing
- Railway, pre-deploy y Config as Code obsoleto: https://docs.railway.com/config-as-code/reference · https://docs.railway.com/guides/nextjs
- Knip, plugin de Drizzle (el `schema` cuenta como entrada): https://github.com/webpro-nl/knip/tree/main/packages/knip/src/plugins/drizzle
- Las fuentes de autenticación están en ADR-003.
