# Requisitos

Estado: **listo para revisión** (v2, 2026-11-25) · respuestas del Board a P1–P10 incorporadas (MEG-7); pendiente de aprobación del Arquitecto. Quedan abiertos los `[NEEDS CLARIFICATION]` indicados.

Formato EARS. Cada requisito tiene un ID estable (`RF-xx` funcional, `RNF-xx` no funcional) que las specs referencian. Prioridad MoSCoW: M = Must, S = Should, C = Could, W = Won't (v1).

| Patrón | Plantilla |
|---|---|
| Ubicuo | THE SYSTEM SHALL … |
| Evento | WHEN <disparador> THE SYSTEM SHALL … |
| Estado | WHILE <estado> THE SYSTEM SHALL … |
| No deseado | IF <condición> THEN THE SYSTEM SHALL … |

Los requisitos describen el qué; el stack y el cómo los decide el Arquitecto (ADR-001). `[NEEDS CLARIFICATION: Pn]` remite a la pregunta n del comentario al Board en MEG-7.

## Funcionales

### Home
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-01 | THE SYSTEM SHALL mostrar en la home un hero con video o imagen configurable desde el CMS. | M | |
| RF-02 | THE SYSTEM SHALL mostrar en la home un bloque de beneficios editable desde el CMS. | M | |
| RF-03 | THE SYSTEM SHALL ofrecer en la home un buscador que permita elegir una zona y llevar al listado filtrado por ella. | M | |
| RF-04 | THE SYSTEM SHALL mostrar en la home carruseles de programas cuya selección y orden se definen en el CMS. | M | |
| RF-05 | THE SYSTEM SHALL mostrar en la home bloques editoriales (imagen, texto, enlace) editables desde el CMS. | S | |
| RF-06 | WHILE un banner con contador tenga fecha de fin futura THE SYSTEM SHALL mostrar el tiempo restante hasta esa fecha. | S | |
| RF-07 | WHEN un banner supere su fecha de fin THE SYSTEM SHALL dejar de mostrarlo sin intervención del editor. (Los periodos incluyen el inicio y excluyen el fin, como hoy.) | M | |

### Plantilla de listado
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-08 | THE SYSTEM SHALL ofrecer una única plantilla de listado reutilizable para Bloqueos, Circuitos (con subtipos «no incluye vuelo» / «incluye vuelo») y cada zona. | M | |
| RF-08b | THE SYSTEM SHALL ofrecer inicialmente las zonas Europa, Asia, Medio Oriente, Estados Unidos, Centro América, Caribe, Sur América, África y Cruceros, y permitir agregarlas, editarlas y desactivarlas desde el CMS. | M | |
| RF-09 | WHEN el asesor aplique filtros THE SYSTEM SHALL mostrar solo los programas que cumplan todos los filtros activos (OR dentro de un mismo filtro, AND entre filtros). Filtros: zona, destino, origen, mes de salida, rango de fechas, promoción, naviera (si aplica) y texto libre. | M | |
| RF-10 | THE SYSTEM SHALL permitir ordenar el listado por destacados, fecha, precio ascendente/descendente y duración. | M | |
| RF-11 | WHEN el asesor aplique filtros, orden o página THE SYSTEM SHALL reflejarlos en la URL de modo que un enlace copiado reproduzca el mismo resultado. | M | |
| RF-12 | THE SYSTEM SHALL mostrar en cada tarjeta de programa: imagen, nombre, código MTPE, destino, duración, precio con moneda y condición, y chips de promoción. | M | |
| RF-13 | THE SYSTEM SHALL expresar todos los precios en USD, sin conversión de divisas. | M | |
| RF-14 | THE SYSTEM SHALL mostrar banners en el listado en las ubicaciones definidas en el CMS (cabecera, entre resultados, final). | S | |
| RF-15 | IF el filtro no devuelve resultados THEN THE SYSTEM SHALL mostrar un mensaje comprensible y una acción para limpiar filtros. | M | |

