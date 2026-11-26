# Constitución

Reglas no negociables. Toda spec, plan y línea de código las respeta. El Arquitecto la mantiene; el Auditor y el Arquitecto la usan como criterio al revisar. Máximo ~30 artículos. Una excepción solo con ADR y fecha de revisión.

## I. Simplicidad
1. Se implementa lo mínimo que cumple la spec. Nada de "future-proofing".
2. Ninguna abstracción hasta el tercer uso real (regla de tres).
3. Toda complejidad extra se justifica en la tabla "Complejidad justificada" del plan.

## II. Anti-abstracción
4. Se usa el framework directamente; no se envuelve en capas propias.
5. Un solo modelo por concepto: no hay DTOs, mappers ni repositorios duplicando la misma forma sin motivo escrito.

## III. Reutilización
6. Antes de crear código se consulta el grafo (`graphify query`) y el mapa de código; el plan incluye el inventario de reutilización.
7. Ninguna dependencia nueva sin ADR.

## IV. Calidad
8. Todo cambio de comportamiento lleva test; todo bug corregido lleva test de regresión.
9. Los sensores (lint, tipos, tests, duplicación, código muerto, capas) pasan antes de integrar. Debilitarlos requiere ADR.
10. Sin código muerto; los comentarios explican el porqué, no el qué.

## V. Seguridad
11. Ningún secreto en el repositorio; configuración por variables de entorno documentadas en `.env.example`.
12. Toda entrada externa se valida en el servidor; consultas parametrizadas; autorización explícita en cada acción.
13. Datos personales: los mínimos, nunca en logs, con consentimiento y forma de borrarlos.

## VI. Proceso
14. No se implementa lo que no está en una spec aprobada (o en la ruta corta del roadmap).
15. Quien escribe un artefacto no lo aprueba.
16. `main` solo lo actualiza el Board tras el dictamen pre-merge del Auditor; `develop` solo DevOps.

## VII. Experiencia de usuario (si hay UI)
17. Todos los valores visuales vienen de los tokens de diseño.
18. Funciona con teclado, formularios etiquetados, errores comprensibles, móvil desde 360 px.

## VIII. Reglas del dominio
19. [Específicas del proyecto.]
