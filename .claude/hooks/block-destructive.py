"""PreToolUse (Bash): bloquea comandos destructivos y cualquier intento de tocar main.

Origen: _framework v1.0 (patrones por subcadena). Ampliado para el marco de
equipo: expresiones regulares de `protected_branch_regexes` (push, checkout o
update-ref sobre main, uso de ALLOW_MAIN_UPDATE, cambio de core.hooksPath).
Configuración en hooks.config.json.
"""
import re

from _common import block, load_config, ok, read_event

event = read_event()
command = str(event.get("tool_input", {}).get("command", ""))
if not command:
    ok()

cfg = load_config()
lowered = command.lower()
for pattern in cfg["destructive_patterns"]:
    if pattern.lower() in lowered:
        block(f"el comando contiene '{pattern}'. Si es intencional, pide al humano que lo ejecute.")

for regex in cfg.get("protected_branch_regexes", []):
    if re.search(regex, command, flags=re.IGNORECASE):
        block(
            "main solo lo actualiza el humano tras el checkpoint CP4. Trabaja en tu rama; "
            "la integración en develop la hace DevOps."
        )
ok()
