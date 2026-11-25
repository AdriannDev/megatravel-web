"""PreCompact: indica al resumen qué conservar.

Claude Code usa el stdout de este hook como instrucciones adicionales para la
compactación. En el marco, compactar significa que la tarea superó el techo de
contexto (50 % de la ventana de trabajo): se conserva lo imprescindible para
escribir el handoff y cerrar el run.
"""
from _common import ok

print(
    "Conserva literalmente: (1) el contrato del issue: objetivo, criterios de aceptación, "
    "archivos permitidos, presupuesto y comandos de verificación; (2) la spec y la tarea activas "
    "(ruta y sección); (3) la lista de archivos modificados; (4) los comandos ejecutados y su "
    "resultado; (5) lo pendiente. Descarta salidas largas de herramientas y lecturas de archivos. "
    "Tras compactar: escribe el handoff (skill handoff) indicando 'Contexto: compactado' y termina el run."
)
ok()
