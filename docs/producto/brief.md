# Brief · Megatravel Web

Estado: **listo para revisión** (v2, 2026-11-25). Validado por el Product Analyst contra `requisitos.md` y el inventario de bloqueosweb. Las preguntas P1–P10 se hicieron al Board en MEG-7 en un solo comentario y **el Board respondió el 2026-11-25**; las respuestas están incorporadas. Lo que sigue abierto queda marcado `[NEEDS CLARIFICATION]`. Pendiente de aprobación del Arquitecto.

## Problema
bloqueosmegatravel.pe es hoy una landing de bloqueos. Se quiere convertir en una **web de viajes para asesores de agencias de Perú**, con contenido rico por programa y un CMS hecho a medida para que el equipo de producto cree y mantenga todo sin depender de desarrollo.

## Usuarios
| Usuario | Qué necesita | Cómo lo hace hoy |
|---|---|---|
| Asesor de agencia | Encontrar programas por zona, tipo (Bloqueos, Circuitos) y fecha; ver salidas con disponibilidad, tarifas, itinerario y condiciones; ir a reservar en Meganet | Landing de bloqueos + enlaces a Meganet y Café Megatravel |
| Equipo de producto (editores) | Crear programas completos, gestionar salidas, banners y la home, con vista previa antes de publicar | CMS actual (Payload) de la web de bloqueos |
| Marketing (CMS) | Subir banners, videos y contenido visual en general | Lo hace un editor |

Roles del CMS (P1): **Editor, Administrador y Marketing**. Los tres pueden publicar cambios.

## Objetivo de la primera versión
1. **Home de contenido**: hero con video o imagen, beneficios, buscador con zonas, carruseles de programas, bloques editoriales y banners con contador.
2. **Plantilla de listado** reutilizable para Bloqueos, Circuitos y cada zona: filtros, chips de promoción y banners.
3. **Detalle de programa**: barra fija de navegación, salidas por mes con disponibilidad, incluye/no incluye, itinerario, hoteles, tarifas, suplementos, tours opcionales, fotos de pasajeros y condiciones.
4. **CMS a medida** con diseño propio para subir y editar contenido: programas completos, salidas, banners y home; roles; vista previa.
5. **Reservas**: siguen yendo a Meganet (enlaces); no se reserva en esta web.

## Alcance
- Incluye: lo anterior, migración de los programas y salidas actuales, rendimiento y SEO, lanzamiento en el dominio actual.
- No incluye (v1): reservas ni pagos, ni login para visitantes o asesores: la web es **pública** (P2).
- Tipos de programa (P8): **Bloqueos** (foco de la v1) y **Circuitos** (porciones terrestres; subtipos «no incluye vuelo» e «incluye vuelo»).
- Zonas iniciales (P8): Europa, Asia, Medio Oriente, Estados Unidos, Centro América, Caribe, Sur América, África y Cruceros. El CMS debe permitir agregarlas y gestionarlas.
- Idioma y moneda (P7): solo español; moneda siempre USD.
- Funcionalidades extra (P10): aún no decididas; el producto crecerá de forma incremental con specs nuevas. El Board está generando prototipos para definir la estructura de la página.
- Pendiente: el Board indicó que aún falta decidir si se agregan más funcionalidades. Se añadirán como specs nuevas en el roadmap.

## Restricciones
- Repositorio nuevo; **la web actual sigue en producción sin cambios hasta el lanzamiento**.
- No se comparte la base de datos de producción; la migración trabaja sobre exportaciones.
- Stack preferido por el Board (no obligatorio): Next.js, React, Tailwind CSS, PostgreSQL y un CMS compatible que asegure rapidez y rendimiento. Decide el Arquitecto en ADR-001 tras la investigación.
- Hosting y presupuesto (P3): se **quita el tope** de USD 20/mes, pero se busca un costo óptimo sin gasto exagerado. Railway es preferible si encaja; el Arquitecto puede evaluar y recomendar alternativas en ADR-001.

## Datos
- Contenido público: programas, salidas, tarifas, imágenes, banners.
- **Fotos de pasajeros**: contienen imágenes de personas. Decisión del Board (P4): el consentimiento lo registra y custodia Megatravel fuera del sistema; el CMS las trata como una subida normal, sin condicionarla. Retirar una foto la elimina del almacenamiento, no solo la oculta (Constitución arts. 13 y 22).
- **Cuentas del CMS**: credenciales y roles de editores → revisión de seguridad.

## Métricas de éxito
- Rendimiento (P5): la web debe ser rápida; Core Web Vitals en verde en móvil (Constitución art. 23) en home, listado y detalle, y **80 puntos** de rendimiento como piso adicional.
- Fatiga mínima al publicar un programa. Idea del Board: **leer un documento Word** con el contenido del programa y volcar sus datos al CMS, porque hoy todo el contenido ya vive en un Word que se envía a clientes. Según el Arquitecto, solo es factible con una plantilla Word de estructura fija; se aplaza a una spec posterior (RF-49, Could). [NEEDS CLARIFICATION: ¿el Board acepta normalizar el Word a una plantilla?]
- Meta de tiempo de publicación (minutos): no definida. [NEEDS CLARIFICATION: ¿meta en minutos? Opcional]

## Preguntas abiertas (para la spec 000)
- P6 (resuelta): se mantienen los parámetros de filtro actuales si no afectan; las otras webs siempre redirigen al home de bloqueos. Resuelto por el Arquitecto: `/` es la home y `/` con parámetros redirige con 301 al listado de Bloqueos (RF-45b).
- P9 (resuelta): basta la vista previa; sin flujo de borrador/revisión obligatorio; se puede publicar directo y corregir después. Falta confirmar si se mantiene el retiro automático por fecha de corte y si reactivar un retirado exige confirmación (RF-23, RF-41b).
- Moneda: el Board indicó solo USD; hoy existen salidas en PEN. [NEEDS CLARIFICATION: ¿qué se hace con las salidas actuales en PEN?]
- Sin dueño aún: ¿existe fuente para migrar el contenido rico del detalle (itinerario, hoteles, tarifas) o se carga a mano? El inventario actual solo cubre salidas.
