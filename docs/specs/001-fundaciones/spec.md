# Spec 001 · Fundaciones

Estado: borrador
Autor: Arquitecto · Requisitos que cubre: RNF-01 (stack), constitución art. 9 (sensores) · ADR: ADR-001 (aceptado), ADR-002 (propuesto en esta spec)

## 1. Problema y objetivo
El repo solo tiene documentación: no hay app, CI ni sensores, y la sección «Comandos» de `AGENTS.md` está vacía. Sin esa base, ninguna spec posterior puede integrar con garantías. Al terminar, existe la app Next.js con `/` y `/admin` como esqueletos. Lint, tipos, duplicación, código muerto y tests corren con un solo comando en local y en la CI de cada PR a `develop`. Cualquier agente encuentra en `AGENTS.md` los comandos verificados.

## 2. Requisitos
| ID | Requisito (EARS) | Criterio de aceptación (observable) |
|---|---|---|
| R1 | THE SYSTEM SHALL ser 1 app Next.js 16 (App Router, `src/app`) con React, TypeScript `strict` y Tailwind v4, instalable con npm en Node 24, y con solo las dependencias de ADR-001 y ADR-002. | En un clon limpio con Node 24, `npm ci` y `npm run build` terminan con exit 0. Cada dependencia de `package.json` aparece en ADR-001 o ADR-002. `engines.node` es `24.x` |
| R2 | WHEN un visitante pide `/`, THE SYSTEM SHALL responder 200 con una página esqueleto en español (`<html lang="es">`) que usa al menos 1 utilidad de Tailwind. | Con `npm run start`, `curl -s -o /dev/null -w '%{http_code}' localhost:3000/` devuelve `200`. La clase usada aparece en el CSS de `.next/static`. El test de `/` pasa |
| R3 | WHEN un usuario pide `/admin`, THE SYSTEM SHALL responder 200 con un esqueleto del CMS sin datos ni acciones, marcado `noindex`. | `curl` a `/admin` devuelve `200` y el HTML contiene `<meta name="robots" content="noindex`. El test de `/admin` pasa |
| R4 | IF el código tiene un error o un aviso de ESLint (`eslint-config-next`: `core-web-vitals` + `typescript`) THEN `npm run lint` SHALL terminar con exit ≠ 0. | `npm run lint` da 0 en la rama. En el handoff, la salida de un fallo provocado y no commiteado |
| R5 | IF hay un error de tipos THEN `npm run typecheck` (`tsc --noEmit`) SHALL terminar con exit ≠ 0. | Igual que R4 |
| R6 | IF la duplicación en `src` supera el 3 % THEN `npm run dup` (jscpd) SHALL terminar con exit ≠ 0. | Igual que R4, con un bloque duplicado provocado |
| R7 | IF hay archivos, exports o dependencias sin uso THEN `npm run knip` SHALL terminar con exit ≠ 0. | Igual que R4, con un export sin uso provocado |
| R8 | IF falla un test, o no hay ningún test, THEN `npm test` (Vitest) SHALL terminar con exit ≠ 0. | `npm test` da 0 con los tests de R2 y R3. No se usa `--passWithNoTests` |
| R9 | THE SYSTEM SHALL ofrecer `npm run check`, que ejecuta R4 a R8 en orden y se detiene en el primer fallo. | `npm run check` da exit 0 en la rama. Si se provoca el fallo de R4, da exit ≠ 0 |
| R10 | WHEN se abre o actualiza un PR contra `develop` o `main`, o se hace push a `develop`, THE SYSTEM SHALL ejecutar en GitHub Actions `npm ci`, `npm run check` y `npm run build` en Node 24, y marcar el job como fallido si falla cualquiera de ellos. | Enlace a una ejecución en verde del job `ci` en el PR de integración. El workflow no tiene `continue-on-error` ni pasos que ignoren errores |
| R11 | WHILE corre `npm run dev`, THE SYSTEM SHALL dejar `AGENTS.md` sin cambios (`agentRules: false`, ADR-002). | Tras `npm run dev` con un agente activo, `git status --porcelain AGENTS.md` sale vacío |
| R12 | THE SYSTEM SHALL documentar en `AGENTS.md` § «Comandos» los 6 comandos (instalar, desarrollo, tests por zona, sensores rápidos, CI completa y build), cada uno ejecutado con éxito. | Cada comando de la sección aparece en el handoff de T3 con su salida y exit 0 |