### Detalle de programa
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-16 | THE SYSTEM SHALL mostrar en el detalle una barra de navegación fija con anclas a cada sección. | M | |
| RF-17 | THE SYSTEM SHALL mostrar las salidas del programa agrupadas por mes, con fecha, origen, precio, moneda, condición y disponibilidad vigente. | M | |
| RF-18 | IF la referencia de disponibilidad de una salida está vencida, ausente o en cero THEN THE SYSTEM SHALL no mostrar cupos para esa salida. (Validez por defecto 72 h, configurable.) | M | |
| RF-19 | THE SYSTEM SHALL mostrar las secciones: incluye / no incluye, itinerario día a día, hoteles, tarifas, suplementos, tours opcionales y condiciones. | M | |
| RF-20 | THE SYSTEM SHALL mostrar una galería de fotos de pasajeros que estén publicadas en el programa. | S | |
| RF-21 | WHEN el asesor pulse «Reservar» en una salida THE SYSTEM SHALL llevarlo al enlace de Meganet de esa salida. | M | |
| RF-22 | WHEN el asesor pulse el enlace de descriptivo THE SYSTEM SHALL abrir el enlace externo configurado (Café Megatravel u otro). | S | |
| RF-23 | WHEN una salida alcance su fecha de corte THE SYSTEM SHALL dejar de publicarla. (Corte = fecha de salida − días de anticipación, 00:00 America/Lima.) [NEEDS CLARIFICATION: el Board no confirmó si se mantiene el retiro automático] | M | |
| RF-24 | IF un programa no tiene salidas vigentes THEN THE SYSTEM SHALL indicarlo y ofrecer enlace de contacto con un asesor de Megatravel. | S | |
| RF-25 | THE SYSTEM SHALL no procesar reservas ni pagos. | M | |

### CMS: contenido
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-26 | THE SYSTEM SHALL permitir al editor crear y editar un programa completo (datos comerciales, itinerario, hoteles, incluye/no incluye, tarifas, suplementos, tours opcionales, condiciones, imágenes) sin intervención de desarrollo. | M | |
| RF-27 | THE SYSTEM SHALL permitir crear, editar, duplicar y retirar salidas de un programa, con fecha, origen, precio, moneda, condición, cupos y promociones. | M | |
| RF-28 | THE SYSTEM SHALL permitir gestionar banners (imagen, texto alternativo, enlace, periodo, orden, ubicación, contador opcional). | M | |
| RF-29 | THE SYSTEM SHALL permitir configurar la home (hero, beneficios, carruseles, bloques editoriales). | M | |
| RF-30 | THE SYSTEM SHALL permitir gestionar promociones, destinos, orígenes, zonas y navieras como referencias reutilizables. | M | |
| RF-31 | WHEN el editor guarde un programa o salida THE SYSTEM SHALL registrar quién cambió qué y cuándo (historial no editable). | M | |
| RF-32 | IF un editor intenta publicar con datos obligatorios incompletos o inválidos (precio ≤ 0, enlaces no HTTPS, fecha pasada, etc.) THEN THE SYSTEM SHALL impedir la publicación y explicar cada error. | M | |
| RF-33 | THE SYSTEM SHALL permitir importar salidas desde CSV con validación previa por fila y reporte de errores antes de escribir. | S | |
| RF-34 | THE SYSTEM SHALL permitir subir fotos de pasajeros como contenido normal, sin exigir registro de consentimiento (se gestiona internamente), y permitir retirarlas desde el CMS. | M | |
| RF-49 | WHEN el editor suba un documento Word de un programa THE SYSTEM SHALL extraer sus datos y precargar el formulario del programa para que el editor los revise antes de guardar. [NEEDS CLARIFICATION: factibilidad y estructura del Word; la evalúa el Arquitecto] | C | |
| RF-35 | THE SYSTEM SHALL no permitir borrar salidas por el acceso normal; para dejar de mostrarlas se retiran con motivo. | S | |

### CMS: roles y vista previa
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-36 | THE SYSTEM SHALL exigir autenticación para todo el CMS. | M | |
| RF-37 | THE SYSTEM SHALL ofrecer los roles Editor (gestiona contenido), Marketing (sube banners, videos y contenido visual) y Administrador (además, cuentas, roles y configuración). Los tres roles pueden publicar cambios. | M | |
| RF-38 | IF un usuario sin rol suficiente intenta una acción THEN THE SYSTEM SHALL rechazarla en el servidor, no solo ocultar el control. | M | |
| RF-39 | WHEN el editor solicite vista previa THE SYSTEM SHALL mostrar el programa, listado o home tal como se vería publicado, incluyendo cambios aún no guardados o en borrador. | M | |
| RF-40 | THE SYSTEM SHALL restringir la vista previa a usuarios autenticados y excluirla de los buscadores. | M | |
| RF-41 | THE SYSTEM SHALL permitir publicar directamente tras llenar el contenido o tras la vista previa, sin paso obligatorio de borrador ni aprobación, y permitir editar o retirar lo publicado. | M | |
| RF-41b | THE SYSTEM SHALL permitir guardar un programa o salida sin publicar. [NEEDS CLARIFICATION: el Board no necesita borrador; confirmar si se conserva como opción y si la reactivación de retirados sigue exigiendo confirmación de revisión] | C | |
| RF-42 | THE SYSTEM SHALL permitir al Administrador crear, desactivar y cambiar el rol de cuentas. | M | |
| RF-43 | THE SYSTEM SHALL tener un diseño propio del CMS coherente con la marca. | S | |

