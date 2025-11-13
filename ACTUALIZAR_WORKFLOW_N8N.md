# 🔧 Actualizar Workflow n8n - Archivos Corregidos

## El Problema

Tu workflow actual tiene un pequeño error en cómo convierte los archivos a base64:

```javascript
// ❌ INCORRECTO
const base64Content = file.data.toString('base64');
```

Esto falla porque `file.data` puede ser un Buffer de diferentes formas.

## La Solución

He creado `N8N_WORKFLOW_CORREGIDO.json` con la corrección en el nodo **"Procesar Archivos"**.

### Cambio Principal

```javascript
// ✅ CORRECTO - Maneja múltiples formatos
let base64Content = '';

if (file.data instanceof Buffer) {
  // Si es un Buffer de Node.js
  base64Content = file.data.toString('base64');
} else if (typeof file.data === 'string') {
  // Si ya es string base64
  base64Content = file.data;
} else if (file.data && typeof file.data === 'object') {
  // Si es un objeto con propiedades
  const buffer = Buffer.from(file.data);
  base64Content = buffer.toString('base64');
}
```

## Pasos para Actualizar

### Opción 1: Importar el workflow completo (RECOMENDADO)

1. En n8n, ve a **Workflows**
2. Click en **Import from file**
3. Selecciona `N8N_WORKFLOW_CORREGIDO.json`
4. Click en **Import**
5. Prueba con un correo que tenga archivos

### Opción 2: Actualizar solo el nodo (Manual)

1. Abre tu workflow actual en n8n
2. Haz click en el nodo **"Procesar Archivos"**
3. Reemplaza TODO el código JavaScript con el del archivo `N8N_WORKFLOW_CORREGIDO.json`
4. Guarda cambios

## Qué Cambia

| Aspecto | Antes | Después |
|--------|-------|---------|
| Conversión base64 | Simple | Robusta (3 casos) |
| Manejo de errores | Mínimo | Mejorado |
| Versión workflow | 2.6 | 2.7 |
| Compatibilidad | Limitada | Completa |

## Verificación

Después de actualizar, prueba con un correo que tenga:

- ✅ Archivo Word (.docx)
- ✅ Archivo Excel (.xlsx)
- ✅ Archivo PDF
- ✅ Imagen adjunta

En los logs de n8n deberías ver:

```
✅ Adjunto: documento.docx (25.50 KB, tipo: word)
✅ Adjunto: presupuesto.xlsx (15.25 KB, tipo: excel)
✅ Adjunto: especificaciones.pdf (102.50 KB, tipo: pdf)
📊 Total de archivos: 3 (3 adjuntos + 0 imágenes inline)
```

## Si Sigue Sin Funcionar

1. **Verifica que `downloadAttachments: true`** en el Outlook Trigger
2. **Revisa los logs de n8n** para ver si hay errores
3. **Prueba con un correo simple** sin archivos primero
4. **Contacta con soporte** si persiste el problema

## Archivos Relacionados

- `N8N_WORKFLOW_CORREGIDO.json` - Workflow completo actualizado
- `app/routes/webhooks.py` - Backend que recibe los archivos
- `app/routes/pedidos.py` - Endpoint de descarga
- `N8N_ARCHIVOS_DESCARGA_GUIA.md` - Guía completa

## Notas Importantes

⚠️ **Después de importar el workflow:**
- Verifica que la URL del webhook sea correcta: `http://192.168.1.43:5000/webhook/pedido/nuevo`
- Verifica que el token sea: `mundosol-webhook-token-2024-cambiar`
- Verifica que la carpeta de Outlook sea: `Pedidos Pendientes`

✅ **Los archivos ahora se guardarán correctamente en base64 y se descargarán sin modificaciones.**
