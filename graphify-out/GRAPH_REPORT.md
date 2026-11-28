# Graph Report - MEG-42-Arquitecto  (2026-11-28)

## Corpus Check
- 39 files · ~21,727 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .toml 1, .css 1)

## Summary
- 254 nodes · 279 edges · 26 communities (19 shown, 7 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0d636324`
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
- package.json
- react
- compilerOptions
- scripts
- ci.yml
- Spec 001b · Datos y acceso al CMS
- ADR-003 · Sesiones y hash de contraseñas del CMS

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 16 edges
2. `Megatravel web` - 12 edges
3. `Spec 001b · Datos y acceso al CMS` - 12 edges
4. `Spec 001 · Fundaciones` - 11 edges
5. `scripts` - 10 edges
6. `Constitución` - 9 edges
7. `Brief` - 9 edges
8. `Funcionales` - 9 edges
9. `ok()` - 7 edges
10. `react` - 7 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (26 total, 7 thin omitted)

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

### Community 14 - "package.json"
Cohesion: 0.10
Nodes (26): devDependencies, eslint@^9, eslint-config-next@16.4.6, jscpd@^5, knip@^6, tailwindcss@4.3.3, @tailwindcss/turbopack@4.3.3, @types/node@^24 (+18 more)

### Community 20 - "react"
Cohesion: 0.13
Nodes (14): nextConfig, dependencies, next@16.4.6, react@19.3.0, react-dom@19.3.0, vitest@^5, next, react (+6 more)

### Community 21 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 22 - "scripts"
Cohesion: 0.20
Nodes (10): scripts, build, check, dev, dup, knip, lint, start (+2 more)

### Community 23 - "ci.yml"
Cohesion: 0.11
Nodes (18): runs-on, steps, jobs, ci, name, on, pull_request, push (+10 more)

### Community 24 - "Spec 001b · Datos y acceso al CMS"
Cohesion: 0.15
Nodes (12): 10. Tareas, 1. Problema y objetivo, 2. Requisitos, 3. No debe cambiar, 4. Fuera de alcance, 5. Inventario de reutilización, 6. Diseño, 7. Complejidad justificada (+4 more)

### Community 25 - "ADR-003 · Sesiones y hash de contraseñas del CMS"
Cohesion: 0.29
Nodes (6): ADR-003 · Sesiones y hash de contraseñas del CMS, Cómo revertir, Decisión, Fuentes (consultadas el 2026-11-28), Impacto por agente, Motivo y trade-offs

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `scripts` connect `scripts` to `package.json`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.10052910052910052 - nodes in this community are weakly interconnected._
- **Why does `devDependencies` connect `package.json` to `react`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Should `react` be split into smaller, more focused modules?**
  _Cohesion score 0.1341991341991342 - nodes in this community are weakly interconnected._
- **Why does `react` connect `react` to `package.json`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Should `compilerOptions` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `ci.yml` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._