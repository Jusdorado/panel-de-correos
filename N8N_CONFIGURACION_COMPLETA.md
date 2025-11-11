# Configuración Completa de n8n para Mundosol

## Flujo General

```
Outlook Trigger → Filtro Pedido → Procesar Datos → HTTP POST → Webhook Flask
```

## 1. Nodos Necesarios en n8n

### 1.1 Microsoft Outlook Trigger (Ya existe)
- **Configuración**: Monitorea carpeta de entrada cada minuto
- **Salida**: Mensaje completo de Outlook con todos los detalles

### 1.2 Filtro: ¿Es pedido/recibo? (Ya existe)
- **Tipo**: IF
- **Condiciones**: Busca palabras clave en asunto o preview
- **Salida**: True/False

### 1.3 NUEVO: Procesar Datos (Code Node - JavaScript)
**Este es el nodo crítico que adapta los datos**

```javascript
// Procesar y adaptar datos de Outlook para el webhook
const messageData = {
  // Identificadores únicos
  messageId: $input.item.json.id,
  
  // Información de la cuenta de Outlook que recibió
  account: $input.item.json.from?.emailAddress?.address || 'unknown',
  accountName: $node["Microsoft Outlook Trigger"].name || 'Cuenta Outlook',
  
  // Información del remitente (quien envía el pedido)
  from: {
    name: $input.item.json.from?.emailAddress?.name || 'Sin nombre',
    email: $input.item.json.from?.emailAddress?.address || 'unknown@unknown.com'
  },
  
  // Contenido del correo
  subject: $input.item.json.subject || 'Sin asunto',
  bodyPreview: $input.item.json.bodyPreview || '',
  body: $input.item.json.body?.content || '',
  bodyHtml: $input.item.json.body?.contentType === 'html' ? 
            $input.item.json.body?.content : null,
  
  // Fechas
  receivedDateTime: $input.item.json.receivedDateTime,
  
  // Adjuntos - IMPORTANTE: Procesar cada archivo
  attachments: [],
  
  // Metadatos
  webLink: $input.item.json.webLink,
  conversationId: $input.item.json.conversationId,
  
  // Prioridad basada en importancia del correo
  prioridad: $input.item.json.importance === 'high' ? 'alta' : 
            $input.item.json.importance === 'low' ? 'baja' : 'normal'
};

// Procesar adjuntos si existen
if ($input.item.json.hasAttachments && $input.item.json.attachments) {
  messageData.attachments = $input.item.json.attachments.map(att => {
    // Mapear tipos MIME a categorías
    const contentType = att.contentType || 'application/octet-stream';
    const isImage = contentType.startsWith('image/');
    const isVideo = contentType.startsWith('video/');
    const isPdf = contentType === 'application/pdf';
    
    return {
      name: att.name,
      contentType: contentType,
      size: att.size || 0,
      // URL de descarga desde Outlook (si está disponible)
      url: att['@odata.mediaContentUrl'] || null,
      // Categoría para facilitar procesamiento
      category: isImage ? 'image' : isVideo ? 'video' : 'document'
    };
  });
}

// Validación: asegurar que tenemos datos mínimos
if (!messageData.subject || !messageData.body) {
  throw new Error('Faltan datos críticos del correo (asunto o cuerpo)');
}

return messageData;
```

### 1.4 HTTP Request (Enviar a Flask)

**Configuración:**

| Campo | Valor |
|-------|-------|
| **Method** | POST |
| **URL** | `http://localhost:5000/webhook/pedido/nuevo` |
| **Authentication** | None (el token va en headers) |
| **Headers** | Ver abajo |
| **Body** | Raw JSON (del nodo anterior) |

**Headers a configurar:**

```
X-Webhook-Token: mundosol-webhook-token-2024-cambiar
Content-Type: application/json
```

**Body (Raw):**
```json
{{ $json }}
```

## 2. Flujo Paso a Paso

### Paso 1: Outlook Trigger recibe correo
```
Entrada: Correo de Outlook con:
- ID del mensaje
- Remitente
- Asunto
- Cuerpo (texto + HTML)
- Archivos adjuntos
- Fecha de recepción
```

### Paso 2: Filtro valida si es pedido
```
Busca en asunto/preview:
- "pedido"
- "orden"
- "recibo"
- "compra"
- "orden de compra"

Si coincide → Continúa
Si no coincide → Termina (No Match)
```

### Paso 3: Procesar Datos (Code Node)
```
Transforma el JSON de Outlook a formato esperado por Flask:

ANTES (Outlook):
{
  "id": "AAMkADU5NTk1...",
  "from": {
    "emailAddress": {
      "name": "Juan García",
      "address": "juan@cliente.com"
    }
  },
  "subject": "Nuevo pedido",
  "body": {
    "contentType": "html",
    "content": "<html>..."
  },
  "attachments": [...]
}

DESPUÉS (Para Flask):
{
  "messageId": "AAMkADU5NTk1...",
  "from": {
    "name": "Juan García",
    "email": "juan@cliente.com"
  },
  "subject": "Nuevo pedido",
  "body": "...",
  "bodyHtml": "<html>...",
  "attachments": [
    {
      "name": "archivo.pdf",
      "contentType": "application/pdf",
      "size": 125000,
      "url": "https://...",
      "category": "document"
    }
  ]
}
```

