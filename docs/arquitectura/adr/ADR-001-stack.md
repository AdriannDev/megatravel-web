# ADR-001 · Stack del proyecto

- Estado: **aceptado**
- Fecha: 2026-11-27
- Issue: MEG-27
- Aprobación del Board:
  - Tarjeta «Stack del proyecto» (`ask_user_questions` `ea8a0334-bc9b-488d-a9b4-80665d4d143a`, respondida el 2026-11-27): opción ① en las 4 capas.
  - Tarjeta «Aprobar stack» (`request_confirmation` `a4947479-03b8-4329-95bf-7bfc0ff33b26`, aceptada el 2026-11-27).
- Evaluación completa con fuentes: documento `stack` de MEG-27 (rev 1).

## Contexto
RNF-01 fija React, Next.js, Tailwind y TypeScript, y un CMS propio sin CMS de terceros. RNF-02 pide el coste mínimo sobre la infraestructura existente (Railway, R2 y dominio propio). El volumen de diseño es de 300 programas × 20 salidas (RNF-03), con datos tipados (RNF-04) y propagación ≤ 1 min (RNF-07).

## Decisión
| Capa | Elección |
|---|---|
| Frontend | **1 app Next.js 16 (App Router) + React + Tailwind CSS v4 + TypeScript**. Web pública en `/` y CMS en `/admin` en la misma app |
| Backend | **Integrado en Next.js**: Server Components, Server Actions y Route Handlers. Acceso a datos con **Drizzle ORM** (línea estable, no la v1.0 beta) y migraciones con **drizzle-kit** |
| BD | **PostgreSQL en Railway** (18.x o superior), en la misma red privada que la app. Búsqueda de RF-02 con FTS nativo y `unaccent` |
| Hosting | **Railway** (1 servicio `next start` + Postgres) · **Cloudflare R2** para medios por la API S3 · **dominio propio** |

Dependencias que aprueba este ADR: `next`, `react`, `react-dom`, `typescript`, `tailwindcss`, `drizzle-orm`, `drizzle-kit`, `pg` (driver) y `@aws-sdk/client-s3` (R2). Cualquier otra, incluidas las herramientas de CI de la spec 001, necesita su propio ADR.

## Alternativas descartadas
- **Monorepo con 2 apps Next.js / CMS como SPA con Vite:** duplican el despliegue sin un requisito que lo pida.
- **Prisma:** válido. Drizzle se elige por su esquema en TS sin generador aparte.
- **API aparte (Hono, NestJS):** añaden un servicio y una capa sin requisito que lo pida.
- **Neon, Supabase o SQLite/Turso:** suman un proveedor o pierden el FTS de Postgres.
- **Vercel Pro + Neon / Cloudflare Workers (OpenNext):** más coste o límites de tamaño e imágenes. Railway ya existe.

## Consecuencias
- **1 instancia de la app.** `revalidateTag` e ISR cumplen RNF-07 con 1 instancia. Escalar a más de 1 exige un `cacheHandler` compartido (p. ej. Redis), con su propio ADR.
- **Coste estimado:** Railway Hobby $5/mes con $5 de uso incluido, más el exceso (no confirmado hasta medir en `develop`). R2 $0 con las imágenes (≈ 1,6 GB) y ≈ $0,30/mes si cada programa guarda 1 vídeo de 100 MB. Dominio ya pagado.
- **RNF-16 (backups):** no está confirmado qué planes de Railway incluyen los backups de volumen. DevOps lo verifica en la spec 001. Si el plan no los incluye, programa un `pg_dump` diario a R2 con el cron de Railway.
- **Cron en UTC** (Railway). La caducidad y la programación (RF-19, RF-20, RF-39) convierten a la zona de la agencia en el código (RNF-14).
- **RNF-05 (auth):** la librería de sesiones y el hash de contraseñas van en un ADR propio, en la spec del CMS.
