# 00 · Proyecto

## Ficha
| Campo | Valor |
|---|---|
| Nombre | Megatravel web: web de programas de viaje y CMS a medida |
| Perfil | **M** (propuesto, pendiente de aprobación del Board · MEG-25). Motivo en «Justificación del perfil» |
| Repo | `~/dev/megatravel-web` · remoto: `https://github.com/AdriannDev/megatravel-web` |
| Proyecto en Paperclip | Megatravel |
| Inicio | 2026-11-27 |

### Justificación del perfil (tabla de `docs/07` del marco)
| Criterio | Megatravel | Perfil que indica |
|---|---|---|
| Datos | Contenido público y cuentas de editores. Sin datos personales de clientes (contacto por enlaces, sin formulario) ni pagos | M |
| Usuarios | Usuarios reales: clientes de la agencia y 3 roles internos | M |
| Alcance | Varios módulos: web pública, CMS con roles y automatización de cupos | M |
| Duración | 1–2 meses estimados (11 specs en la v1) | M |
| Disponibilidad | Sin SLA ni operación crítica 24/7 | No sube a L |

No es L porque no hay pagos, ni datos personales, ni SLA, y la integración con Google Drive va en v1.1. **Revisar el perfil** si se añaden formulario de contacto, reservas o pagos, o si la 012 lo justifica. Cualquier cambio se anota en «Cambios de perfil».

## Equipo activo (según el perfil, ver `docs/07` del marco)
| Rol | Activo | Notas |
|---|---|---|
| Orquestador | Sí | |
| Arquitecto | Sí | |
| UX/UI Designer | Sí | Inventario de la web contra Figma. CMS cuando llegue su prototipo |
| Frontend Engineer | Sí | |
| Backend Engineer | Sí | |
| QA Engineer | Sí | QA por spec |
| DevOps / Integrador | Sí | |
| Auditor | Sí | Auditoría de arranque y dictamen pre-merge |

## Límites
| Límite | Valor |
|---|---|
| Tamaño de tarea | ≤ 8 archivos · ≤ 400 líneas de diff |
| Techo de contexto | < 50 % de 200k (≈100k tokens); handoff al 40 % |
| Rondas por revisión | 2 (después corta el Orquestador) |
| Dictamen pre-merge | Por release, antes de cada merge a `main` |

## Ramas
`main` (solo el Board, tras el dictamen pre-merge) ← `develop` (solo DevOps) ← `<ID>-<slug>` (worktree de cada issue).

## Cambios de perfil
| Fecha | De → a | Motivo |
|---|---|---|
