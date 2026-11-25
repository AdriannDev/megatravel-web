@AGENTS.md

## Solo para Claude Code
- Los hooks de `.claude/hooks/` bloquean comandos destructivos, cambios en `main`, edición de secretos y lockfiles; si te bloquean, no busques rodeos: explica en el issue qué necesitas.
- Si una exploración va a leer muchos archivos, delégala a un subagente que devuelva un resumen (y dale la regla de graphify).
- Al compactar, el hook `PreCompact` indica qué conservar y `SessionStart` te pedirá cerrar con handoff.
