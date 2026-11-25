"""Stop: ejecuta los sensores rápidos antes de que el agente termine.

Si `stop_check_command` (hooks.config.json) está vacío, no hace nada: se rellena
en la spec 001 cuando el Arquitecto fije el stack. Si el comando falla, sale con
código 2 y Claude ve la salida para corregir antes de terminar. Para evitar
bucles, si el evento indica stop_hook_active (ya se reintentó una vez), deja
terminar y el fallo queda para el revisor.
"""
import subprocess
import sys

from _common import PROJECT_DIR, load_config, ok, read_event

event = read_event()
if event.get("stop_hook_active"):
    ok()

command = load_config().get("stop_check_command", "")
if not command:
    ok()

try:
    result = subprocess.run(command, shell=True, cwd=PROJECT_DIR, capture_output=True, text=True, timeout=600)
except subprocess.TimeoutExpired:
    ok()

if result.returncode != 0:
    output = (result.stdout + result.stderr)[-3000:]
    sys.stderr.write(
        f"Los sensores rápidos fallan ({command}). Corrige antes de terminar o explica el fallo en el handoff.\n{output}\n"
    )
    sys.exit(2)
ok()
