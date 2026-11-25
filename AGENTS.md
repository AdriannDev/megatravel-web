# Megatravel Web

<!-- Fuente única de reglas para todos los agentes (Codex y Antigravity la leen directo; Claude vía CLAUDE.md). Máximo 150 líneas. -->

## Qué es
Rediseño completo de bloqueosmegatravel.pe: web de viajes para asesores de agencias de Perú (home de contenido, listados de Bloqueos/Circuitos/zonas y detalle de programa) alimentada por un CMS a medida para el equipo de producto. Las reservas siguen en Meganet. Brief: `docs/producto/brief.md`.
Perfil: **M** (ver `docs/00-proyecto.md`). Marco del equipo: `/home/producto/dev/marco-equipo`.
**La web actual (repo `bloqueosweb`) sigue en producción sin cambios hasta el lanzamiento: no se modifica ni se conecta a su base de datos.**

## Dónde está cada cosa
| Necesito | Archivo |
|---|---|
| Perfil, equipo activo y límites | `docs/00-proyecto.md` |
| Requisitos | `docs/producto/requisitos.md` |
| Reglas no negociables | `docs/arquitectura/constitucion.md` |
| Decisiones (stack, dependencias) | `docs/arquitectura/adr/` |
| Dónde va cada tipo de código | `docs/arquitectura/mapa-de-codigo.md` |
| Qué construir ahora | `docs/specs/NNN-*/` (spec, plan, tasks) |
| Orden de las specs | `docs/roadmap.md` |
| Informes de checkpoints | `docs/auditoria/` |

## Cómo se trabaja (siempre)
1. **El issue de Paperclip es tu contrato.** Lee solo su "Lectura mínima"; no explores el repo por tu cuenta.
2. **No implementes nada que no esté en una spec aprobada** (o en un issue de ruta corta). Si falta algo en la spec, dilo en el issue; no lo inventes.
3. **Reutiliza antes de crear.** Antes de escribir una función, componente, hook o tipo, ejecuta `graphify query`. Si existe algo equivalente, úsalo o extiéndelo.
4. **Lo mínimo que cumple la spec.** Sin abstracciones hasta el tercer uso real, sin capas que envuelvan el framework, sin parámetros "por si acaso".
5. **Ninguna dependencia nueva sin ADR** aprobado.
6. **Quédate en tu alcance**: solo los archivos permitidos del contrato y dentro de su presupuesto (archivos y líneas).
7. **Evidencia**: termina con la salida de tests/lint/build o capturas; nunca solo "listo".
8. **Nunca toques `main`** (ni push, ni checkout, ni merge). Trabaja en la rama de tu issue; DevOps integra en `develop`.
9. **No debilites CI**: no bajes umbrales, no saltes tests, no añadas ignores sin ADR.
10. **No leas ni edites** `.env*`, secretos ni lockfiles; pide el nombre de la variable en el issue.

## Contexto (semáforo)
- Ventana de trabajo: 200k tokens. **Verde** < 40 %: trabaja. **Amarillo** 40–50 %: termina el paso, haz handoff y cierra el run. **Rojo** (compactación): handoff con "Contexto: compactado" y cierra.
- Una tarea que no cabe en una sesión estaba mal dimensionada: dilo en el handoff.

## Handoff (al cerrar cada run)
Comentario en el issue: **Hecho · Pendiente · Archivos tocados · Comandos y resultado · Siguiente paso · Contexto**. Actualiza `tasks.md` y haz push de tu rama. Commits en Conventional Commits, en inglés, en imperativo, **sin líneas Co-Authored-By ni menciones a herramientas de IA** (Claude, Codex u otras).

## Comandos
<!-- Se rellenan en la spec 001 cuando el Arquitecto fije el stack. Solo comandos verificados. -->
- Instalar: `[ ]`
- Desarrollo: `[ ]`
- Tests rápidos (por zona): `[ ]`
- Sensores rápidos (lint, tipos, jscpd, knip): `[ ]`
- CI completa: `[ ]`
- Build: `[ ]`

## Convenciones
<!-- Solo lo que difiera de los defaults del formateador. Se rellena en la spec 001. -->
- Ramas: `main` (solo humano) ← `develop` (integración) ← rama de issue `<ID>-<slug>`.
- Estructura: ver `docs/arquitectura/mapa-de-codigo.md`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. When the answer is under a Markdown heading, `graphify section "<heading>"` prints that section's text, so the .md need not be opened. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.

## Gotchas
<!-- Comportamientos no obvios del entorno; lo que un agente hizo mal más de una vez. -->
- [ ]
