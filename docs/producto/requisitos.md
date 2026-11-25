# Requisitos

Estado: **borrador** (2026-11-25) · pendiente de respuestas del Board (MEG-7, comentario numerado P1–P10) y de aprobación del Arquitecto.

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
| RF-08 | THE SYSTEM SHALL ofrecer una única plantilla de listado reutilizable para Bloqueos, Circuitos y cada zona. [NEEDS CLARIFICATION: P8 tipos y zonas existentes] | M | |
| RF-09 | WHEN el asesor aplique filtros THE SYSTEM SHALL mostrar solo los programas que cumplan todos los filtros activos (OR dentro de un mismo filtro, AND entre filtros). Filtros: zona, destino, origen, mes de salida, rango de fechas, promoción, naviera (si aplica) y texto libre. | M | |
| RF-10 | THE SYSTEM SHALL permitir ordenar el listado por destacados, fecha, precio ascendente/descendente y duración. | M | |
| RF-11 | WHEN el asesor aplique filtros, orden o página THE SYSTEM SHALL reflejarlos en la URL de modo que un enlace copiado reproduzca el mismo resultado. | M | |
| RF-12 | THE SYSTEM SHALL mostrar en cada tarjeta de programa: imagen, nombre, código MTPE, destino, duración, precio con moneda y condición, y chips de promoción. | M | |
| RF-13 | IF dos salidas están en monedas distintas THEN THE SYSTEM SHALL ordenar por precio agrupando por moneda y sin convertir divisas. | S | |
| RF-14 | THE SYSTEM SHALL mostrar banners en el listado en las ubicaciones definidas en el CMS (cabecera, entre resultados, final). | S | |
| RF-15 | IF el filtro no devuelve resultados THEN THE SYSTEM SHALL mostrar un mensaje comprensible y una acción para limpiar filtros. | M | |

### Detalle de programa
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-16 | THE SYSTEM SHALL mostrar en el detalle una barra de navegación fija con anclas a cada sección. | M | |
| RF-17 | THE SYSTEM SHALL mostrar las salidas del programa agrupadas por mes, con fecha, origen, precio, moneda, condición y disponibilidad vigente. | M | |
| RF-18 | IF la referencia de disponibilidad de una salida está vencida, ausente o en cero THEN THE SYSTEM SHALL no mostrar cupos para esa salida. (Validez por defecto 72 h, configurable.) | M | |
| RF-19 | THE SYSTEM SHALL mostrar las secciones: incluye / no incluye, itinerario día a día, hoteles, tarifas, suplementos, tours opcionales y condiciones. | M | |
| RF-20 | THE SYSTEM SHALL mostrar una galería de fotos de pasajeros únicamente de las fotos con consentimiento registrado. [NEEDS CLARIFICATION: P4 proceso de consentimiento] | S | |
| RF-21 | WHEN el asesor pulse «Reservar» en una salida THE SYSTEM SHALL llevarlo al enlace de Meganet de esa salida. | M | |
| RF-22 | WHEN el asesor pulse el enlace de descriptivo THE SYSTEM SHALL abrir el enlace externo configurado (Café Megatravel u otro). | S | |
| RF-23 | WHEN una salida alcance su fecha de corte THE SYSTEM SHALL dejar de publicarla. (Corte = fecha de salida − días de anticipación, 00:00 America/Lima.) [NEEDS CLARIFICATION: P9 confirmar que se mantiene] | M | |
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
| RF-34 | THE SYSTEM SHALL permitir subir una foto de pasajero solo si se registra su consentimiento y permitir retirarla desde el CMS. [NEEDS CLARIFICATION: P4] | M | |
| RF-35 | THE SYSTEM SHALL no permitir borrar salidas por el acceso normal; para dejar de mostrarlas se retiran con motivo. | S | |

### CMS: roles y vista previa
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-36 | THE SYSTEM SHALL exigir autenticación para todo el CMS. | M | |
| RF-37 | THE SYSTEM SHALL ofrecer al menos los roles Editor (gestiona contenido) y Administrador (además, cuentas, roles y configuración). [NEEDS CLARIFICATION: P1 roles adicionales y quién publica] | M | |
| RF-38 | IF un usuario sin rol suficiente intenta una acción THEN THE SYSTEM SHALL rechazarla en el servidor, no solo ocultar el control. | M | |
| RF-39 | WHEN el editor solicite vista previa THE SYSTEM SHALL mostrar el programa, listado o home tal como se vería publicado, incluyendo cambios aún no guardados o en borrador. | M | |
| RF-40 | THE SYSTEM SHALL restringir la vista previa a usuarios autenticados y excluirla de los buscadores. | M | |
| RF-41 | THE SYSTEM SHALL mantener estados borrador, publicado y retirado; una salida retirada solo se reactiva tras confirmar revisión. [NEEDS CLARIFICATION: P9 si hay paso de aprobación] | M | |
| RF-42 | THE SYSTEM SHALL permitir al Administrador crear, desactivar y cambiar el rol de cuentas. | M | |
| RF-43 | THE SYSTEM SHALL tener un diseño propio del CMS coherente con la marca. | S | |

