# Graph Report - megatravel-web  (2026-11-26)

## Corpus Check
- 24 files · ~10,374 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 4, .toml 1)

## Summary
- 102 nodes · 109 edges · 16 communities (9 shown, 7 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2742ea6e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _common.py
- [NOMBRE DEL PROYECTO]
- Constitución
- Brief
- Runbook
- 00 · Proyecto
- Arquitectura
- Requisitos
- Roadmap
- Mapa de código
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `[NOMBRE DEL PROYECTO]` - 12 edges
2. `Constitución` - 9 edges
3. `Brief` - 9 edges
4. `ok()` - 7 edges
5. `00 · Proyecto` - 6 edges
6. `Arquitectura` - 6 edges
7. `Runbook` - 6 edges
8. `load_config()` - 6 edges
9. `read_event()` - 6 edges
10. `block()` - 5 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (16 total, 7 thin omitted)

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
Cohesion: 0.29
Nodes (6): 00 · Proyecto, Cambios de perfil, Equipo activo (según el perfil, ver `docs/07` del marco), Ficha, Límites, Ramas

### Community 7 - "Arquitectura"
Cohesion: 0.29
Nodes (6): Arquitectura, Capas y dependencias permitidas, Datos, Decisiones, Entornos, Vista general

### Community 9 - "Requisitos"
Cohesion: 0.50
Nodes (3): Funcionales, No funcionales, Requisitos

### Community 10 - "Roadmap"
Cohesion: 0.50
Nodes (3): Roadmap, Ruta corta, Specs

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Not enough signal to generate questions. This usually means the corpus has no AMBIGUOUS edges, no bridge nodes, no INFERRED relationships, and all communities are tightly cohesive. Add more files or run with --mode deep to extract richer edges._