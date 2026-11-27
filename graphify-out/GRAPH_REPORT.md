# Graph Report - MEG-31-Arquitecto  (2026-11-27)

## Corpus Check
- 27 files · ~17,595 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 5, .toml 1)

## Summary
- 136 nodes · 140 edges · 19 communities (12 shown, 7 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `514de1b4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _common.py
- [NOMBRE DEL PROYECTO]
- Constitución
- Brief
- Runbook
- 00 · Proyecto
- Spec 001 · Fundaciones
- Arquitectura
- ADR-002 · Herramientas de desarrollo, CI y sensores
- Funcionales
- Roadmap
- Mapa de código
- CLAUDE.md
- ADR-001 · Stack del proyecto

## God Nodes (most connected - your core abstractions)
1. `Megatravel web` - 12 edges
2. `Spec 001 · Fundaciones` - 11 edges
3. `Constitución` - 9 edges
4. `Brief` - 9 edges
5. `Funcionales` - 9 edges
6. `ok()` - 7 edges
7. `ADR-002 · Herramientas de desarrollo, CI y sensores` - 6 edges
8. `Arquitectura` - 6 edges
9. `load_config()` - 6 edges
10. `read_event()` - 6 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (19 total, 7 thin omitted)

### Community 0 - "_common.py"
Cohesion: 0.16
Nodes (5): block(), load_config(), normalize(), ok(), read_event()

### Community 1 - "[NOMBRE DEL PROYECTO]"
Cohesion: 0.15
Nodes (12): Comandos, Contexto (semáforo), Convenciones, Cómo respondes, Cómo se trabaja (siempre), Dónde está cada cosa, Gotchas, graphify (+4 more)

### Community 2 - "Constitución"
Cohesion: 0.20
Nodes (9): Constitución, I. Simplicidad, II. Anti-abstracción, III. Reutilización, IV. Calidad, V. Seguridad, VI. Proceso, VII. Experiencia de usuario (si hay UI) (+1 more)

### Community 3 - "Brief"
Cohesion: 0.20
Nodes (9): Alcance, Brief, Datos, Métricas de éxito, Objetivo de la primera versión, Preguntas abiertas, Problema, Restricciones (+1 more)

### Community 4 - "Runbook"
Cohesion: 0.29
Nodes (6): Desplegar, Entornos, Migraciones, Rollback, Runbook, Variables de entorno

### Community 5 - "00 · Proyecto"
Cohesion: 0.25
Nodes (7): 00 · Proyecto, Cambios de perfil, Equipo activo (según el perfil, ver `docs/07` del marco), Ficha, Justificación del perfil (tabla de `docs/07` del marco), Límites, Ramas

### Community 6 - "Spec 001 · Fundaciones"
Cohesion: 0.17
Nodes (11): 10. Tareas, 1. Problema y objetivo, 2. Requisitos, 3. No debe cambiar, 4. Fuera de alcance, 5. Inventario de reutilización, 6. Diseño, 7. Complejidad justificada (+3 more)

### Community 7 - "Arquitectura"
Cohesion: 0.29
Nodes (6): Arquitectura, Capas y dependencias permitidas, Datos, Decisiones, Entornos, Vista general

### Community 8 - "ADR-002 · Herramientas de desarrollo, CI y sensores"
Cohesion: 0.29
Nodes (6): ADR-002 · Herramientas de desarrollo, CI y sensores, Alternativas descartadas, Consecuencias, Contexto, Decisión, Fuentes (consultadas el 2026-11-27)

### Community 9 - "Funcionales"
Cohesion: 0.17
Nodes (11): Automatizaciones, CMS: acceso, roles y permisos, CMS: importación y carga inicial, CMS: medios y documentos, CMS: programas, Funcionales, No funcionales, Requisitos (+3 more)

### Community 10 - "Roadmap"
Cohesion: 0.50
Nodes (3): Roadmap, Ruta corta, Specs

### Community 13 - "ADR-001 · Stack del proyecto"
Cohesion: 0.33
Nodes (5): ADR-001 · Stack del proyecto, Alternativas descartadas, Consecuencias, Contexto, Decisión

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Not enough signal to generate questions. This usually means the corpus has no AMBIGUOUS edges, no bridge nodes, no INFERRED relationships, and all communities are tightly cohesive. Add more files or run with --mode deep to extract richer edges._