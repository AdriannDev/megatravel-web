# Requisitos

Estado: aprobado por el Board (MEG-25)

Formato EARS. Cada requisito tiene un ID estable (`RF-xx` funcional, `RNF-xx` no funcional) que las specs referencian.

| Patrón | Plantilla |
|---|---|
| Ubicuo | THE SYSTEM SHALL … |
| Evento | WHEN <disparador> THE SYSTEM SHALL … |
| Estado | WHILE <estado> THE SYSTEM SHALL … |
| Opcional | WHERE <función activada> THE SYSTEM SHALL … |
| No deseado | IF <condición> THEN THE SYSTEM SHALL … |

**Parte:** `WEB` (web pública) · `CMS` · `AUTO` (automatización) · `TRANS` (transversal).
**Marcas:**
- **[PP]**: pendiente de prototipo del CMS. La capacidad está fijada; la interfaz se decide cuando llegue el prototipo.
- **[FIG]**: el inventario final se confirma contra el Figma `MEGA-TRAVEL-BLOQUEOS` (acceso de edición abierto por el Board; se hace en la 004).

Spec: número del `docs/roadmap.md`.

## Funcionales

### Web pública: listado y búsqueda
| ID | Requisito | Prioridad | Parte | Spec |
|---|---|---|---|---|
| RF-01 | THE SYSTEM SHALL mostrar los programas en cards con imagen, título, duración, zona y destino, precio «desde» y etiquetas (promoción, últimas plazas, crucero). [FIG] | Must | WEB | 003 |
| RF-02 | WHEN el cliente escribe en el buscador THE SYSTEM SHALL buscar en todo el contenido del programa: título, países, ciudades, itinerario, hoteles y descripción. | Must | WEB | 003 |
| RF-03 | THE SYSTEM SHALL ofrecer filtros combinables por destino (país), zona (Europa, Asia, Sudamérica…), fecha de salida, duración, categoría, promociones y cruceros. | Must | WEB | 003 |
| RF-04 | THE SYSTEM SHALL listar solo los programas publicados que tengan al menos una salida disponible (RF-20 a RF-22). | Must | WEB | 003 |
| RF-05 | THE SYSTEM SHALL mostrar en la portada los banners y videos promocionales publicados desde el CMS. [FIG] | Must | WEB | 005 |

### Web pública: detalle del programa
| ID | Requisito | Prioridad | Parte | Spec |
|---|---|---|---|---|
| RF-06 | THE SYSTEM SHALL mostrar los bloques fijos del detalle: título, duración, países y ciudades, itinerario día a día, salidas, tarifas, suplementos, qué incluye y qué no, hoteles, opcionales, requisitos del viaje, condiciones, galería de fotos y videos y descargas. [FIG] | Must | WEB | 004 |
| RF-07 | THE SYSTEM SHALL mostrar el collage de fotos de clientes y los programas relacionados del programa. [FIG] | Should | WEB | 004 |
| RF-08 | THE SYSTEM SHALL mostrar, además de los fijos, los bloques libres que el editor añada y ordene en cada programa (título + contenido enriquecido). | Must | WEB | 004 |
| RF-09 | IF un bloque no tiene contenido THEN THE SYSTEM SHALL ocultarlo. | Must | WEB | 004 |
| RF-10 | THE SYSTEM SHALL mostrar las tarifas en una tabla por tipo de habitación, y en cada salida su precio de referencia en habitación doble, todo en USD. | Must | WEB | 004 |
| RF-11 | THE SYSTEM SHALL mostrar como precio principal «desde» el menor precio en habitación doble entre las salidas disponibles. | Must | WEB | 002 |
| RF-12 | WHILE la disponibilidad de una salida está marcada como visible y su cupo tiene un valor mayor que 0 THE SYSTEM SHALL mostrar «Disponibilidad: N». Si el cupo está vacío, no muestra nada. | Must | WEB | 004 |
| RF-13 | THE SYSTEM SHALL mostrar la etiqueta «Últimas plazas» en las salidas que el editor marca a mano, y nunca una etiqueta «Agotado». | Must | WEB | 004 |
| RF-14 | WHEN el cliente pulsa «Cotizar ahora» THE SYSTEM SHALL abrir WhatsApp con un mensaje prellenado con el programa y, si se pulsó desde una salida, también su fecha. | Must | WEB | 004 |
| RF-15 | THE SYSTEM SHALL mostrar el email y el teléfono de contacto de la agencia. | Must | WEB | 004 |
| RF-16 | THE SYSTEM SHALL permitir compartir el programa: copiar enlace, WhatsApp y redes sociales. | Must | WEB | 004 |
| RF-17 | THE SYSTEM SHALL mostrar en «Condiciones» un resumen y un botón que abre o descarga el documento completo. | Must | WEB | 006 |

