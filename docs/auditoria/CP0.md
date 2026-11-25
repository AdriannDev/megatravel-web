# CP0 · Arranque del proyecto · 2026-11-25

**Veredicto** — NO CONFORME

## Comprobaciones

Referencias del marco: [06 · Checkpoints](/home/producto/dev/marco-equipo/docs/06-auditoria-checkpoints.md#checkpoints), [04 · Valores por rol](/home/producto/dev/marco-equipo/docs/04-limites-y-contexto.md#5-valores-por-rol-configuración-del-agente-el-auditor-los-ajusta-con-datos) y [08 · Configurar Paperclip](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md). Corte de evidencia del 25 de noviembre de 2026, hora de Lima. El worktree partió de `f644c60577ee048fbdc5ed07a21bcaa4384c891c`, que devolvieron `git rev-parse HEAD origin/develop` y `git ls-remote --heads origin develop` para la rama remota.

| # | Regla | Resultado | Evidencia |
|---|---|---|---|
| 1 | [06 · Perfil elegido, justificado y equipo activo](/home/producto/dev/marco-equipo/docs/06-auditoria-checkpoints.md#checkpoints) | Conforme | [Ficha y equipo](../00-proyecto.md#ficha) declaran perfil **M** por duración de 1–2 meses, varios módulos y datos públicos, e identifican 12 roles activos. La API de agentes devolvió los 12 roles, 11 en `idle` y el Auditor en `running`. |
| 2 | [08 §3 · Configuración de los 12 agentes](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md#3-agentes) y [04 §5 · Límites](/home/producto/dev/marco-equipo/docs/04-limites-y-contexto.md#5-valores-por-rol-configuración-del-agente-el-auditor-los-ajusta-con-datos) | No conforme | Backend con esfuerzo `high` frente a `medium`. El Arquitecto usa la alternativa Opus prevista en §0, con cuota de Fable sin verificar. Los límites de turnos y tiempo coinciden en los 12 roles. La API devuelve `heartbeat.enabled=false`, `wakeOnDemand=true` y `maxConcurrentRuns=1` en los 12. Véase el detalle por agente. |
| 3 | [08 §2–3 · Permisos y creación de agentes](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md#2-valores-comunes-a-todos-los-agentes) | Creación conforme. Asignación no conforme. | `canCreateAgents=true` solo en Orquestador. `canCreateSkills=true` solo en Orquestador y Tech Writer. Siete agentes adicionales tienen `canAssignTasks=true`. |
| 4 | [06 · Protección de main](/home/producto/dev/marco-equipo/docs/06-auditoria-checkpoints.md#checkpoints) y [regla del repo](../00-proyecto.md#ramas) | Protección local conforme. Remota no conforme. | `git config --show-origin --get core.hooksPath` → `.githooks`, desde la configuración compartida del repo. `git ls-files --stage .githooks/reference-transaction` → modo `100755`. Con una actualización simulada por entrada estándar, el hook en fase `prepared` devolvió `BLOQUEADO: refs/heads/main solo lo actualiza el humano tras CP4` y código 1. `gh api repos/AdriannDev/megatravel-web/branches/main` → `protected:false`. La ruta `branches/main/protection` devolvió HTTP 404, «Branch not protected», y `rules/branches/main` devolvió `[]`. |
| 5 | [06 · Graphify instalado](/home/producto/dev/marco-equipo/docs/06-auditoria-checkpoints.md#checkpoints) | Conforme | `command -v graphify` → `/home/producto/.local/bin/graphify`. `graphify --version` → `0.9.119`. `graphify query "Perfil M, equipo activo y configuración de arranque CP0 en docs/00-proyecto.md" --budget 1000` → grafo de 117 nodos y referencias a la ficha, equipo y límites del proyecto. |
| 6 | [06 · AGENTS.md ≤ 150 líneas](/home/producto/dev/marco-equipo/docs/06-auditoria-checkpoints.md#checkpoints) | Conforme | `wc -l AGENTS.md` → `72 AGENTS.md`. |
| 7 | [08 §5 · Repo ref y URL](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md#5-proyecto) | Conforme | `GET /api/issues/{MEG-6}` → `project.primaryWorkspace.repoRef=origin/develop` y `project.codebase.repoRef=origin/develop`. `project.primaryWorkspace.repoUrl` coincide con `git config --local --get remote.origin.url`: `https://github.com/AdriannDev/megatravel-web`. |
| 8 | [08 §6 · Revisión de la primera tanda](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md#6-primera-tanda-de-issues) | Configuración no conforme | `GET /api/issues/{id}` para [MEG-7](/MEG/issues/MEG-7) y [MEG-8](/MEG/issues/MEG-8) → `status=todo`, `startedAt=null`, `executionPolicy=null`. Falta la etapa de revisión por el Arquitecto en ambos. La actividad de MEG-7 solo registra su creación. |

### Configuración por agente

Evidencia de la tabla: `GET /api/companies/{companyId}/agents`, campos `adapterType`, `adapterConfig`, `reportsTo` y `permissions`. Esfuerzo de Claude en `adapterConfig.effort` y de Codex en `adapterConfig.modelReasoningEffort`. Los permisos se muestran en orden **asignar / crear agentes / crear skills**. Se consultó también `GET /api/agents/{id}/config-revisions` para los 12 roles. La última columna recoge el contraste con [08 §2–3](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md#3-agentes).

| Agente | Adaptador · modelo · esfuerzo | Turnos / segundos | Reporta a | Permisos | Diferencia o extra |
|---|---|---|---|---|---|
| Orquestador | `claude_local` · `claude-opus-5-5` · high | 60 / 1800 | Sin superior (`null`) | Sí / Sí / Sí | Conforme |
| Product Analyst | `claude_local` · `claude-sonnet-5-5` · medium | 80 / 1800 | Orquestador | No / No / No | Conforme |
| Arquitecto | `claude_local` · `claude-opus-5-5` · high | 100 / 2700 | Orquestador | Sí / No / No | Asignación adicional. [08 §0](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md#0-antes-de-empezar) permite Opus cuando la cuota de Fable es insuficiente. El cambio de modelo registrado el 25 de noviembre a las 15:45 UTC muestra `null → claude-opus-5-5`. La revisión no documenta la cuota. |
| UX/UI Designer | `claude_local` · `claude-opus-5-5` · high | 120 / 2700 | Orquestador | Sí / No / No | Asignación adicional. `chrome=true`. |
| Frontend Engineer | `claude_local` · `claude-opus-5-5` · high | 150 / 2700 | Orquestador | Sí / No / No | Asignación adicional |
| Backend Engineer | `claude_local` · `claude-sonnet-5-5` · high | 150 / 2700 | Orquestador | No / No / No | Esfuerzo esperado `medium` |
| QA Engineer | `claude_local` · `claude-sonnet-5-5` · medium | 120 / 2700 | Orquestador | Sí / No / No | Asignación adicional. `chrome=true`. |
| Code Reviewer | `codex_local` · `gpt-6.2-astra` · medium | — / 1800 | Orquestador | Sí / No / No | Asignación adicional |
| Researcher | `codex_local` · `gpt-6.2-sol` · medium | — / 1800 | Orquestador | Sí / No / No | Asignación adicional. `search=true`. |
| DevOps / Integrador | `codex_local` · `gpt-6.2-sol` · medium | — / 2700 | Orquestador | No / No / No | Conforme |
| Tech Writer | `claude_local` · `claude-haiku-5-5` · Auto | 60 / 1200 | Orquestador | Sí / No / Sí | Asignación adicional. `effort` ausente, conforme al modo Auto de Haiku. |
| Auditor | `codex_local` · `gpt-6.2-sol` · medium | — / 1800 | Board (`reportsTo=null`) | No / No / No | Conforme |

## Métricas

Umbrales de [06 · Métricas, perfil M](/home/producto/dev/marco-equipo/docs/06-auditoria-checkpoints.md#métricas). La ventana es el arranque y el run de MEG-6 al corte. `GET /api/issues/{MEG-6}/diagnostics/subtree` devolvió un nodo y dos solicitudes de despertar asociadas al mismo run, una reclamada y una coalescida.

| Métrica | Valor al corte | Umbral de alerta |
|---|---|---|
| Runs por tarea | 1 visible para MEG-6 en `GET /api/companies/{companyId}/heartbeat-runs`, filtrado por `issueId` del resultado | > 3 |
| Sesiones reanudadas | 0 observadas. El run en curso devuelve `sessionIdBefore=null` y `sessionIdAfter=null` al corte | > 2 |
| Contexto estimado | Pendiente de contabilizar. El run en curso devuelve `inputTokens=0` al corte | > 100 000 por run |
| Compactaciones | 0 observadas durante el run de MEG-6 al corte | Cualquiera |
| Rondas de revisión | 0 transiciones visibles en `GET /api/issues/{MEG-6}/activity` | ≥ 2 |
| Diff fuera de contrato | 0 archivos fuera del alcance de MEG-6, según `git diff --name-only origin/develop...HEAD` al verificar la entrega | > 0 |
| Duplicación y código muerto nuevos | No aplican a este checkpoint documental | > 0 en jscpd o knip, respectivamente |
| Tareas reabiertas tras integrar | Sin base de cálculo en esta primera tanda, según la lista de issues del proyecto | > 10 % |
| Presión de cuota | 0 errores observados para MEG-6 al corte, `errorCode=null` | Cualquier error de cuota |

## Observaciones y propuestas

- Para desbloquear la primera tanda, registrar en Paperclip la revisión por el Arquitecto de [MEG-7](/MEG/issues/MEG-7) y [MEG-8](/MEG/issues/MEG-8), alinear el esfuerzo del Backend y retirar los siete permisos de asignación adicionales. Las reglas aplicables son [08 §2–3 y §6](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md#2-valores-comunes-a-todos-los-agentes).
- Para acreditar la protección de `main`, verificar en GitHub una regla activa que preserve el control humano establecido en la [ficha del proyecto](../00-proyecto.md#ramas) y en el [CP0 del marco](/home/producto/dev/marco-equipo/docs/06-auditoria-checkpoints.md#checkpoints).
- La evidencia de cuota del Arquitecto y los resultados de **Test Environment** por agente quedan sin verificar. Las revisiones de configuración acreditan valores guardados. El criterio de cuota y la prueba de entorno figuran en [08 §0 y §3](/home/producto/dev/marco-equipo/docs/08-configurar-paperclip.md#0-antes-de-empezar).

## Para el Board

- **CP0 NO CONFORME.** El perfil M, el equipo de 12 roles, Graphify y la base `origin/develop` quedaron verificados.
- Solo el Orquestador puede crear agentes. Siete roles tienen permisos adicionales de asignación y Backend tiene esfuerzo `high` frente a `medium`.
- El hook local protege `main`. GitHub devolvió `protected:false` y ninguna regla activa para esa rama.
- Spec 000 e Investigación están pendientes de configurar la revisión del Arquitecto en Paperclip.