## 3. No debe cambiar
- `docs/producto/*`, ADR-001 y `main`.
- `AGENTS.md`: solo cambian las secciones «Comandos» y «Gotchas» (R12). El resto queda igual (`git diff` lo comprueba).
- Hooks de `.claude/`, `.codex/` y `.githooks/`: ningún sensor los analiza ni los modifica.

## 4. Fuera de alcance
El Board confirma el destino de cada punto en la revisión. La spec **001b** es una propuesta: si se acepta, se añade al roadmap entre la 001 y la 002, y la 002 pasa a depender de ella.

| Punto (roadmap fila 001) | Requisitos | Pasa a | Motivo |
|---|---|---|---|
| Base de datos: Postgres en Railway, Drizzle y migraciones | — | **001b · Datos y acceso al CMS** (propuesta) | La auth es su primer consumidor (tabla de usuarios) |
| Autenticación del CMS y roles comprobados en el servidor | RF-24, RF-28, RNF-05 | **001b** (sensible: sí), con el ADR de sesiones y hash que pide ADR-001 | Es seguridad: necesita su propio gate y su propia auditoría |
| Entornos, deploy en Railway y preview de `develop` | — | **001b** | Sin BD no hay nada útil que desplegar. La URL de preview va a `AGENTS.md` en esa spec |
| Backups de la BD con restauración probada | RNF-16 (BD) | **001b** | Depende de la BD y del plan de Railway (ADR-001, «Consecuencias») |
| Almacenamiento de medios en R2 y backups de medios | RNF-16 (medios) | **005 · Medios y promoción** | Es el primer consumidor real de R2 |
| Tokens de diseño (`AGENTS.md` «Tokens») | RNF-10 | **003** (primera vista pública); los fija UX/UI | En la 001, las páginas son esqueletos sin diseño |
| E2E (Playwright) y sensor de capas | — | **003** y **001b/002**, cada uno con su ADR | No hay flujos ni capas que comprobar todavía |
| Regla de protección de `develop` que exija el check `ci` | — | **Board** (ajustes de GitHub) | Es un ajuste del repositorio; DevOps deja el nombre del check en el handoff de T3 |

## 5. Inventario de reutilización
| Necesidad | Consulta graphify | Existe | Ruta | Decisión |
|---|---|---|---|---|
| Esqueleto de la app (layout y páginas) | `graphify query "Next.js app scaffold layout page"` | No ("No matching nodes found") | — | Crear |
| CI y sensores | `graphify query "CI workflow lint tests sensors"` | No ("No matching nodes found") | — | Crear |
| Scripts de `package.json` | `graphify query "package.json scripts"` | No: solo aparecen los hooks Python de `.claude/hooks` | — | Crear |
| Exclusiones de `.gitignore` | lectura directa (no es código) | Sí: `node_modules/`, `.next/`, `coverage/` | `.gitignore` | Extender con `next-env.d.ts` y `*.tsbuildinfo` |

## 6. Diseño
- **Scaffold:** se parte de `create-next-app@16.4.6 --ts --tailwind --eslint --app --src-dir --use-npm`, generado fuera del repo, y se copian solo los archivos de T1. **No se copian** su `AGENTS.md`, su `README.md`, `public/*` ni `favicon.ico`. Tampoco se copian la fuente Geist ni los colores del CSS de ejemplo: el diseño llega con los tokens.
- **Archivos base:**
  - `next.config.ts`: los defaults del scaffold (`cacheComponents`, regla de turbopack para `@tailwindcss/turbopack`) más `agentRules: false`.
  - `src/app/globals.css`: solo `@import "tailwindcss";`.
  - `src/app/layout.tsx`: `<html lang="es">` y `metadata.title` «Megatravel».
