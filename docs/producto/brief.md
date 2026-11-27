# Brief

Estado: aprobado por el Board (MEG-25)

## Problema
La agencia publica hoy sus programas de viaje en una landing con una grilla de cards y banners. Esa landing tiene poca información editable por programa. Cada programa se gestiona en un documento Word y los cupos en archivos aparte. Subir y actualizar un programa es lento, el cliente no ve el detalle completo (itinerario, salidas, tarifas, condiciones) y el equipo no tiene una herramienta propia para mantener el contenido.

## Usuarios
| Usuario | Qué necesita | Cómo lo hace hoy |
|---|---|---|
| Cliente final (público, sin cuenta) | Encontrar un programa por destino, zona, fecha, duración o ciudad; ver su detalle completo, sus salidas y su precio, y pedir una cotización | Navega la landing actual y escribe por WhatsApp |
| Producto (CMS) | Dar de alta, editar, programar y retirar programas con todo su detalle, salidas, tarifas y cupos, de forma rápida | Documento Word por programa y edición limitada en la web actual |
| Marketing (CMS) | Publicar banners, videos promocionales y flyers | Edición manual de la landing |
| Administrador (CMS) | Todo lo anterior, además de gestionar usuarios y roles | Sin herramienta propia |

## Objetivo de la primera versión
- **Cliente:** lista los programas en cards, busca en todo su contenido (incluidas las ciudades) y filtra. Ve la página de detalle completa, comparte el programa y pide una cotización por WhatsApp desde el programa o desde una salida concreta.
- **Producto:** carga un programa completo en el CMS sin ayuda técnica, lo programa o lo publica con vista previa, y mantiene a mano sus salidas, tarifas y cupos. Las salidas caducan solas 30 días antes de su fecha, y un programa sin salidas disponibles se retira solo.
- **Marketing:** gestiona banners, videos y flyers y los publica sin aprobación.
- **Administrador:** gestiona usuarios y roles.

## Alcance
- **Incluye:**
  - Web pública nueva: listado, buscador y filtros, detalle de programa, banners y videos promocionales, compartir, contacto por WhatsApp, email y teléfono, y SEO básico con analítica.
  - CMS a medida con roles (Marketing, Producto, Administrador), estados de publicación, publicación programada y vista previa.
  - Documentos descargables por programa.
  - Herramienta de importación para la carga inicial de los ~70 programas actuales.
- **Se reutiliza solo el diseño visual** de la web actual y de los prototipos de Figma. Del sistema actual no se reutilizan el código, la estructura ni la infraestructura.
- **No incluye (v1):**
  - **Sincronización de cupos desde Google Drive → v1.1**, justo después de la v1. El modelo de datos queda preparado desde la v1: cupos por salida, actualizables desde una fuente externa y con historial de cuándo y de dónde vino cada cambio (manual o Drive).
  - **Chatbot** de consultas de clientes: futuro, sin fecha. Para no bloquearlo, el contenido de los programas es estructurado y legible por máquina.
  - Formulario de contacto propio, cuentas de clientes, reservas y pagos online.
  - Otros idiomas (solo español) y otras monedas (solo USD).
  - Flujo de aprobación entre roles: cada rol publica directamente lo suyo.
  - CMS de terceros (WordPress, Strapi, Payload, Sanity…). Las librerías sí se permiten.

## Restricciones
- **Stack de referencia** (restricción de partida, no decisión): web pública en React, Next.js y Tailwind CSS. El CMS va en TypeScript, en el mismo ecosistema React y Tailwind, y sirve el contenido a la web pública sin fricción. Las piezas concretas se eligen en la issue `stack` (MEG-27) con una tarjeta de 4 capas al Board, no en la spec 001.
- **Infraestructura existente:** Railway (hosting), Cloudflare R2 en capa gratuita (imágenes) y dominio propio. Si se mantiene o se cambia se decide en MEG-27.
- **Coste:** sin presupuesto asignado; se prefiere el coste mensual mínimo.
- **Plazo:** sin fecha fija; se deriva del perfil (M) y del roadmap.
- **Prototipo del CMS:** todavía no existe. Los requisitos del CMS van por capacidad y las decisiones de interfaz quedan como «pendiente de prototipo».

## Datos
- **Contenido** (programas, salidas, tarifas, cupos y medios): todo público y no sensible.
- **Cuentas del CMS:** credenciales de los editores. Hay que proteger su acceso y la integridad del contenido: nadie sin el rol correspondiente puede publicar.
- **Datos personales de clientes:** la web pública no los recoge. El contacto se hace por enlaces a WhatsApp, email y teléfono, sin formulario. Si la analítica usa cookies, hará falta un aviso de consentimiento (lo concreta la spec de SEO y analítica).

## Métricas de éxito
La v1 funciona si el equipo usa el CMS como herramienta habitual. Valores propuestos, que el Board confirma al aprobar:
- **Alta completa de un programa:** ≤ 20 min con importación y ≤ 45 min a mano.
- **Edición de salidas, tarifas o cupos:** ≤ 2 min por cambio, y el cambio se ve en la web en ≤ 1 min.
- **Ediciones concurrentes:** 0 cambios perdidos cuando dos editores tocan el mismo programa.
- **Carga inicial:** los ~70 programas activos publicados antes del lanzamiento.

## Preguntas abiertas
No cambian el alcance ni el perfil; se cierran en la spec indicada.
- **Figma `MEGA-TRAVEL-BLOQUEOS`:** resuelto. El Board abrió el acceso de edición; el inventario de bloques del detalle se hace en la spec 004.
- **Formato de la importación masiva:** se define durante el proyecto, cuando se sepan los datos mínimos que necesita un programa importado. Se cierra en la spec 011.
- **«Últimas plazas»:** resuelto. La marca el editor a mano (RF-13); el modo por umbral queda como opción activable (RF-51, Could) en la spec 002.
