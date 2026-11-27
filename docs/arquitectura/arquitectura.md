# Arquitectura

Estado: stack aceptado (ADR-001). Capas, datos y entornos se detallan en la spec 001

## Vista general
- **App Next.js** (1 servicio `next start` en Railway): web pública en `/` y CMS en `/admin`. Lee y escribe en Postgres con Drizzle desde el servidor.
- **PostgreSQL** (Railway, red privada): contenido, usuarios y roles.
- **Cloudflare R2**: imágenes y vídeos, subidos desde el servidor por la API S3.
- **Cron de Railway** (UTC): caducidad de salidas y publicación programada.

## Capas y dependencias permitidas
<!-- Se traduce a reglas de dependency-cruiser en la spec 001. -->
| Capa | Puede depender de | No puede depender de |
|---|---|---|

## Datos
PostgreSQL con migraciones de drizzle-kit. Modelo en la spec 002.

## Entornos
| Entorno | Para qué | Cómo se despliega |
|---|---|---|

## Decisiones
Ver `adr/`.