### Vigencia de salidas y programas
| ID | Requisito | Prioridad | Parte | Spec |
|---|---|---|---|---|
| RF-18 | THE SYSTEM SHALL tener estos estados de programa: borrador, programado, publicado y retirado. | Must | CMS | 002 |
| RF-19 | WHEN llega la fecha y hora programada THE SYSTEM SHALL publicar el programa sin intervención. | Must | CMS | 002 |
| RF-20 | WHEN faltan 30 días para la fecha de una salida THE SYSTEM SHALL deshabilitarla: deja de mostrarse y de cotizarse. | Must | AUTO | 002 |
| RF-21 | IF el cupo de una salida es 0 THEN THE SYSTEM SHALL ocultar esa salida. | Must | AUTO | 002 |
| RF-22 | WHEN un programa publicado se queda sin salidas disponibles THE SYSTEM SHALL retirarlo de la web automáticamente, sin borrar sus datos. | Must | AUTO | 002 |
| RF-23 | THE SYSTEM SHALL permitir a Producto retirar o volver a publicar a mano un programa o una salida. | Must | CMS | 002 |

### CMS: acceso, roles y permisos
| ID | Requisito | Prioridad | Parte | Spec |
|---|---|---|---|---|
| RF-24 | THE SYSTEM SHALL exigir inicio de sesión para entrar al CMS. La web pública no tiene cuentas. | Must | CMS | 001 |
| RF-25 | THE SYSTEM SHALL permitir al rol **Marketing** crear, editar, publicar y retirar banners, videos promocionales y flyers, sin aprobación. | Must | CMS | 002 |
| RF-26 | THE SYSTEM SHALL permitir al rol **Producto** crear, editar, publicar, programar y retirar programas con todo su detalle, salidas, tarifas y cupos, sin aprobación. | Must | CMS | 002 |
| RF-27 | THE SYSTEM SHALL permitir al rol **Administrador** todo lo de Marketing y Producto, y además gestionar usuarios y roles. | Must | CMS | 002 |
| RF-28 | IF un usuario intenta una acción fuera de su rol, o sin sesión válida THEN THE SYSTEM SHALL rechazarla en el servidor sin modificar nada. | Must | CMS | 001 |
| RF-29 | THE SYSTEM SHALL permitir al Administrador crear, desactivar y reactivar usuarios, asignarles rol y forzar el cambio de contraseña. [PP] | Must | CMS | 008 |

### CMS: programas
| ID | Requisito | Prioridad | Parte | Spec |
|---|---|---|---|---|
| RF-30 | THE SYSTEM SHALL permitir dar de alta y editar un programa con todos los campos de los bloques de RF-06 a RF-08: salidas con fecha, cupo, visibilidad del cupo, «últimas plazas» y precio por tipo de habitación; suplementos; y bloques libres ordenables. | Must | CMS | 002 |
| RF-31 | THE SYSTEM SHALL ofrecer formularios de carga pensados para el equipo, no genéricos. [PP] | Must | CMS | 009 |
| RF-32 | THE SYSTEM SHALL mostrar una vista previa del programa, tal como se verá en la web, antes de publicarlo y sin hacerlo público. [PP] | Must | CMS | 009 |
| RF-33 | IF dos editores guardan cambios sobre la misma versión de un programa THEN THE SYSTEM SHALL impedir que el segundo sobrescriba al primero sin aviso. | Must | CMS | 002 |
| RF-34 | THE SYSTEM SHALL permitir duplicar un programa existente como base de uno nuevo. [PP] | Could | CMS | 009 |
| RF-35 | THE SYSTEM SHALL permitir asignar a cada programa zona, países y ciudades, categoría, si es crucero y si está en promoción, para alimentar RF-03. | Must | CMS | 002 |

