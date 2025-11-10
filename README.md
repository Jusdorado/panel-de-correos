# Mundosol - Sistema de Gestión de Pedidos

Sistema web de gestión de pedidos para Mundosol, integrado con Outlook mediante workflows de n8n.

## 🚀 Características

- **Bandeja de entrada colaborativa** tipo Gmail para gestión de pedidos
- **Autenticación y roles** (Admin, Logística, Usuario)
- **Integración con Outlook** vía webhooks n8n bidireccionales
- **Asignación de pedidos** a usuarios de logística
- **Seguimiento completo** con historial de acciones
- **Interfaz moderna** con Bootstrap 5 y colores corporativos Mundosol
- **Responsive** para uso en móviles y tablets

## 📋 Requisitos

- Python 3.10 o superior
- MySQL 5.7 o superior
- n8n (para integración con Outlook)

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone <url-repositorio>
cd panel-de-correos
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Crear base de datos MySQL:

```sql
CREATE DATABASE mundosol_pedidos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mundosol_user'@'localhost' IDENTIFIED BY 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON mundosol_pedidos.* TO 'mundosol_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurar variables de entorno

Copiar `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Editar `.env`:

```env
SECRET_KEY=tu-secret-key-muy-segura-aqui
DATABASE_URL=mysql+pymysql://mundosol_user:tu_contraseña_segura@localhost/mundosol_pedidos
N8N_WEBHOOK_URL=https://tu-n8n-instance.com/webhook
WEBHOOK_TOKEN=token-seguro-para-webhooks-cambiar-esto
```

### 6. Inicializar base de datos y ejecutar

```bash
python run.py
```

El script creará automáticamente:
- Todas las tablas necesarias
- Usuario administrador por defecto

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

⚠️ **IMPORTANTE:** Cambiar la contraseña del admin en producción.

### 7. Acceder a la aplicación

Abrir navegador en: http://localhost:5000

## 📁 Estructura del Proyecto

```
mundosol-pedidos/
├── app/
│   ├── __init__.py           # Factory de la aplicación
│   ├── models.py             # Modelos de base de datos
│   ├── auth.py               # Sistema de autenticación
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py           # Rutas de login/logout
│   │   ├── admin.py          # Panel de administración
│   │   ├── pedidos.py        # Gestión de pedidos
│   │   └── webhooks.py       # Webhooks entrantes/salientes
│   ├── static/
│   │   ├── css/
│   │   │   └── mundosol.css  # Estilos personalizados
│   │   └── js/
│   │       └── dashboard.js  # JavaScript del dashboard
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── pedidos/
│       │   ├── detalle.html
│       │   └── historial.html
│       └── admin/
│           └── users.html
├── migrations/               # Migraciones de base de datos
├── config.py                 # Configuración de la aplicación
├── requirements.txt          # Dependencias Python
├── run.py                    # Punto de entrada
├── .env                      # Variables de entorno (no versionar)
└── README.md
```

## 🔐 Roles y Permisos

### Admin
- Acceso total al sistema
- Gestión de usuarios
- Ver y gestionar todos los pedidos
- Archivar pedidos

### Logística
- Ver todos los pedidos
- Asignar pedidos a usuarios
- Completar cualquier pedido
- Ver historial completo

### Usuario
- Ver solo pedidos asignados a él
- Completar sus propios pedidos
- Ver historial de sus pedidos

## 🔗 Integración con n8n

### Workflow 1: Recibir pedidos desde Outlook

Configurar webhook en n8n que envíe POST a:

```
POST http://tu-servidor:5000/webhook/pedido/nuevo
Headers:
  X-Webhook-Token: tu-token-configurado-en-env
  Content-Type: application/json

Body:
{
  "message_id": "AAMkAGI...",
  "from": "cliente@ejemplo.com",
  "subject": "Pedido de naranjas",
  "body": "Contenido del email...",
  "attachments": [
    {
      "filename": "pedido.pdf",
      "url": "https://..."
    }
  ],
  "prioridad": "normal"  // opcional: baja, normal, alta
}
```

### Workflow 2: Actualizar Outlook cuando se asigna/completa