### Acceso, SEO y migración
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-44 | THE SYSTEM SHALL servir las páginas públicas sin login ni cuentas de visitantes o asesores. | M | |
| RF-45 | WHEN se solicite una URL actual que cambie en la nueva web THE SYSTEM SHALL redirigir de forma permanente a su equivalente. | M | |
| RF-45b | THE SYSTEM SHALL conservar los parámetros de filtro actuales del catálogo siempre que ello no afecte el diseño nuevo. | S | |
| RF-45c | WHEN se solicite una URL de otras webs de Megatravel que apuntaban a bloqueosmegatravel.pe THE SYSTEM SHALL llevar al home de Bloqueos. | M | |
| RF-46 | THE SYSTEM SHALL ofrecer título, descripción, URL canónica y datos estructurados por página pública, y sitemap. | S | |
| RF-47 | THE SYSTEM SHALL cargar los programas y salidas actuales (anexo A) mediante migración sobre exportaciones, sin conectarse a la base de producción. | M | |
| RF-48 | THE SYSTEM SHALL presentar todo el contenido y la interfaz solo en español. | M | |

## No funcionales
| ID | Requisito | Medición |
|---|---|---|
| RNF-01 | THE SYSTEM SHALL ser rápido en móvil para home, listado y detalle, con un mínimo de 80 puntos de rendimiento y el objetivo de superarlo. | Puntuación de rendimiento en móvil ≥ 80; Core Web Vitals en verde como objetivo; método exacto en ADR de calidad (spec 001). |
| RNF-02 | THE SYSTEM SHALL funcionar en móvil desde 360 px y con teclado, con formularios etiquetados y errores comprensibles. | Revisión manual + auditoría de accesibilidad sin fallos críticos. |
| RNF-03 | THE SYSTEM SHALL tomar todos los valores visuales de tokens de diseño. | Revisión de código; sin valores literales de color/espaciado. |
| RNF-04 | THE SYSTEM SHALL permitir editar todo contenido visible desde el CMS, sin contenido escrito en el código. | Revisión: ningún texto comercial en el código. |
| RNF-05 | THE SYSTEM SHALL minimizar el esfuerzo para publicar un programa completo (ver RF-49). | Meta en minutos no definida. [NEEDS CLARIFICATION: ¿valor objetivo? Opcional] |
| RNF-06 | THE SYSTEM SHALL no incluir secretos en el repositorio y documentar la configuración en `.env.example`. | Escaneo de secretos en CI. |
| RNF-07 | THE SYSTEM SHALL validar en el servidor toda entrada externa y autorizar explícitamente cada acción. | Tests de autorización por rol. |
| RNF-08 | THE SYSTEM SHALL almacenar datos personales mínimos (cuentas del CMS), no escribirlos en logs y permitir borrarlos. | Revisión de logs; prueba de retirada de foto. |
| RNF-09 | THE SYSTEM SHALL almacenar las contraseñas de las cuentas del CMS con hash seguro y caducar las sesiones. | Revisión de seguridad. |
| RNF-10 | THE SYSTEM SHALL exponer públicamente solo los campos comerciales permitidos, nunca campos de gestión (motivos, notas, usuarios, historial). | Test de contrato de la respuesta pública. |
| RNF-11 | IF el origen de datos falla THEN THE SYSTEM SHALL mostrar un error recuperable sin exponer detalles internos. | Prueba con origen caído. |
| RNF-12 | THE SYSTEM SHALL operar con un costo de hosting óptimo, sin tope fijo. Se prefiere Railway si encaja; el Arquitecto puede recomendar alternativas. | Estimación de costo mensual en ADR-001. |
| RNF-13 | THE SYSTEM SHALL tener copias de seguridad restaurables de la base y las imágenes. | Restauración de prueba documentada. |
| RNF-14 | THE SYSTEM SHALL mantener la web actual en producción sin cambios hasta el lanzamiento. | Ningún cambio en el repo ni la base de bloqueosweb. |

## Comportamiento que no debe cambiar
- Las reservas siguen en Meganet; la web solo enlaza (Constitución art. 19).
- La web actual (bloqueosmegatravel.pe) sigue en producción sin cambios hasta el lanzamiento.
- Reglas de negocio de salidas que hoy funcionan: corte a 00:00 de Lima con anticipación configurable (30 días por defecto), precio > 0 para publicar, enlaces HTTPS, no volver de publicado/retirado a borrador, retirado requiere confirmación de revisión para reactivar, sin conversión de divisas (ahora solo USD).
- Los cupos solo se muestran con referencia vigente (72 h por defecto).
- Fecha de salida como fecha de calendario `AAAA-MM-DD` sin reinterpretación por huso horario.

## Anexo A · Inventario de contenido y URLs actuales

