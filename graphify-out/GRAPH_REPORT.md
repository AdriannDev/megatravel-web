# Graph Report - megatravel-web  (2026-11-25)

## Corpus Check
- 28 files · ~11,794 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .toml 1)

## Summary
- 117 nodes · 124 edges · 16 communities (11 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2bd25905`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _common.py
- [NOMBRE DEL PROYECTO]
- Constitución
- Brief
- Spec NNN · [Nombre]
- 00 · Proyecto
- ADR-NNN · [Título de la decisión]
- Arquitectura
- Plan · Spec NNN
- Requisitos
- Primera tanda de issues (las crea el Board en Paperclip)
- Mapa de código
- CLAUDE.md
- README.md
- tasks.md

## God Nodes (most connected - your core abstractions)
1. `Megatravel Web` - 10 edges
2. `Constitución` - 9 edges
3. `Brief` - 9 edges
4. `Spec NNN · [Nombre]` - 8 edges
5. `ok()` - 7 edges
6. `load_config()` - 6 edges
7. `read_event()` - 6 edges
8. `00 · Proyecto` - 6 edges
9. `ADR-NNN · [Título de la decisión]` - 6 edges
10. `Arquitectura` - 6 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (16 total, 5 thin omitted)

### Community 0 - "_common.py"
Cohesion: 0.16
Nodes (5): block(), load_config(), normalize(), ok(), read_event()

### Community 1 - "[NOMBRE DEL PROYECTO]"
Cohesion: 0.18
Nodes (10): Comandos, Contexto (semáforo), Convenciones, Cómo se trabaja (siempre), Dónde está cada cosa, Gotchas, graphify, Handoff (al cerrar cada run) (+2 more)

### Community 2 - "Constitución"
Cohesion: 0.20
Nodes (9): Constitución, I. Simplicidad, II. Anti-abstracción, III. Reutilización, IV. Calidad, V. Seguridad, VI. Proceso, VII. Experiencia de usuario (si hay UI) (+1 more)

### Community 3 - "Brief"
Cohesion: 0.20
Nodes (9): Alcance, Brief, Datos, Métricas de éxito, Objetivo de la primera versión, Preguntas abiertas, Problema, Restricciones (+1 more)

### Community 4 - "Spec NNN · [Nombre]"
Cohesion: 0.22
Nodes (8): Comportamiento que no debe cambiar, Criterios de aceptación, Dudas, Fuera de alcance, Problema y objetivo, Requisitos (EARS), Seguridad y datos, Spec NNN · [Nombre]

### Community 5 - "00 · Proyecto"
Cohesion: 0.29
Nodes (6): 00 · Proyecto, Cambios de perfil, Equipo activo, Ficha, Límites, Ramas

### Community 6 - "ADR-NNN · [Título de la decisión]"
Cohesion: 0.29
Nodes (6): ADR-NNN · [Título de la decisión], Consecuencias, Contexto, Decisión, Fuentes, Opciones consideradas

### Community 7 - "Arquitectura"
Cohesion: 0.29
Nodes (6): Arquitectura, Capas y dependencias permitidas, Datos, Decisiones, Entornos, Vista general

### Community 8 - "Plan · Spec NNN"
Cohesion: 0.29
Nodes (6): Complejidad justificada, Diseño, Inventario de reutilización (obligatorio), Plan · Spec NNN, Riesgos, Verificación de la spec completa

### Community 9 - "Requisitos"
Cohesion: 0.50
Nodes (3): Funcionales, No funcionales, Requisitos

### Community 10 - "Primera tanda de issues (las crea el Board en Paperclip)"
Cohesion: 0.22
Nodes (8): ADR-001 · Stack y CMS — Arquitecto (revisión: Code Reviewer) · bloqueado por Spec 000 e Investigación, CP0 · Arranque del proyecto — Auditor, Investigación de stack y CMS — Researcher (revisión: Arquitecto), Primera tanda de issues (las crea el Board en Paperclip), Roadmap · Megatravel Web, Ruta corta, Spec 000 · Brief y requisitos — Product Analyst (revisión: Arquitecto), Specs

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Not enough signal to generate questions. This usually means the corpus has no AMBIGUOUS edges, no bridge nodes, no INFERRED relationships, and all communities are tightly cohesive. Add more files or run with --mode deep to extract richer edges._