### Acceso, SEO y migración
| ID | Requisito | Prioridad | Spec |
|---|---|---|---|
| RF-44 | THE SYSTEM SHALL servir las páginas públicas sin login. [NEEDS CLARIFICATION: P2 público vs. login de asesor] | M | |
| RF-45 | WHEN se solicite una URL actual que cambie en la nueva web THE SYSTEM SHALL redirigir de forma permanente a su equivalente. [NEEDS CLARIFICATION: P6 URLs a conservar] | M | |
| RF-46 | THE SYSTEM SHALL ofrecer título, descripción, URL canónica y datos estructurados por página pública, y sitemap. | S | |
| RF-47 | THE SYSTEM SHALL cargar los programas y salidas actuales (anexo A) mediante migración sobre exportaciones, sin conectarse a la base de producción. | M | |
| RF-48 | THE SYSTEM SHALL presentar todo el contenido y la interfaz en español. [NEEDS CLARIFICATION: P7 idiomas] | M | |

## No funcionales
| ID | Requisito | Medición |
|---|---|---|
| RNF-01 | THE SYSTEM SHALL cumplir Core Web Vitals en verde en móvil para home, listado y detalle. | LCP, INP, CLS en umbrales «buenos»; método y umbrales exactos en ADR de calidad (spec 001). |
| RNF-02 | THE SYSTEM SHALL funcionar en móvil desde 360 px y con teclado, con formularios etiquetados y errores comprensibles. | Revisión manual + auditoría de accesibilidad sin fallos críticos. |
| RNF-03 | THE SYSTEM SHALL tomar todos los valores visuales de tokens de diseño. | Revisión de código; sin valores literales de color/espaciado. |
| RNF-04 | THE SYSTEM SHALL permitir editar todo contenido visible desde el CMS, sin contenido escrito en el código. | Revisión: ningún texto comercial en el código. |
| RNF-05 | THE SYSTEM SHALL permitir que un editor publique un programa completo en un tiempo objetivo. | [NEEDS CLARIFICATION: P5 meta en minutos] |
| RNF-06 | THE SYSTEM SHALL no incluir secretos en el repositorio y documentar la configuración en `.env.example`. | Escaneo de secretos en CI. |
| RNF-07 | THE SYSTEM SHALL validar en el servidor toda entrada externa y autorizar explícitamente cada acción. | Tests de autorización por rol. |
| RNF-08 | THE SYSTEM SHALL almacenar datos personales mínimos, no escribirlos en logs y permitir borrarlos. | Revisión de logs; prueba de retirada de foto. |
| RNF-09 | THE SYSTEM SHALL almacenar las contraseñas de las cuentas del CMS con hash seguro y caducar las sesiones. | Revisión de seguridad. |
| RNF-10 | THE SYSTEM SHALL exponer públicamente solo los campos comerciales permitidos, nunca campos de gestión (motivos, notas, usuarios, historial). | Test de contrato de la respuesta pública. |
| RNF-11 | IF el origen de datos falla THEN THE SYSTEM SHALL mostrar un error recuperable sin exponer detalles internos. | Prueba con origen caído. |
| RNF-12 | THE SYSTEM SHALL funcionar dentro del presupuesto de hosting acordado. | [NEEDS CLARIFICATION: P3 hosting y tope mensual] |
| RNF-13 | THE SYSTEM SHALL tener copias de seguridad restaurables de la base y las imágenes. | Restauración de prueba documentada. |
| RNF-14 | THE SYSTEM SHALL mantener la web actual en producción sin cambios hasta el lanzamiento. | Ningún cambio en el repo ni la base de bloqueosweb. |

## Comportamiento que no debe cambiar
- Las reservas siguen en Meganet; la web solo enlaza (Constitución art. 19).
- La web actual (bloqueosmegatravel.pe) sigue en producción sin cambios hasta el lanzamiento.
- Reglas de negocio de salidas que hoy funcionan: corte a 00:00 de Lima con anticipación configurable (30 días por defecto), precio > 0 para publicar, enlaces HTTPS, no volver de publicado/retirado a borrador, retirado requiere confirmación de revisión para reactivar, sin conversión USD/PEN.
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
| `/` | Catálogo único con filtros y paginación (12 por página) | Pública | Pasa a ser home + listado; conservar o redirigir. [NEEDS CLARIFICATION: P6] |
| `/?q=&zones=&destinations=&origins=&months=&programs=&promotions=&cruiseLines=&from=&to=&sort=&page=` | Filtros del catálogo en la URL | Pública | Redirigir a la plantilla de listado equivalente. [NEEDS CLARIFICATION: P6] |
| `/api/public/catalog` | JSON del catálogo vigente | Pública | Fuera del alcance de requisitos; decide el Arquitecto si se mantiene. |
| `/admin` y subrutas | Panel del CMS actual | Editor/Admin | Sustituido por el CMS nuevo. |
| `/preview/[id]` | Vista previa privada, no indexable | Editor | Equivalente en RF-39/RF-40. |
| `/api/health`, `/api/cron/retire` | Salud y retiro programado | Servicio | Necesidad funcional cubierta por RF-23 y RNF-13. |
| `/megatravel-default.svg`, `/favicon-megatravel.png`, `/flyers/*` | Recursos públicos | Pública | Revisar si algún enlace externo apunta a ellos. |
| Enlaces salientes | Meganet (reserva), Café Megatravel (descriptivo), WhatsApp / contacto | — | Se mantienen por salida (RF-21, RF-22). |

### A.4 Puntos del inventario que quedan abiertos
- URLs externas que apuntan al sitio actual (correos, redes, Meganet, Café): P6.
- El inventario describe un catálogo de salidas, no la home ni los programas ricos que se piden: ese contenido (hero, beneficios, itinerarios, hoteles, tarifas, etc.) se crea de cero o se obtiene de otra fuente. [NEEDS CLARIFICATION: ¿existe fuente para migrar ese contenido rico o se carga a mano?]
