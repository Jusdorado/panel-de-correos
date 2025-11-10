# Configuración de n8n para Mundosol

Esta guía explica cómo configurar los workflows de n8n para integrar Outlook con Mundosol.

## Requisitos Previos

- n8n instalado y funcionando
- Cuenta de Outlook/Microsoft 365 configurada en n8n
- Mundosol corriendo y accesible desde n8n

## Workflow 1: Recibir Emails de Outlook

Este workflow detecta nuevos emails en Outlook y los envía a Mundosol.

### Nodos necesarios:

1. **Trigger: Microsoft Outlook - On Email Received**
   - Configurar cuenta de Outlook
   - Carpeta: Inbox (o carpeta específica)
   - Trigger on: New Email

2. **Function: Preparar Datos**
   ```javascript
   // Extraer datos del email
   const item = items[0].json;
   
   return [{
     json: {
       message_id: item.id,
       from: item.from.emailAddress.address,
       subject: item.subject,
       body: item.bodyPreview || item.body.content,
       attachments: (item.attachments || []).map(att => ({
         filename: att.name,
         url: att.contentUrl || ''
       })),
       prioridad: item.importance === 'high' ? 'alta' : 
                  item.importance === 'low' ? 'baja' : 'normal'
     }
   }];
   ```

3. **HTTP Request: Enviar a Mundosol**
   - Method: POST
   - URL: `http://tu-servidor:5000/webhook/pedido/nuevo`
   - Headers:
     - `X-Webhook-Token`: `tu-token-configurado`
     - `Content-Type`: `application/json`
   - Body: JSON
   ```json
   {
     "message_id": "={{ $json.message_id }}",
     "from": "={{ $json.from }}",
     "subject": "={{ $json.subject }}",
     "body": "={{ $json.body }}",
     "attachments": "={{ $json.attachments }}",
     "prioridad": "={{ $json.prioridad }}"
   }
   ```

4. **IF: Verificar Respuesta**
   - Condition: `{{ $json.success }} === true`

5. **Microsoft Outlook: Marcar como Leído** (opcional)
   - Operation: Update Message
   - Message ID: `={{ $node["Trigger"].json.id }}`
   - Update Fields:
     - Is Read: true

## Workflow 2: Actualizar Outlook desde Mundosol

Este workflow recibe actualizaciones de Mundosol y actualiza el email en Outlook.

### Nodos necesarios:

1. **Webhook: Recibir Actualización**
   - Path: `/actualizar-outlook`
   - Method: POST
   - Authentication: Header Auth
     - Name: `X-Webhook-Token`
     - Value: `tu-token-configurado`

2. **Function: Preparar Categoría**
   ```javascript
   const estado = items[0].json.estado;
   const asignado_a = items[0].json.asignado_a;
   
   let categoria = 'Mundosol - Pendiente';
   let color = 'preset0'; // Amarillo
   
   if (estado === 'asignado') {
     categoria = `Mundosol - Asignado a ${asignado_a}`;
     color = 'preset3'; // Naranja
   } else if (estado === 'completado') {
     categoria = 'Mundosol - Completado';
     color = 'preset5'; // Verde
   }
   
   return [{
     json: {
       message_id: items[0].json.message_id,
       categoria: categoria,
       color: color
     }
   }];
   ```

3. **Microsoft Outlook: Actualizar Email**
   - Operation: Update Message
   - Message ID: `={{ $json.message_id }}`
   - Update Fields:
     - Categories: `={{ [$json.categoria] }}`

4. **HTTP Request: Confirmar a Mundosol** (opcional)
   - Method: POST
   - URL: `http://tu-servidor:5000/webhook/pedido/outlook-actualizado`
   - Headers:
     - `X-Webhook-Token`: `tu-token-configurado`
     - `Content-Type`: `application/json`
   - Body:
   ```json
   {
     "message_id": "={{ $json.message_id }}",
     "estado": "={{ $json.categoria }}",
     "timestamp": "={{ $now.toISO() }}"
   }
   ```

