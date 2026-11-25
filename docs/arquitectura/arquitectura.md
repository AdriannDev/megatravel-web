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
- **Caché y vigencia**: páginas públicas cacheadas con etiquetas por colección; los hooks `afterChange`/`afterDelete` de Payload invalidan las etiquetas al publicar. Las reglas de vigencia (corte 00:00 America/Lima RF-23, fin de banner RF-07, cupos 72 h RF-18) se evalúan al consultar con funciones puras de `src/lib`, y la caché tiene vida máxima corta (valor exacto en la spec 005/006, ≤ 15 min como referencia) para que caduquen sin cron.
- **Vista previa (RF-39/40)**: Live Preview de Payload + Draft Mode de Next en `/preview`, solo con sesión del CMS, `noindex` y sin caché.
- **Redirecciones (RF-45, RF-45b, RF-45c)**: en `next.config` o en `src/proxy.ts`/middleware de Next, según lo que fije la spec 009.

## Capas y dependencias permitidas
Rutas relativas a `src/`. Cada fila se traduce a una regla `forbidden` de dependency-cruiser en la spec 001. "Externos" son paquetes de `node_modules`.

| Capa | Carpeta | Puede depender de | No puede depender de |
|---|---|---|---|
| Utilidades de dominio | `lib/` | `lib/`, `payload-types.ts` (solo tipos) | `app/`, `components/`, `admin/`, `collections/`, `globals/`, `access/`, `payload.config.ts`; externos `next`, `react`, `payload`, `@payloadcms/*` |
| Control de acceso | `access/` | `lib/`, `payload-types.ts`, `payload` (tipos) | `app/`, `components/`, `admin/`, `collections/`, `globals/` |
| Modelo de contenido | `collections/`, `globals/` | `access/`, `lib/`, `payload-types.ts`, otras colecciones, `payload`, `@payloadcms/*`, `next/cache` (invalidar en hooks) | `app/`, `components/`, `admin/` (el panel se referencia por ruta de texto en la config, no por import) |
| Configuración de Payload | `payload.config.ts` | `collections/`, `globals/`, `access/`, `lib/`, `payload`, `@payloadcms/*` | `app/`, `components/`, `admin/` |
| Panel a medida | `admin/` | `components/`, `lib/`, `payload-types.ts`, `@payloadcms/ui`, `react`, `next` | `app/`, `collections/`, `globals/`, `access/`, `payload.config.ts`, `payload` (runtime de servidor) |
| UI pública | `components/` | `components/`, `lib/`, `payload-types.ts` (solo tipos), `react`, `next` | `app/`, `admin/`, `collections/`, `globals/`, `access/`, `payload.config.ts`, `payload`, `@payloadcms/*` |
| Rutas públicas | `app/(frontend)/` | `components/`, `lib/`, `payload-types.ts`, `@payload-config`, `payload`, `next`, `react` | `admin/`, `collections/`, `globals/`, `access/` (se pasa siempre por la Local API) |
| Rutas de Payload | `app/(payload)/` | Generado por Payload; se excluye de las reglas | — |
| Migraciones | `migrations/` | Generado por Payload; se excluye de las reglas | — |
| Scripts | `../scripts/` | `lib/`, `payload-types.ts`, `@payload-config`, `payload` | Nada de `src/` importa `scripts/` |
| Tests | `**/*.test.ts(x)`, `../tests/` | Cualquier capa | Nada de `src/` (salvo otros tests) importa tests |

Reglas globales:
- Sin dependencias circulares.
- Acceso a datos **solo por Payload**: `pg`, `drizzle-orm` y `@payloadcms/drizzle` no se importan fuera de `migrations/`. SQL propio requiere ADR.
- Ningún archivo importa de `bloqueosweb` ni se conecta a su base (art. 20).
- Ningún módulo de cliente (`"use client"`) importa `payload`, `@payload-config`, `collections/` ni `access/`.

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