### CMS: medios y documentos
| ID | Requisito | Prioridad | Parte | Spec |
|---|---|---|---|---|
| RF-36 | THE SYSTEM SHALL permitir subir fotos y videos, y también enlazar videos de YouTube o Vimeo, tanto en la galería del programa como en el contenido promocional. | Must | CMS | 005 |
| RF-37 | THE SYSTEM SHALL permitir ordenar la galería y gestionar el collage de fotos de clientes de cada programa. [PP] | Must | CMS | 010 |
| RF-38 | WHEN se sube una imagen o un video THE SYSTEM SHALL optimizarlo para la web (tamaño y formato) antes de servirlo. | Should | CMS | 005 |
| RF-39 | THE SYSTEM SHALL permitir gestionar banners con orden y publicación programada. | Must | CMS | 005 |
| RF-40 | THE SYSTEM SHALL permitir gestionar flyers (imagen o PDF). La ubicación en la web se define con el prototipo. [PP] [FIG] | Must | CMS | 010 |
| RF-41 | THE SYSTEM SHALL permitir adjuntar a cada programa documentos descargables (PDF y Word), incluido el documento completo de condiciones. | Must | CMS | 006 |
| RF-42 | THE SYSTEM SHALL generar desde el contenido del programa un documento descargable (PDF y/o Word) sin la marca de la empresa. | Should | WEB | 006 |

### CMS: importación y carga inicial
| ID | Requisito | Prioridad | Parte | Spec |
|---|---|---|---|---|
| RF-43 | THE SYSTEM SHALL permitir importar en lote los datos principales de varios programas, que luego se completan a mano en el CMS. | Must | CMS | 011 |
| RF-44 | WHEN Producto sube el Word de un programa THE SYSTEM SHALL prellenar con él los campos del detalle, para revisarlos antes de guardar. Sujeto a un spike de viabilidad al inicio de la spec. [PP] | Could | CMS | 011 |
| RF-45 | THE SYSTEM SHALL tener cargados y publicados los ~70 programas activos antes del lanzamiento de la v1. | Must | CMS | 011 |

### Automatizaciones
| ID | Requisito | Prioridad | Parte | Spec |
|---|---|---|---|---|
| RF-46 | THE SYSTEM SHALL guardar el cupo por salida, no por programa, y aceptar actualizaciones desde una fuente externa además de la edición manual. | Must | AUTO | 002 |
| RF-47 | WHEN cambia el cupo de una salida THE SYSTEM SHALL registrar el valor anterior y el nuevo, la fecha y hora, el origen (`manual` o `drive`) y el autor o proceso. | Must | AUTO | 002 |
| RF-48 | THE SYSTEM SHALL ofrecer en el CMS un punto de control de automatizaciones. En v1 muestra el historial de cupos por salida y las retiradas automáticas (RF-20 a RF-22). [PP] | Must | AUTO | 009 |
| RF-49 | WHEN se ejecuta la sincronización THE SYSTEM SHALL leer el archivo de cupos de cada programa en Google Drive y actualizar los cupos por salida. El estado de la sincronización y sus errores se ven en el punto de control. | Won't (v1) · v1.1 | AUTO | 012 |
| RF-50 | THE SYSTEM SHALL responder consultas de clientes con un chatbot basado en el contenido de la web. | Won't (v1) · futuro | AUTO | — |
| RF-51 | WHERE el editor activa el modo umbral en una salida THE SYSTEM SHALL marcar «Últimas plazas» cuando el cupo baja del umbral configurado. La marca manual de RF-13 sigue siendo el modo por defecto. | Could | CMS | 002 |