Fuente (solo lectura): `bloqueosweb/docs/datos-y-api.md` y `docs/arquitectura.md`, leídos el 2026-11-25. Es el estado documentado, no una auditoría del sitio en producción.

### A.1 Entidades de contenido
| Entidad (slug actual) | Contenido | Observaciones para la migración |
|---|---|---|
| Programas (`programs`) | `program`, `mtpe` (único, mayúsculas), destino, zona, días, noches, naviera, flyer, enlaces de reserva y descriptivo | Contenido comercial compartido por todas las salidas. **No existen aún** itinerario, hoteles, incluye/no incluye, tarifas, suplementos, tours opcionales ni fotos de pasajeros: son contenido nuevo (RF-19, RF-20). |
| Salidas (`departures`) | Una fecha de viaje por programa y origen: fecha, precio, moneda (USD/PEN), condición, cupos, promociones, prioridad, días de anticipación, estado | Identidad por MTPE + origen + fecha; `stableId` estable. Estados `draft`/`published`/`withdrawn`. |
| Imágenes (`media`) | Archivo, texto alternativo, URL de origen | Hoy en Cloudflare R2; flyers con respaldo `/megatravel-default.svg`. |
| Promociones (`campaigns`) | Nombre, etiqueta, identificador, periodo | Periodo con inicio incluido y fin excluido. |
| Banners (`banners`) | Imagen, enlace, periodo, orden, ubicación `hero` / `between-results` / `catalog-end` | Los antiguos sin ubicación son `hero`. |
| Destinos, Orígenes, Navieras | Listas de referencia por nombre | Reutilizables. |
| Historial (`audit-log`) | Cambios y transiciones de estado | Privado; decidir si se migra o se archiva. |
| Usuarios (`users`) | Cuentas y roles (Editor, Administrador) | No migrar contraseñas; recrear cuentas. |
| Configuración (`settings`) | Contacto (URL y etiqueta), validez de cupos (72 h) | Global único. |

### A.2 Volumen de referencia
Corte inicial de la preparación desde el Excel: 411 filas, 233 publicables, 10 borradores, 168 históricos. Es una foto inicial, no el conteo vigente; el conteo real se pide a Producto antes de migrar. Fuente original: Excel con columnas A–T (mes, MTPE, programa, días/noches, salida, zona, origen, destino, enlaces Meganet y Café, precio, foto, crucero, promociones, días de retiro, retiro histórico y motivo).

### A.3 URLs y rutas actuales
| URL / ruta | Función | Visibilidad | Propuesta |
|---|---|---|---|
| `/` | Catálogo único con filtros y paginación (12 por página) | Pública | Pasa a ser home + listado. [NEEDS CLARIFICATION: cómo conviven `/` como home y como catálogo con parámetros; decide el Arquitecto con el Board] |
| `/?q=&zones=&destinations=&origins=&months=&programs=&promotions=&cruiseLines=&from=&to=&sort=&page=` | Filtros del catálogo en la URL | Pública | Conservar los parámetros si no afecta (P6); si no, redirigir al listado equivalente. |
| `/api/public/catalog` | JSON del catálogo vigente | Pública | Fuera del alcance de requisitos; decide el Arquitecto si se mantiene. |
| `/admin` y subrutas | Panel del CMS actual | Editor/Admin | Sustituido por el CMS nuevo. |
| `/preview/[id]` | Vista previa privada, no indexable | Editor | Equivalente en RF-39/RF-40. |
| `/api/health`, `/api/cron/retire` | Salud y retiro programado | Servicio | Necesidad funcional cubierta por RF-23 y RNF-13. |
| `/megatravel-default.svg`, `/favicon-megatravel.png`, `/flyers/*` | Recursos públicos | Pública | Revisar si algún enlace externo apunta a ellos. |
| Enlaces salientes | Meganet (reserva), Café Megatravel (descriptivo), WhatsApp / contacto | — | Se mantienen por salida (RF-21, RF-22). |

### A.4 Puntos del inventario que quedan abiertos
- URLs externas (P6): el Board indicó que las otras webs siempre redirigirán al home de Bloqueos; no se conserva ninguna URL externa específica. Falta confirmar las de `/flyers/*` y recursos públicos.
- Moneda: el inventario tiene salidas en USD y PEN; el Board indicó solo USD. [NEEDS CLARIFICATION: ¿qué pasa con las salidas actuales en PEN?]
- El inventario describe un catálogo de salidas, no la home ni los programas ricos que se piden: ese contenido (hero, beneficios, itinerarios, hoteles, tarifas, etc.) se crea de cero o se obtiene de otra fuente. [NEEDS CLARIFICATION: ¿existe fuente para migrar ese contenido rico o se carga a mano?]
