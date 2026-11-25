"""SessionStart: recuerda las reglas clave al iniciar, tras /clear o tras compactar.

Lo que imprime se añade al contexto. Si la sesión viene de una compactación
(source == "compact"), pide escribir el handoff y cerrar el run.
"""
import os
import subprocess

from _common import PROJECT_DIR, load_config, ok, read_event

event = read_event()
cfg = load_config()
lines = []

msg = cfg.get("session_start_message", "")
if msg:
    lines.append(msg)

try:
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=PROJECT_DIR, capture_output=True, text=True, timeout=5
    ).stdout.strip()
    if branch:
        lines.append(f"Rama actual: {branch}.")
except (OSError, subprocess.SubprocessError):
    pass

task = os.environ.get("PAPERCLIP_TASK_ID")
if task:
    lines.append(f"Issue de Paperclip: {task}. Su descripción es tu contrato.")

if event.get("source") == "compact":
    lines.append(
        "ATENCIÓN: esta sesión se acaba de compactar (superaste el 50 % de la ventana de trabajo). "
        "No sigas implementando: escribe el handoff con la skill handoff, indica 'Contexto: compactado' "
        "y termina el run. El Orquestador partirá lo pendiente en un issue nuevo."
    )

if lines:
    print("\n".join(lines))
ok()