## No funcionales
| ID | Requisito | Medición | Prioridad | Parte |
|---|---|---|---|---|
| RNF-01 | **Restricción de stack.** La web pública usa React, Next.js y Tailwind CSS. El CMS usa TypeScript, el ecosistema React y Tailwind, y sirve el contenido a la web pública sin fricción. No se usa ningún CMS de terceros; las librerías sí. Las piezas concretas se eligen en la 001. | El ADR del stack cumple cada punto | Must | TRANS |
| RNF-02 | **Coste mensual mínimo.** Se evalúa primero la infraestructura existente: Railway, Cloudflare R2 en capa gratuita y dominio propio. | El ADR del stack incluye una estimación mensual con el volumen de RNF-03 | Must | TRANS |
| RNF-03 | **Volumen.** ≥ 70 programas activos con crecimiento gradual (diseño para 300). De 1 a 20 salidas por programa (media de 10). De 15 a 20 medios por programa. Videos de hasta 3 min y 100 MB. | Pruebas con datos sintéticos de 300 programas × 20 salidas | Must | TRANS |
| RNF-04 | **Datos estructurados y legibles por máquina:** campos tipados (salidas, tarifas, itinerario por día, ciudades), no HTML libre, para no bloquear el chatbot. | El modelo de la 002 se exporta a JSON sin parsear HTML | Must | TRANS |
| RNF-05 | **Seguridad de cuentas:** contraseñas con hash robusto, sesiones que caducan, límite de intentos de login, permisos comprobados en el servidor y HTTPS en todo. | Auditoría sin P0 ni P1 de seguridad | Must | CMS |
| RNF-06 | **Trazabilidad:** cada cambio de contenido guarda autor y fecha. | Comprobable en el historial de un programa | Should | CMS |
| RNF-07 | **Propagación:** un cambio publicado se ve en la web pública en poco tiempo. | ≤ 1 min | Must | WEB |
| RNF-08 | **Rendimiento web.** | LCP ≤ 2,5 s en móvil 4G en listado y detalle; buscador y filtros ≤ 500 ms con el volumen de RNF-03 | Should | WEB |
| RNF-09 | **Rendimiento CMS.** | Guardar ≤ 2 s; alta completa ≤ 45 min a mano y ≤ 20 min con importación | Should | CMS |
| RNF-10 | **Fidelidad visual:** la web pública reproduce el diseño visual actual y los prototipos de Figma mediante tokens. | Revisión UX contra Figma sin P1 | Must | WEB |
| RNF-11 | **Responsive:** web pública mobile-first desde 360 px. CMS optimizado para escritorio. | QA en 360, 768 y 1280 px | Must | WEB |
| RNF-12 | **Accesibilidad** de la web pública. | WCAG 2.1 AA en listado y detalle (axe sin errores críticos) | Should | WEB |
| RNF-13 | **Localización:** solo español; precios en USD con un formato único. | Revisión de copy y formato | Must | WEB |
| RNF-14 | **Zona horaria única** (la de la agencia) para la caducidad de RF-20 y la programación de RF-19 y RF-39. | Tests de los cortes de fecha | Must | TRANS |
| RNF-15 | **Privacidad:** la web pública no recoge datos personales. Si la analítica usa cookies, se muestra un aviso de consentimiento. | Revisión en la spec 007 | Must | WEB |
| RNF-16 | **Copias de seguridad** de la base de datos y de los medios, con restauración probada. | Runbook con prueba de restauración | Should | TRANS |
| RNF-17 | **Navegadores:** últimas 2 versiones de Chrome, Safari, Edge y Firefox. | QA | Should | TRANS |
| RNF-18 | **Interfaz del CMS por capacidades:** las specs de interfaz del CMS no empiezan hasta que llegue su prototipo. [PP] | Roadmap: 008–010 tras el hito del prototipo | Must | CMS |
