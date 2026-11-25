# Mapa de código

Dónde va cada tipo de cosa. Corto a propósito: el índice detallado es el grafo (`graphify query`). Lo mantiene el Tech Writer; lo cambia el Arquitecto. Sigue la estructura de la plantilla oficial de Payload 3 + Next.js (ADR-001); las capas y lo que cada una puede importar están en `arquitectura.md`.

Aún no hay código: la columna "Ejemplo existente" se rellena en la spec 001 con el primer archivo real de cada fila.

| Tipo de código | Carpeta | Ejemplo existente |
|---|---|---|
| Páginas y rutas públicas (home, listados, detalle, vista previa) | `src/app/(frontend)/` | — |
| Rutas del panel y API de Payload (generadas, no se editan a mano) | `src/app/(payload)/` | — |
| Componentes de UI pública reutilizables (reciben datos por props) | `src/components/` | — |
| Componentes y vistas del panel a medida (CMS) | `src/admin/` | — |
| Colecciones de Payload (campos, validaciones, hooks propios de la colección al lado) | `src/collections/` (un archivo, o carpeta si crece, por colección) | — |
| Globals de Payload (home, configuración) | `src/globals/` | — |
| Matriz de permisos rol × acción (funciones de acceso) | `src/access/` | — |
| Configuración de Payload | `src/payload.config.ts` | — |
| Tipos de contenido (generados por `payload generate:types`) | `src/payload-types.ts` | — |
| Utilidades puras del dominio (vigencia y corte, cupos, filtros de URL, formatos de precio y fecha) | `src/lib/` | — |
| Tokens de diseño y estilos globales | `src/styles/` | — |
| Migraciones de esquema (generadas por `payload migrate:create`) | `src/migrations/` | — |
| Scripts de una vez (migración de datos, semillas) | `scripts/` | — |
| Tests unitarios y de integración | junto al archivo: `*.test.ts` / `*.test.tsx` | — |
| Tests end-to-end | `tests/e2e/` | — |

## Reglas de ubicación
- Si una utilidad la usa un solo módulo, vive junto a ese módulo; pasa a la carpeta compartida al tercer uso.
- Una consulta a Payload vive en la ruta que la usa. Si tres rutas repiten la misma consulta, se mueve a una función en la carpeta de la ruta común más cercana (p. ej. `src/app/(frontend)/_datos/`), nunca a un "repositorio".
- Un hook de Payload vive con su colección; si lo usan tres colecciones (p. ej. historial o invalidación de caché), pasa a `src/collections/_compartido/`.
- No se crean carpetas `utils2`, `helpers-new`, `services`, `repositories` ni similares: se extiende la existente.
- Nada de texto comercial en el código (art. 21): los textos visibles vienen del CMS; solo los mensajes de interfaz (errores, etiquetas de formulario) pueden vivir en componentes.