- **Páginas:** `src/app/page.tsx` (título y 1 línea de texto) y `src/app/admin/page.tsx` (título «CMS», `export const metadata = { robots: { index: false } }`). Son Server Components síncronos, sin datos.
- **Tests:** junto a cada página (`page.test.tsx`), con `renderToStaticMarkup` de `react-dom/server` y Vitest sin config.
- **Scripts de `package.json`:**
  - `dev`, `build` y `start`: los de Next.
  - `lint`: `eslint --max-warnings 0`.
  - `typecheck`: `tsc --noEmit`.
  - `dup`: `jscpd --threshold 3 --exit-code 1 src`.
  - `knip`: `knip`.
  - `test`: `vitest run`.
  - `check`: `npm run lint && npm run typecheck && npm run dup && npm run knip && npm test`.
- **CI:** `.github/workflows/ci.yml` con 1 job `ci` en `ubuntu-latest`. Pasos: `actions/checkout@v7`, `actions/setup-node@v7` (`node-version: 24`, `cache: npm`), `npm ci`, `npm run check` y `npm run build`. Disparadores: `pull_request` a `develop` y `main`, y `push` a `develop`.
- **Mapa de código:** las páginas y rutas van en `src/app/**`. Los tests van junto al módulo (`*.test.ts(x)`).
- **Tamaño de tarea:** `package-lock.json` cuenta como archivo, pero no entra en las 400 líneas porque es generado.

## 7. Complejidad justificada
| Excepción a la constitución | Motivo | Alternativa simple descartada | ADR |
|---|---|---|---|
| (ninguna) | Las herramientas nuevas no son excepciones; se aprueban en ADR-002 | — | ADR-002 |

## 8. API (esbozo)
N/A: la 001 no crea endpoints.

## 9. UX
N/A: las páginas son esqueletos sin diseño. Los tokens y `ux.md` llegan en la 003.

## 10. Tareas
| ID | Tarea | Dueño | Tipo | Criterios | Archivos previstos | Verificación | Ola | Sensible |
|---|---|---|---|---|---|---|---|---|
| T1 | Scaffold de la app con las dependencias de ADR-002 y las de ADR-001 que usa esta spec (Next.js, React, Tailwind y TypeScript), scripts y config de ESLint | DevOps | tarea | R1, R4, R5, R6, R11 | `package.json`, `package-lock.json`, `tsconfig.json`, `next.config.ts`, `eslint.config.mjs`, `.gitignore`, `src/app/layout.tsx`, `src/app/globals.css` (8) | `npm ci`, `npm run lint`, `npm run typecheck`, `npm run dup` y `npm run build` → exit 0. R11 con `git status`. `npm run knip` → exit 0. Fallos provocados de R4 a R6 en el handoff. `npm test` aún falla (no hay tests): es lo esperado | 1 | no |
| T2 | Páginas `/` y `/admin` con sus tests | Frontend | tarea | R2, R3, R8 | `src/app/page.tsx`, `src/app/page.test.tsx`, `src/app/admin/page.tsx`, `src/app/admin/page.test.tsx` (4) | `npm test`, `npm run build` y `curl` a `/` y `/admin` (código y `noindex`). Fallo provocado de R8 en el handoff | 2 | no |
| T3 | Workflow de CI y comandos verificados en `AGENTS.md` | DevOps | tarea | R7, R9, R10, R12 | `.github/workflows/ci.yml`, `AGENTS.md` (solo «Comandos» y «Gotchas») (2) | `npm run check` y `npm run build` → exit 0, más fallos provocados de R7 y R9. Enlace al job `ci` en verde. Cada comando de R12 con su salida | 3 | no |
| T4 | Mapa de código: zona de páginas y tests | Arquitecto | tarea | — (§6, «Mapa de código») | `docs/arquitectura/mapa-de-codigo.md` (1) | Las filas «Páginas / rutas» y «Tests» apuntan a archivos que existen | 3 | no |

Drizzle, `drizzle-kit`, `pg` y `@aws-sdk/client-s3` siguen aprobados en ADR-001, pero no se instalan en esta spec: sin código que los use, `knip` (R7) falla. Los instala la spec que los usa (decisión del Board en MEG-33).

**Orden:** T1 → T2 → (T3 ‖ T4). T2 necesita las dependencias de T1. T3 necesita los tests de T2 para que `npm test` y la CI pasen. T3 y T4 no comparten archivos.

**Gotchas para T3** (van a `AGENTS.md`): `create-next-app` genera su propio `AGENTS.md`, que no se copia. `@types/node` debe seguir la mayor de Node: con `^20`, `vitest@5` no instala.