## Workflow 3: Completar Pedido

Este workflow maneja cuando un pedido se marca como completado.

### Nodos necesarios:

1. **Webhook: Recibir Completado**
   - Path: `/completar-pedido`
   - Method: POST
   - Authentication: Header Auth

2. **Microsoft Outlook: Actualizar Categoría**
   - Operation: Update Message
   - Message ID: `={{ $json.message_id }}`
   - Update Fields:
     - Categories: `["Mundosol - Completado"]`

3. **IF: ¿Hay Respuesta?**
   - Condition: `{{ $json.respuesta }}` is not empty

4. **Microsoft Outlook: Enviar Respuesta** (si hay respuesta)
   - Operation: Send Email
   - To: `={{ $json.from }}`
   - Subject: `RE: {{ $json.subject }}`
   - Body: `={{ $json.respuesta }}`

5. **Microsoft Outlook: Mover a Carpeta** (opcional)
   - Operation: Move Message
   - Message ID: `={{ $json.message_id }}`
   - Folder: "Completados" o "Archivo"

## Configuración de Categorías en Outlook

Para mejor visualización, crear categorías personalizadas en Outlook:

1. **Mundosol - Pendiente** (Amarillo)
2. **Mundosol - Asignado** (Naranja)
3. **Mundosol - Completado** (Verde)
4. **Mundosol - Archivado** (Gris)

## Configuración de Carpetas (Opcional)

Crear carpetas en Outlook para organizar:

- **Mundosol/Pendientes**
- **Mundosol/En Proceso**
- **Mundosol/Completados**

Modificar Workflow 1 para mover emails automáticamente según estado.

## Testing

### Probar Webhook de Entrada

Desde n8n, ejecutar manualmente el workflow 1 o enviar un email de prueba.

### Probar Webhook de Salida

Desde Mundosol, asignar un pedido y verificar que se actualiza en Outlook.

```bash
# Test manual con curl
curl -X POST http://localhost:5678/webhook/actualizar-outlook \
  -H "X-Webhook-Token: tu-token" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "AAMkAGI...",
    "estado": "asignado",
    "asignado_a": "juan"
  }'
```

## Seguridad

1. **Usar HTTPS** en producción para webhooks
2. **Tokens seguros**: Generar tokens aleatorios largos
3. **Validar origen**: Verificar IPs permitidas en n8n
4. **Logs**: Activar logging en n8n para auditoría

## Troubleshooting

### Email no llega a Mundosol

1. Verificar que n8n puede acceder a la URL de Mundosol
2. Revisar logs de n8n para errores
3. Verificar token en headers
4. Probar endpoint manualmente con curl

### Outlook no se actualiza

1. Verificar permisos de la cuenta de Outlook en n8n
2. Revisar que el message_id es correcto
3. Verificar que las categorías existen en Outlook
4. Revisar logs del workflow en n8n

### Respuestas no se envían

1. Verificar permisos de envío de la cuenta
2. Revisar formato del email de respuesta
3. Verificar que el campo "from" tiene un email válido

## Ejemplo Completo de Flujo

1. Cliente envía email a `pedidos@mundosol.com`
2. Outlook recibe email
3. n8n Workflow 1 detecta nuevo email
4. n8n envía datos a Mundosol `/webhook/pedido/nuevo`
5. Mundosol crea pedido en estado "pendiente"
6. Usuario de logística asigna pedido en Mundosol
7. Mundosol llama webhook n8n `/actualizar-outlook`
8. n8n Workflow 2 actualiza categoría en Outlook
9. Usuario completa pedido y escribe respuesta
10. Mundosol llama webhook n8n `/completar-pedido`
11. n8n Workflow 3 marca como completado y envía respuesta
12. Email se mueve a carpeta "Completados"

## Recursos Adicionales

- [Documentación n8n](https://docs.n8n.io/)
- [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/)
- [n8n Community](https://community.n8n.io/)

## Soporte

Para problemas específicos de integración, contactar al equipo de desarrollo.
