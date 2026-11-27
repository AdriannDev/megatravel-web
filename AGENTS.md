# Megatravel web

<!-- Fuente única de reglas para todos los agentes (Codex lo lee directo; Claude vía CLAUDE.md). Máximo 150 líneas. Dueño: Arquitecto. -->

## Qué es
Web pública de programas de viaje de la agencia y CMS a medida para mantenerlos (Producto, Marketing y Administrador). Brief: `docs/producto/brief.md`.
Perfil: **M** (ver `docs/00-proyecto.md`). Marco del equipo: `/home/producto/dev/marco-equipo`.
Stack (ADR-001): 1 app Next.js 16 + React + Tailwind v4 + TypeScript · backend integrado (Server Actions y Route Handlers) + Drizzle · PostgreSQL en Railway · medios en Cloudflare R2. Tokens: `[ruta, la fija UX/UI]`. Preview de `develop`: `[URL, la fija DevOps en la 001]`.
Rutas: web pública en `/` · CMS en `/admin`, en la misma app. **1 sola instancia** de la app (más instancias exigen ADR de caché compartida).

## Dónde está cada cosa
| Necesito | Archivo |
|---|---|
| Perfil y límites | `docs/00-proyecto.md` |
| Requisitos (`RF-xx`, `RNF-xx`) | `docs/producto/requisitos.md` |
| Reglas no negociables | `docs/arquitectura/constitucion.md` |
| Decisiones (stack, dependencias) | `docs/arquitectura/adr/` |
| Dónde va cada tipo de código | `docs/arquitectura/mapa-de-codigo.md` |
| Qué construir: spec, UX y API | `docs/specs/NNN-*/spec.md`, `ux.md`, `api.md` |
| Orden de las specs | `docs/roadmap.md` |
| Despliegue y rollback | `docs/ops/runbook.md` |

**Repo y Paperclip:**
- En el repo va lo que un agente futuro necesita para construir: lo de la tabla de arriba, más el código y los tests.
- En Paperclip va el proceso: contratos, handoffs, veredictos, documentos `qa` y `dictamen`, capturas y estado de las tareas.

## Cómo se trabaja (siempre)
1. **El issue es tu contrato.** Su `Tipo` dice qué skill usar. Lee solo su *Lectura mínima*: no explores el repo.
2. **Nada sin spec aprobada** (o issue de ruta corta). Si falta algo, dilo en el issue; no lo inventes.
3. **Reutiliza antes de crear**: `graphify query` antes de escribir una función, componente, hook o tipo.
4. **Lo mínimo que cumple**: ninguna abstracción hasta el tercer uso real, ninguna capa sobre el framework, nada "por si acaso".
5. **Ninguna dependencia nueva sin ADR** aprobado por el Board.
6. **Tu alcance**: solo los archivos permitidos y dentro del presupuesto.
7. **Evidencia**: salida de tests, lint o build, o capturas. Nunca solo "listo".
8. **Nunca toques `main`.** Trabajas en la rama de tu issue; solo DevOps integra en `develop`.
9. **No debilites la CI**: ni umbrales, ni tests saltados, ni `ignore` sin ADR.
10. **No leas ni edites** `.env*` (salvo `.env.example`) ni secretos; pide el nombre de la variable. Los lockfiles solo los actualiza DevOps, con el gestor de paquetes y con ADR.

## Cómo respondes
- **Formato**: solo la plantilla de tu skill. No repites el contrato, no explicas teoría ni resumes lo que ya está enlazado.
- **Comentarios**: 15 líneas como máximo, salvo las tablas de evidencia.
- **Preguntas al Board**: con tarjetas (`ask_user_questions` o `request_confirmation`), todas en una y con opciones concretas. Después, el issue va a `in_review`.
- **`complain` y `suggestion-box`**: Paperclip las monta siempre, pero este equipo no las usa. Las propuestas de mejora van en la "Salud del proceso" del dictamen pre-merge.

## Severidad y veredictos (únicos para todo el equipo)
| Nivel | Significa | Efecto |
|---|---|---|
| **P0** | Caída, pérdida o corrupción de datos, seguridad o permisos, flujo principal inusable | Bloquea |
| **P1** | Incumple un criterio (`R`, `UX` o API) o rompe el contrato | Bloquea |
| **P2** | Fallo menor con alternativa, o desviación de token o copy | No bloquea: va al issue de ajustes de la spec |
| **P3** | Cosmético o mejora | No bloquea: va al backlog |

**Veredictos:**
- `APROBADO`: sin hallazgos.
- `APROBADO CON NOTAS`: solo P2 o P3.
- `CAMBIOS REQUERIDOS`: hay algún P0 o P1.

**Rondas:**
- Como máximo **2** por revisión o verificación.
- La 2.ª solo comprueba los hallazgos de la 1.ª; algo nuevo solo bloquea si es una regresión.
- Después, el Orquestador corta el ciclo.

## Contexto (semáforo)
- **Verde** (< 40 % de 200k): trabaja.
- **Amarillo** (40–50 %): termina el paso, haz el handoff y cierra.
- **Rojo** (compactación): handoff con "Contexto: compactado" y cierra.

Una tarea que no cabe en una sesión estaba mal dimensionada.

## Handoff (al cerrar cada run)
La skill puede aparecer con sufijo (p. ej. `handoff--7f46fe5d96`). Si no la encuentras, este formato basta.
- **Comentario en el issue**: **Hecho · Pendiente · Archivos tocados · Comandos y resultado · Siguiente paso · Contexto**.
- **Rama**: push de tu rama.
- **Commits**: Conventional Commits, en inglés, en imperativo, **sin Co-Authored-By ni menciones a herramientas de IA**.

## Comandos
<!-- Los rellena DevOps en la spec 001. Solo comandos verificados. -->
- Instalar: `[ ]`
- Desarrollo: `[ ]`
- Tests rápidos (por zona): `[ ]`
- Sensores rápidos (lint, tipos, jscpd, knip): `[ ]`
- CI completa: `[ ]`
- Build: `[ ]`

## Convenciones
<!-- Solo lo que difiera de los defaults del formateador. Se rellena en la spec 001. -->
- Ramas: `main` (solo el Board) ← `develop` (solo DevOps) ← rama de issue `<ID>-<slug>`.
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
