# Guía de Instalación Rápida - Mundosol

## Instalación en Windows

### 1. Instalar Python 3.10+
Descargar desde: https://www.python.org/downloads/

### 2. Instalar MySQL
Descargar desde: https://dev.mysql.com/downloads/mysql/

### 3. Configurar Base de Datos

Abrir MySQL Command Line Client y ejecutar:

```sql
CREATE DATABASE mundosol_pedidos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mundosol_user'@'localhost' IDENTIFIED BY 'MundosolPass2024!';
GRANT ALL PRIVILEGES ON mundosol_pedidos.* TO 'mundosol_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Configurar el Proyecto

Abrir PowerShell en la carpeta del proyecto:

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
copy .env.example .env
```

### 5. Editar archivo .env

Abrir `.env` con un editor de texto y configurar:

```env
SECRET_KEY=mundosol-secret-key-2024-cambiar-en-produccion
DATABASE_URL=mysql+pymysql://mundosol_user:MundosolPass2024!@localhost/mundosol_pedidos
N8N_WEBHOOK_URL=http://localhost:5678/webhook
WEBHOOK_TOKEN=mundosol-webhook-token-2024-cambiar
```

### 6. Ejecutar la Aplicación

```powershell
python run.py
```

### 7. Acceder

Abrir navegador en: http://localhost:5000

**Login:**
- Usuario: `admin`
- Contraseña: `admin123`

## Instalación en Linux/Mac

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tu editor favorito
nano .env

# Ejecutar
python run.py
```

## Verificación de Instalación

### Probar Webhook

```bash
curl -X POST http://localhost:5000/webhook/pedido/nuevo \
  -H "X-Webhook-Token: mundosol-webhook-token-2024-cambiar" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "test-123",
    "from": "cliente@ejemplo.com",
    "subject": "Pedido de prueba",
    "body": "Este es un pedido de prueba",
    "attachments": []
  }'
```

Deberías recibir:
```json
{
  "success": true,
  "message": "Pedido creado correctamente",
  "pedido_id": 1
}
```

## Solución de Problemas Comunes

### Error: "No module named 'MySQLdb'"

```bash
pip install pymysql
```

### Error: "Access denied for user"

Verificar credenciales en `.env` y que el usuario MySQL tenga permisos.

### Error: "Can't connect to MySQL server"

Verificar que MySQL está corriendo:

```bash
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql
```

### Puerto 5000 ocupado

Cambiar puerto en `run.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

## Próximos Pasos

1. Cambiar contraseña del admin en el panel de usuarios
2. Crear usuarios de logística
3. Configurar webhooks de n8n
4. Probar flujo completo de pedidos

## Soporte

Para más información, consultar `README.md`
