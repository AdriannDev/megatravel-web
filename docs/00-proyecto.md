# 00 · Proyecto

## Ficha
| Campo | Valor |
|---|---|
| Nombre | Megatravel Web |
| Perfil | **M**: rediseño de 1–2 meses, varios módulos (home, listados, detalle, CMS), datos públicos. Security entra por las cuentas del CMS y las fotos de pasajeros |
| Repo | `~/dev/megatravel-web` · remoto: pendiente (crear repo privado en GitHub y proteger `main`) |
| Proyecto en Paperclip | Megatravel Web (empresa Megatravel) |
| Inicio | 2026-11-25 |
| Referencia (solo lectura) | Web actual: `/mnt/c/Users/KelingMireyaMachacua/CLAUDE PROYECTOS/megatravel/bloqueosweb` (Next.js 16 + Payload 3 + PostgreSQL en Railway). Útil para el modelo de datos de programas y salidas y para la migración (spec 008). No se modifica |

## Equipo activo
| Rol | Activo | Notas |
|---|---|---|
| Orquestador | Sí | |
| Product Analyst | Sí | Empieza con la spec 000 |
| Arquitecto | Sí | Decide stack y CMS (ADR-001) |
| UX/UI Designer | Sí | Diseño a medida de la web y del CMS (spec 002) |
| Frontend Engineer | Sí | |
| Backend Engineer | Sí | |
| QA Engineer | Sí | |
| Code Reviewer | Sí | |
| Security Reviewer | Parcial | Specs 001 (auth del CMS), 003 (roles y vista previa), 004 (subida de archivos y fotos) y 010 (lanzamiento) |
| Researcher | Sí | Investigación de stack y CMS; después bajo demanda |
| DevOps / Integrador | Sí | Desde la spec 001 |
| Tech Writer | Sí | Guía de editores del CMS al cerrar la spec 004 |
| Auditor | Sí | CP0–CP5 |

## Límites
| Límite | Valor |
|---|---|
| Tamaño de tarea | ≤ 8 archivos · ≤ 400 líneas de diff |
| Techo de contexto | < 50 % de 200k (≈100k tokens); handoff al 40 % |
| Rondas de revisión antes de issue de corrección | 2 |
| CP3 | cada 3 tareas integradas |

## Ramas
`main` (solo humano, tras CP4) ← `develop` (DevOps) ← `<ID>-<slug>` (worktree de cada issue).

## Cambios de perfil
| Fecha | De → a | Motivo |
|---|---|---|
| 2026-11-25 | — → M | Arranque |
