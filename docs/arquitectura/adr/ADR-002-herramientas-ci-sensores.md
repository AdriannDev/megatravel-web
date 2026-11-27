# ADR-002 · Herramientas de desarrollo, CI y sensores

- Estado: **aceptado** (Board, revisión de MEG-31)
- Fecha: 2026-11-27
- Issue: MEG-31 (spec 001 · Fundaciones)
- Depende de: ADR-001

## Contexto
ADR-001 aprueba solo las dependencias de la app y deja las herramientas de CI y los sensores para un ADR propio. La constitución (art. 9) exige lint, tipos, tests, duplicación y código muerto antes de integrar. La spec 001 necesita esas piezas, más lo que el scaffold de Next.js 16.4 instala por defecto y ADR-001 no nombra.

## Decisión
| Pieza | Elección | Motivo |
|---|---|---|
| Runtime | **Node 24 LTS** (`engines.node: "24.x"` en `package.json`) | Es el Node del entorno de los agentes (24.22.3), donde se verifican los comandos. Soporte hasta 2028-04-30. Next 16.4.6 exige ≥ 20.9 |
| Gestor de paquetes | **npm** (viene con Node) · lockfile `package-lock.json` | No añade herramienta. pnpm o yarn exigirían corepack sin un motivo concreto |
| Tipos | `@types/node@^24`, `@types/react@^19`, `@types/react-dom@^19` | Los instala `create-next-app`. `@types/node` sigue la mayor de Node: con `^20` (el default del scaffold) `vitest@5` falla por peer dependency (comprobado) |
| Tailwind v4 | `@tailwindcss/turbopack` (tailwindlabs) | Es el cargador que configura `create-next-app@16.4.6` en `next.config.ts`. Evita `postcss` y `postcss.config.mjs` |
| Lint | `eslint@^9` + `eslint-config-next@16.4.6` (`core-web-vitals` + `typescript`) | El scaffold fija `^9`. `next lint` ya no existe en Next 16. eslint 10 no está confirmado con `eslint-config-next` |
| Tipos (sensor) | `typescript@^5` (ya en ADR-001), `tsc --noEmit` | TS 7 no está confirmado con Next 16.4 |
| Tests | `vitest@^5`, sin config ni plugins | Renderiza componentes con `react-dom/server` en entorno node, sin `@vitejs/plugin-react` ni jsdom (comprobado). Testing Library y jsdom, con su ADR, cuando una spec necesite interacción |
| Duplicación | `jscpd@^5` sobre `src`, umbral **3 %** | Sensor de la constitución. El umbral se fija ahora: subirlo después requiere otro ADR |
| Código muerto | `knip@^6`, sin config | Detecta Next y Vitest por sus plugins. Funciona sin config (comprobado) |
| CI | **GitHub Actions** con `actions/checkout@v7` y `actions/setup-node@v7` | El repo ya está en GitHub y es público: los runners estándar son gratis |
| Grafo | Se versionan `graphify-out/graph.json` y `GRAPH_REPORT.md`; `graphify-out/cache/` sigue ignorado | Ya es la práctica del repo. Así, un agente recién llegado puede hacer `graphify query` sin reconstruir |

**Configuración de Next que fija este ADR:** `agentRules: false` en `next.config.ts`. Sin esto, `next dev` añade o restaura un bloque propio en `AGENTS.md` cuando detecta un agente (`node_modules/next/dist/server/lib/start-server.js`, comprobado). `AGENTS.md` es la fuente única de reglas, la mantiene el Arquitecto y tiene un máximo de 150 líneas.

## Alternativas descartadas
- **Prettier:** ESLint basta para la 001. Se añadiría con su ADR si la revisión detecta ruido de formato.
- **Playwright (E2E):** no hay flujos que probar en la 001. Entra con la primera spec de vistas públicas (003), con su ADR.
- **dependency-cruiser (capas):** todavía no hay capas. Entra cuando exista acceso a datos (spec 001b o 002).
- **pnpm / Turborepo:** solo hay 1 app y ningún requisito los pide.
- **`@tailwindcss/postcss`:** es válido. Se descarta porque añade `postcss` y un archivo de config que el scaffold actual no usa.

## Consecuencias
- Dependencias de desarrollo nuevas: las de la tabla. Cualquier otra necesita su ADR.
- CI: 1 workflow con los mismos scripts de `package.json` que se usan en local. No lleva `continue-on-error` ni `--passWithNoTests`.
- Subir la mayor de Node (a la 26 LTS) es un cambio de este ADR: va en `engines`, en `@types/node` y en el workflow a la vez.

## Fuentes (consultadas el 2026-11-27)
- Versiones en el registro de npm (`npm view`): next 16.4.6, eslint-config-next 16.4.6 (peer `eslint >=9`), vitest 5.1.2, knip 6.49.0, jscpd 5.4.3, @tailwindcss/turbopack 4.3.x (repo tailwindlabs/tailwindcss).
- Calendario de Node: https://raw.githubusercontent.com/nodejs/Release/main/schedule.json (v24: mantenimiento desde 2026-10-20, fin el 2028-04-30).
- Últimas versiones de las acciones: `gh api repos/actions/checkout/releases/latest` → v7.0.1 · `actions/setup-node` → v7.1.0.
- Facturación de Actions: https://docs.github.com/en/billing/concepts/product-billing/github-actions («Standard GitHub-hosted runners in public repositories» son gratis).
- Prueba local con `create-next-app@16.4.6` en `/tmp`, fuera del repo: build con `/` y `/admin`, `tsc`, `eslint`, `vitest` (render con `react-dom/server`), `knip` y `jscpd`, todos con exit 0.
