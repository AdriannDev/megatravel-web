# Mapa de código

Dónde va cada tipo de cosa. Corto a propósito: el índice detallado es el grafo (`graphify query`). Lo mantiene el Arquitecto (en cada spec que crea una zona nueva).

| Tipo de código | Carpeta | Ejemplo existente |
|---|---|---|
| [Componentes de UI reutilizables] | | |
| [Páginas / rutas] | | |
| [Acceso a datos] | | |
| [Utilidades puras] | | |
| [Tipos compartidos] | | |
| [Tests] | | |

## Reglas de ubicación
- Si una utilidad la usa un solo módulo, vive junto a ese módulo; pasa a la carpeta compartida al tercer uso.
- No se crean carpetas `utils2`, `helpers-new` ni similares: se extiende la existente.
