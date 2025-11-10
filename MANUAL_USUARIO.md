# Manual de Usuario - Mundosol

Guía completa para usar el sistema de gestión de pedidos Mundosol.

## Índice

1. [Inicio de Sesión](#inicio-de-sesión)
2. [Dashboard Principal](#dashboard-principal)
3. [Gestión de Pedidos](#gestión-de-pedidos)
4. [Roles y Permisos](#roles-y-permisos)
5. [Administración](#administración)

---

## Inicio de Sesión

### Acceder al Sistema

1. Abrir navegador web
2. Ir a: `http://localhost:5000` (o la URL configurada)
3. Ingresar usuario y contraseña
4. Click en "Iniciar Sesión"

### Credenciales por Defecto

- **Usuario:** admin
- **Contraseña:** admin123

⚠️ **Importante:** Cambiar la contraseña después del primer inicio de sesión.

### Olvidé mi Contraseña

Contactar al administrador del sistema para resetear la contraseña.

---

## Dashboard Principal

El dashboard es la pantalla principal del sistema, organizada en 3 columnas:

### Columna 1: Filtros (Izquierda)

**Estados disponibles:**
- **Todos:** Ver todos los pedidos
- **Pendientes:** Pedidos sin asignar (amarillo)
- **Asignados:** Pedidos asignados a usuarios (naranja)
- **Completados:** Pedidos finalizados (verde)
- **Archivados:** Pedidos archivados (gris)

**Acciones rápidas:**
- **Mis asignaciones:** Ver solo pedidos asignados a ti
- **Panel admin:** Gestionar usuarios (solo administradores)

### Columna 2: Lista de Pedidos (Centro)

Muestra los pedidos según filtros aplicados:

- **Remitente:** Email del cliente
- **Asunto:** Título del pedido
- **Preview:** Primeras líneas del contenido
- **Estado:** Badge de color según estado
- **Fecha:** Cuándo se recibió (formato relativo)
- **Asignado a:** Usuario responsable (si aplica)

**Búsqueda:**
- Buscar por remitente, asunto o contenido
- La búsqueda se actualiza automáticamente

**Paginación:**
- 50 pedidos por página
- Navegar con botones "Anterior" y "Siguiente"

### Columna 3: Detalle del Pedido (Derecha)

Al hacer click en un pedido, se muestra:

- **Información completa:**
  - Remitente
  - Fecha y hora de recepción
  - Asunto
  - Contenido completo
  - Archivos adjuntos (si hay)

- **Acciones disponibles** (según estado y rol)

- **Historial completo:**
  - Todas las acciones realizadas
  - Quién y cuándo las realizó
  - Detalles de cada cambio

---

## Gestión de Pedidos

### Estados de un Pedido

Un pedido pasa por estos estados:

1. **Pendiente** → Recién llegado, sin asignar
2. **Asignado** → Asignado a un usuario de logística
3. **Completado** → Procesado y respondido
4. **Archivado** → Guardado para referencia (solo admin)

### Asignar un Pedido

**Quién puede:** Admin y Logística

**Pasos:**
1. Seleccionar pedido en estado "Pendiente"
2. En el detalle, ver sección "Asignar pedido"
3. Seleccionar usuario del desplegable
4. Click en "Asignar"
5. El pedido cambia a estado "Asignado"
6. Outlook se actualiza automáticamente (vía n8n)

### Completar un Pedido

**Quién puede:** Usuario asignado, Admin o Logística

**Pasos:**
1. Seleccionar pedido en estado "Asignado"
2. En el detalle, ver sección "Completar pedido"
3. (Opcional) Escribir la respuesta enviada al cliente
4. Click en "Marcar como completado"
5. El pedido cambia a estado "Completado"
6. Outlook se actualiza automáticamente

**Nota:** El campo de respuesta es opcional pero recomendado para tener registro de lo enviado al cliente.

### Archivar un Pedido

**Quién puede:** Solo Admin

**Pasos:**
1. Seleccionar cualquier pedido
2. En el detalle, click en "Archivar pedido"
3. Confirmar la acción
4. El pedido cambia a estado "Archivado"

**Uso:** Para pedidos que no requieren acción pero se quieren guardar.

### Ver Historial

**Acceso:** Menu superior → "Historial"

Muestra tabla con todos los pedidos completados o archivados:
- Filtros por estado
- Búsqueda
- Exportar (próximamente)

---

## Roles y Permisos

### Usuario

**Puede:**
- ✅ Ver pedidos asignados a él
- ✅ Completar sus propios pedidos
- ✅ Ver historial de sus pedidos

**No puede:**
- ❌ Ver pedidos de otros usuarios
- ❌ Asignar pedidos
- ❌ Archivar pedidos
- ❌ Gestionar usuarios

**Uso típico:** Personal que procesa pedidos específicos.

### Logística

**Puede:**
- ✅ Ver TODOS los pedidos
- ✅ Asignar pedidos a cualquier usuario
- ✅ Completar cualquier pedido
- ✅ Ver historial completo

**No puede:**
- ❌ Archivar pedidos
- ❌ Gestionar usuarios

**Uso típico:** Coordinadores que distribuyen trabajo.

### Admin

**Puede:**
- ✅ TODO lo que puede Logística
- ✅ Archivar pedidos
- ✅ Gestionar usuarios (crear, editar, eliminar)
- ✅ Resetear contraseñas
- ✅ Acceso completo al sistema

**Uso típico:** Administradores del sistema.

---

## Administración

### Gestionar Usuarios

**Acceso:** Menu superior → "Usuarios" (solo Admin)

### Crear Usuario

1. Click en "Crear Usuario"
2. Completar formulario:
   - **Usuario:** Nombre de inicio de sesión (único)
   - **Email:** Correo electrónico (único)
   - **Contraseña:** Mínimo 6 caracteres
   - **Rol:** Usuario, Logística o Admin
3. Click en "Crear Usuario"

**Recomendaciones:**
- Usar nombres de usuario cortos y fáciles de recordar
- Contraseñas seguras (mínimo 8 caracteres, mezcla de letras y números)
- Asignar el rol mínimo necesario

### Editar Usuario

1. En la lista de usuarios, click en ícono de lápiz
2. Modificar campos necesarios:
   - Usuario
   - Email
   - Rol
   - Estado (Activo/Inactivo)
3. Click en "Guardar Cambios"

**Notas:**
- No puedes cambiar tu propio rol
- No puedes desactivar tu propia cuenta

### Resetear Contraseña

1. En la lista de usuarios, click en ícono de llave
2. Ingresar nueva contraseña
3. Click en "Resetear Contraseña"
4. Informar al usuario su nueva contraseña

### Desactivar Usuario

1. Editar usuario
2. Desmarcar "Usuario activo"
3. Guardar cambios

**Efecto:** El usuario no podrá iniciar sesión pero sus datos se conservan.

### Eliminar Usuario

1. En la lista de usuarios, click en ícono de papelera
2. Confirmar eliminación

⚠️ **Advertencia:** Esta acción no se puede deshacer. Los pedidos asignados a este usuario quedarán sin asignar.

---

## Flujo de Trabajo Recomendado

### Proceso Diario

1. **Mañana:**
   - Revisar pedidos pendientes
   - Asignar pedidos urgentes primero
   - Distribuir carga de trabajo

2. **Durante el día:**
   - Procesar pedidos asignados
   - Marcar como completado al terminar
   - Agregar notas en respuesta

3. **Tarde:**
   - Revisar pedidos completados del día
   - Verificar que todos tengan respuesta
   - Archivar pedidos antiguos (si aplica)

### Buenas Prácticas

✅ **Hacer:**
- Asignar pedidos apenas lleguen
- Completar pedidos el mismo día si es posible
- Escribir respuestas claras en el campo de completado
- Revisar historial antes de actuar
- Mantener comunicación con el equipo

❌ **Evitar:**
- Dejar pedidos sin asignar mucho tiempo
- Completar sin agregar respuesta
- Cambiar estado sin procesar realmente
- Archivar pedidos activos

---

## Atajos de Teclado

(Próximamente)

---

## Preguntas Frecuentes

### ¿Cómo sé si un pedido es urgente?

Los pedidos con prioridad "alta" vienen marcados desde Outlook. Revisa el campo de prioridad en el detalle.

### ¿Puedo reasignar un pedido?

Sí, Admin y Logística pueden asignar un pedido a otro usuario en cualquier momento.

### ¿Qué pasa si completo un pedido por error?

Contacta al administrador para que lo revierta desde la base de datos.

### ¿Los emails se envían automáticamente?

No, el sistema solo registra la respuesta. El envío real se hace desde Outlook o mediante n8n si está configurado.

### ¿Puedo ver pedidos de hace meses?

Sí, en la sección "Historial" puedes buscar y filtrar pedidos antiguos.

### ¿El sistema funciona en móvil?

Sí, el diseño es responsive y funciona en tablets y smartphones.

---

## Soporte Técnico

Para problemas técnicos o dudas:

- **Email:** soporte@mundosol.com
- **Teléfono:** XXX-XXX-XXXX
- **Horario:** Lunes a Viernes, 9:00 - 18:00

---

## Actualizaciones

**Versión actual:** 1.0.0

**Próximas funcionalidades:**
- Exportar reportes a Excel
- Notificaciones por email
- Estadísticas y gráficos
- Búsqueda avanzada
- Etiquetas personalizadas
- Comentarios en pedidos

---

*Última actualización: Noviembre 2024*