La aplicación enviará POST a:

```
POST {N8N_WEBHOOK_URL}/actualizar-outlook
Body:
{
  "message_id": "AAMkAGI...",
  "estado": "asignado",
  "asignado_a": "usuario_logistica"
}

POST {N8N_WEBHOOK_URL}/completar-pedido
Body:
{
  "message_id": "AAMkAGI...",
  "estado": "completado",
  "respuesta": "Texto de respuesta enviada..."
}
```

### Workflow 3: Confirmación de actualización (opcional)

n8n puede confirmar que actualizó Outlook enviando:

```
POST http://tu-servidor:5000/webhook/pedido/outlook-actualizado
Headers:
  X-Webhook-Token: tu-token-configurado-en-env
  Content-Type: application/json

Body:
{
  "message_id": "AAMkAGI...",
  "estado": "asignado",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🎨 Personalización

### Colores Mundosol

Los colores corporativos están definidos en `app/static/css/mundosol.css`:

```css
:root {
    --mundosol-green: #4A7C3B;
    --mundosol-lime: #9BC83F;
    --mundosol-yellow: #F4D03F;
    --mundosol-orange: #E67E22;
    --mundosol-dark: #2C3E50;
    --mundosol-light: #ECF0F1;
}
```

## 🔧 Migraciones de Base de Datos

Si necesitas modificar los modelos:

```bash
# Inicializar migraciones (solo primera vez)
flask db init

# Crear migración
flask db migrate -m "Descripción del cambio"

# Aplicar migración
flask db upgrade
```

## 📊 API Endpoints

### Autenticación
- `GET/POST /login` - Iniciar sesión
- `GET /logout` - Cerrar sesión

### Dashboard
- `GET /dashboard` - Vista principal con filtros
- `GET /pedidos/<id>/detalle` - Detalle de pedido (AJAX)
- `POST /pedidos/<id>/asignar` - Asignar pedido
- `POST /pedidos/<id>/completar` - Completar pedido
- `POST /pedidos/<id>/archivar` - Archivar pedido (admin)
- `GET /pedidos/historial` - Historial de pedidos

### Webhooks
- `POST /webhook/pedido/nuevo` - Recibir nuevo pedido
- `POST /webhook/pedido/outlook-actualizado` - Confirmación

### Admin
- `GET /admin/users` - Listar usuarios
- `POST /admin/users/create` - Crear usuario
- `PUT /admin/users/<id>` - Editar usuario
- `POST /admin/users/<id>/reset-password` - Resetear contraseña
- `DELETE /admin/users/<id>/delete` - Eliminar usuario

## 🐛 Troubleshooting

### Error de conexión a MySQL

Verificar que MySQL está corriendo y las credenciales son correctas:

```bash
mysql -u mundosol_user -p mundosol_pedidos
```

### Error de importación de módulos

Reinstalar dependencias:

```bash
pip install --upgrade -r requirements.txt
```

### Webhooks no funcionan

1. Verificar que el token en `.env` coincide con el configurado en n8n
2. Revisar logs del servidor para ver errores
3. Probar webhook con curl:

```bash
curl -X POST http://localhost:5000/webhook/pedido/nuevo \
  -H "X-Webhook-Token: tu-token" \
  -H "Content-Type: application/json" \
  -d '{"message_id":"test","from":"test@test.com","subject":"Test","body":"Test"}'
```

## 📝 Notas de Producción

### Seguridad

1. Cambiar `SECRET_KEY` a un valor aleatorio seguro
2. Cambiar contraseña del usuario admin
3. Usar HTTPS en producción
4. Configurar firewall para proteger puerto 5000
5. Usar variables de entorno seguras (no hardcodear)

### Despliegue

Para producción, usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

O con nginx como proxy inverso.

### Backup

Hacer backup regular de la base de datos:

```bash
mysqldump -u mundosol_user -p mundosol_pedidos > backup_$(date +%Y%m%d).sql
```

## 📄 Licencia

Propiedad de Mundosol. Todos los derechos reservados.

## 👥 Soporte

Para soporte técnico, contactar al equipo de desarrollo.
