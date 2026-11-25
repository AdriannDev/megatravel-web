# Brief · Megatravel Web

Estado: **listo para revisión** (v1, 2026-11-25). Validado por el Product Analyst contra `requisitos.md` y el inventario de bloqueosweb. Las preguntas P1–P10 se hicieron al Board en MEG-7 en un solo comentario; **sin respuesta aún**, por eso siguen marcadas `[NEEDS CLARIFICATION]` con su número. Pendiente de aprobación del Arquitecto.

## Problema
bloqueosmegatravel.pe es hoy una landing de bloqueos. Se quiere convertir en una **web de viajes para asesores de agencias de Perú**, con contenido rico por programa y un CMS hecho a medida para que el equipo de producto cree y mantenga todo sin depender de desarrollo.

## Usuarios
| Usuario | Qué necesita | Cómo lo hace hoy |
|---|---|---|
| Asesor de agencia | Encontrar programas por zona, tipo (Bloqueos, Circuitos) y fecha; ver salidas con disponibilidad, tarifas, itinerario y condiciones; ir a reservar en Meganet | Landing de bloqueos + enlaces a Meganet y Café Megatravel |
| Equipo de producto (editores) | Crear programas completos, gestionar salidas, banners y la home, con vista previa antes de publicar | CMS actual (Payload) de la web de bloqueos |
| [NEEDS CLARIFICATION P1: ¿otros roles en el CMS? p. ej. marketing para banners, aprobador de publicaciones] | | |

## Objetivo de la primera versión
1. **Home de contenido**: hero con video o imagen, beneficios, buscador con zonas, carruseles de programas, bloques editoriales y banners con contador.
2. **Plantilla de listado** reutilizable para Bloqueos, Circuitos y cada zona: filtros, chips de promoción y banners.
3. **Detalle de programa**: barra fija de navegación, salidas por mes con disponibilidad, incluye/no incluye, itinerario, hoteles, tarifas, suplementos, tours opcionales, fotos de pasajeros y condiciones.
4. **CMS a medida** con diseño propio para subir y editar contenido: programas completos, salidas, banners y home; roles; vista previa.
5. **Reservas**: siguen yendo a Meganet (enlaces); no se reserva en esta web.

## Alcance
- Incluye: lo anterior, migración de los programas y salidas actuales, rendimiento y SEO, lanzamiento en el dominio actual.
- No incluye (v1): reservas ni pagos. [NEEDS CLARIFICATION P2: ¿la web es pública o requiere login de asesor?]
- Pendiente: el Board indicó que aún falta decidir si se agregan más funcionalidades. Se añadirán como specs nuevas en el roadmap.

## Restricciones
- Repositorio nuevo; **la web actual sigue en producción sin cambios hasta el lanzamiento**.
- No se comparte la base de datos de producción; la migración trabaja sobre exportaciones.
- Stack preferido por el Board (no obligatorio): Next.js, React, Tailwind CSS, PostgreSQL y un CMS compatible que asegure rapidez y rendimiento. Decide el Arquitecto en ADR-001 tras la investigación.
- Hosting: [NEEDS CLARIFICATION P3: ¿se mantiene Railway? La web actual tiene un presupuesto de referencia de USD 20/mes.]

## Datos
- Contenido público: programas, salidas, tarifas, imágenes, banners.
- **Fotos de pasajeros**: son datos personales (imagen de personas). Requieren consentimiento registrado y forma de retirarlas. [NEEDS CLARIFICATION P4: ¿cómo se obtiene hoy el consentimiento?]
- **Cuentas del CMS**: credenciales y roles de editores → revisión de seguridad.

## Métricas de éxito
[NEEDS CLARIFICATION P5: p. ej. tiempo para publicar un programa completo, Core Web Vitals en verde en móvil, clics hacia Meganet por sesión.]

## Preguntas abiertas (para la spec 000)
- Los `[NEEDS CLARIFICATION]` de este documento.
- P6 · ¿Qué URLs actuales deben mantenerse o redirigirse (SEO)? Inventario en `requisitos.md`, anexo A.
- P7 · ¿Idiomas? ¿Solo español? Supuesto provisional: solo español.
- P8 · Tipos de programa y zonas del listado además de Bloqueos y Circuitos.
- P9 · ¿Flujo de aprobación antes de publicar o basta la vista previa?
- P10 · ¿Funcionalidades extra decididas para v1?
- Sin dueño aún: ¿existe fuente para migrar el contenido rico del detalle (itinerario, hoteles, tarifas) o se carga a mano? El inventario actual solo cubre salidas.
