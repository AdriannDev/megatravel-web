# ADR-003 · Sesiones y hash de contraseñas del CMS

- Estado: **propuesto** (lo aprueba el Board en la revisión de la spec 001b, [MEG-42](/MEG/issues/MEG-42))
- Fecha: 2026-11-28 · Revisar en: spec 008 (gestión de usuarios) o si Node retira `crypto.argon2`

## Decisión
Autenticación propia sobre Node y Postgres, **sin dependencias nuevas**:
- **Hash:** `crypto.argon2` nativo de Node (≥ 24.7), con argon2id, `memory` 19456 KiB, `passes` 2, `parallelism` 1, `tagLength` 32 y un nonce aleatorio de 16 bytes. Se guarda en formato PHC (`$argon2id$v=19$m=…,t=…,p=…$sal$hash`) y se compara con `timingSafeEqual`. Si `crypto.argon2` no existe, la app falla al arrancar.
- **Sesión en BD:** un token aleatorio de 32 bytes va en la cookie `__Host-session` (`HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/`). La tabla `sessions` guarda solo su SHA-256. La sesión caduca a las **8 h**, sin renovación. El logout y la caducidad borran la fila.
- **Límite de intentos:** cada usuario lleva un contador. Tras **5 fallos seguidos**, la cuenta se bloquea **15 min** y se rechaza incluso la contraseña correcta. Un acierto pone el contador a cero. El mensaje de error es siempre el mismo. Con un email desconocido también se calcula un hash, para no delatar por tiempo qué emails existen.
- **Autorización:** un DAL en el servidor (`verifySession()` y `requireRole()`) se llama en cada página, Server Action y Route Handler del CMS. No se usa `proxy`: si se añade, solo redirige de forma optimista.

**Se descarta:**
- Better Auth: trae su propio esquema y su CLI, que compiten con drizzle-kit, y es más de lo que piden 3 roles internos.
- Auth.js (pensado para OAuth), `bcrypt` y `@node-rs/argon2` (dependencias extra; Node ya trae argon2id).
- iron-session o jose (sesión sin estado en la cookie): no se puede revocar una sesión sin una tabla aparte.
- scrypt como algoritmo principal: OWASP lo recomienda solo si no hay argon2id. Queda como plan B (N=2^17, r=8, p=1) si Railway no ofrece Node ≥ 24.7.

## Motivo y trade-offs
- RNF-05 pide 4 cosas, y esto da 1 pieza para cada una:
  - Hash robusto: argon2id con el mínimo de OWASP.
  - Sesiones que caducan: tabla con `expires_at`.
  - Límite de intentos: contador por usuario.
  - Permisos en el servidor: el DAL.
- Son unas 200 líneas propias, auditables por el Auditor, a cambio de 0 dependencias.
- **Coste:** el bloqueo por cuenta permite que alguien bloquee a un usuario durante 15 min si conoce su email. Con 3 roles internos se acepta. No hay límite por IP porque necesitaría confiar en las cabeceras del proxy de Railway (no confirmado).
- **Coste:** 1 consulta a la BD por cada petición del CMS; con 1 instancia y pocos usuarios es despreciable. Contra CSRF: Next compara `Origin` y `Host` en las Server Actions, y la cookie usa `SameSite=Lax`. Un Route Handler que modifique datos debe comprobar `Origin`.

## Impacto por agente
- **Backend:** escribe `src/lib/auth/*` y las tablas `users` y `sessions`. El Auditor revisa cada tarea.
- **Frontend:** usa las Server Actions de login y logout. Nunca lee la cookie ni la BD.
- **DevOps:** fija Node ≥ 24.7 en Railway y en la CI, y documenta que no hay secreto de sesión que rotar. **Auditor:** revisa RNF-05 y los art. 12 y 13.

## Cómo revertir
El hash y la sesión están detrás de 2 módulos (`password.ts` y `session.ts`). Cambiar a otra librería toca solo esos módulos y 1 migración. Los hashes PHC antiguos se pueden verificar y rehacer en el siguiente login.

## Fuentes (consultadas el 2026-11-28)
- Node 24 `crypto.argon2` (`added: v24.7.0`): https://nodejs.org/docs/latest-v24.x/api/crypto.md
- OWASP Password Storage: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Next.js Authentication (DAL, cookies y proxy): https://nextjs.org/docs/app/guides/authentication