### Paso 4: HTTP Request envía a Flask
```
POST http://localhost:5000/webhook/pedido/nuevo
Headers:
  X-Webhook-Token: mundosol-webhook-token-2024-cambiar
  Content-Type: application/json

Body: JSON procesado
```

### Paso 5: Flask procesa y guarda
```
Flask recibe → Valida token → Procesa datos → 
Crea registro en BD → Retorna JSON con ID del pedido
```

## 3. Manejo de Errores en n8n

Añade un nodo "Error Handler" después del HTTP Request:

```javascript
// Si la respuesta no es 201 (Created)
if ($input.item.json.statusCode !== 201) {
  throw new Error(`Error en webhook: ${$input.item.json.body.error}`);
}

return $input.item.json;
```

## 4. Tipos de Adjuntos Soportados

| Tipo | MIME Type | Categoría | Ejemplo |
|------|-----------|-----------|---------|
| **Imágenes** | image/* | image | .jpg, .png, .gif, .webp |
| **Vídeos** | video/* | video | .mp4, .avi, .mov |
| **PDF** | application/pdf | document | .pdf |
| **Excel** | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | document | .xlsx |
| **Word** | application/vnd.openxmlformats-officedocument.wordprocessingml.document | document | .docx |
| **ZIP** | application/zip | document | .zip |

## 5. Flujo Completo en n8n (JSON)

Para importar este flujo en n8n, usa esta estructura:

```json
{
  "name": "Mundosol - Recepción de Pedidos",
  "nodes": [
    {
      "name": "Microsoft Outlook Trigger",
      "type": "n8n-nodes-base.microsoftOutlookTrigger",
      "position": [-880, 112],
      "parameters": {
        "pollTimes": {
          "item": [{"mode": "everyMinute"}]
        }
      }
    },
    {
      "name": "Filtro: ¿Es pedido?",
      "type": "n8n-nodes-base.if",
      "position": [-192, 112],
      "parameters": {
        "conditions": {
          "combinator": "or",
          "conditions": [
            {
              "leftValue": "={{ $json.subject }}",
              "operator": {"type": "string", "operation": "contains"},
              "rightValue": "pedido"
            },
            {
              "leftValue": "={{ $json.subject }}",
              "operator": {"type": "string", "operation": "contains"},
              "rightValue": "orden"
            }
          ]
        }
      }
    },
    {
      "name": "Procesar Datos",
      "type": "n8n-nodes-base.code",
      "position": [256, 112],
      "parameters": {
        "jsCode": "// [Código JavaScript del paso 1.3]"
      }
    },
    {
      "name": "Enviar a Flask",
      "type": "n8n-nodes-base.httpRequest",
      "position": [464, 112],
      "parameters": {
        "method": "POST",
        "url": "http://localhost:5000/webhook/pedido/nuevo",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "X-Webhook-Token",
              "value": "mundosol-webhook-token-2024-cambiar"
            },
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "",
              "value": "={{ $json }}"
            }
          ]
        }
      }
    }
  ],
  "connections": {
    "Microsoft Outlook Trigger": {
      "main": [[{"node": "Filtro: ¿Es pedido?", "type": "main", "index": 0}]]
    },
    "Filtro: ¿Es pedido?": {
      "main": [
        [{"node": "Procesar Datos", "type": "main", "index": 0}],
        [{"node": "No Match - Terminar", "type": "main", "index": 0}]
      ]
    },
    "Procesar Datos": {
      "main": [[{"node": "Enviar a Flask", "type": "main", "index": 0}]]
    },
    "Enviar a Flask": {
      "main": [[]]
    }
  }
}
```

## 6. Pruebas

### Prueba 1: Verificar que n8n recibe el correo
1. Envía un correo de prueba a la cuenta de Outlook
2. Abre n8n y ejecuta el trigger manualmente
3. Verifica que aparezca el correo en los logs

### Prueba 2: Verificar que se filtra correctamente
1. Envía correo CON palabra clave "pedido"
2. Envía correo SIN palabra clave
3. Verifica que solo el primero pase el filtro

### Prueba 3: Verificar que Flask recibe los datos
1. Ejecuta el flujo completo
2. Abre la web de Mundosol
3. Verifica que el pedido aparezca en el dashboard

## 7. Debugging

Si algo falla:

1. **En n8n**: Abre la ejecución y revisa los logs de cada nodo
2. **En Flask**: Revisa la consola donde corre `python run.py`
3. **En navegador**: Abre DevTools (F12) → Network → busca POST a `/webhook/pedido/nuevo`

## 8. Variables de Entorno

Asegúrate de que en `.env` tengas:

```
WEBHOOK_TOKEN=mundosol-webhook-token-2024-cambiar
N8N_WEBHOOK_URL=http://localhost:5678/webhook
```

Y en n8n, configura la URL de Flask como:
```
http://localhost:5000/webhook/pedido/nuevo
```
