"""
Simulador de n8n - Procesa correo de Outlook y lo envía a Flask
Este script simula exactamente lo que hace n8n:
1. Recibe datos de Outlook
2. Los procesa/adapta con código JavaScript (simulado en Python)
3. Los envía a Flask mediante HTTP POST
"""
import requests
import json
from datetime import datetime

# ============================================================
# PASO 1: Simular datos crudos de Outlook
# ============================================================
print("=" * 70)
print("📧 SIMULADOR N8N - MUNDOSOL")
print("=" * 70)

# Datos RAW de Outlook (como los recibe el Trigger)
outlook_raw = {
    "id": "AAMkADU5NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1",
    "from": {
        "emailAddress": {
            "name": "Juan Carlos García López",
            "address": "juan.garcia@clientepremium.com"
        }
    },
    "subject": "URGENTE: Nuevo pedido grande - Cliente Premium XYZ",
    "bodyPreview": "Hola, necesitamos hacer un pedido urgente de varios productos...",
    "body": {
        "contentType": "html",
        "content": """<html>
<body>
<h2>Nuevo Pedido - Cliente Premium XYZ</h2>
<p>Hola equipo de Mundosol,</p>
<p>Espero que se encuentren bien. Les escribo para hacer un <strong>pedido urgente</strong>...</p>
<h3>DETALLES DEL PEDIDO:</h3>
<ul>
<li><strong>50 unidades</strong> de Producto Premium A (Ref: PRD-001)</li>
<li><strong>30 unidades</strong> de Producto Premium B (Ref: PRD-002)</li>
<li><strong>20 unidades</strong> de Producto Premium C (Ref: PRD-003)</li>
<li><strong>15 unidades</strong> de Producto Premium D (Ref: PRD-004)</li>
</ul>
<h3>INFORMACIÓN DE ENTREGA:</h3>
<p>Dirección: Calle Principal 123, Piso 5, Oficina 501<br>
Ciudad: Madrid<br>
Código Postal: 28001<br>
Teléfono: +34 91 123 4567</p>
<h3>TOTAL ESTIMADO: €2,500.00</h3>
</body>
</html>"""
    },
    "receivedDateTime": "2025-11-11T12:00:00Z",
    "hasAttachments": True,
    "attachments": [
        {
            "name": "especificaciones_tecnicas.pdf",
            "contentType": "application/pdf",
            "size": 2500000,
            "@odata.mediaContentUrl": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/especificaciones_tecnicas.pdf"
        },
        {
            "name": "foto_1.jpg",
            "contentType": "image/jpeg",
            "size": 3500000,
            "@odata.mediaContentUrl": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/foto_1.jpg"
        },
        {
            "name": "foto_2.jpg",
            "contentType": "image/jpeg",
            "size": 4200000,
            "@odata.mediaContentUrl": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/foto_2.jpg"
        },
        {
            "name": "video_demostrativo.mp4",
            "contentType": "video/mp4",
            "size": 125000000,
            "@odata.mediaContentUrl": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/video_demostrativo.mp4"
        },
        {
            "name": "presupuesto_anterior.xlsx",
            "contentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "size": 850000,
            "@odata.mediaContentUrl": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/presupuesto_anterior.xlsx"
        }
    ],
    "importance": "high",
    "webLink": "https://outlook.office365.com/mail/inbox/AAMkADU5NTk1",
    "conversationId": "AAQkADU5NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1NTk1"
}

print("\n1️⃣  DATOS CRUDOS DE OUTLOOK (Trigger Output):")
print("-" * 70)
print(json.dumps(outlook_raw, indent=2, default=str)[:500] + "...\n")

# ============================================================
# PASO 2: Procesar/Adaptar datos (Simular nodo Code de n8n)
# ============================================================
print("\n2️⃣  PROCESANDO DATOS (Code Node - JavaScript simulado en Python):")
print("-" * 70)

# Simulación del código JavaScript de n8n
def procesar_datos_outlook(outlook_data):
    """
    Simula el nodo Code de n8n que adapta datos de Outlook
    """
    
    # Extraer información del remitente
    from_data = outlook_data.get('from', {}).get('emailAddress', {})
    
    # Procesar adjuntos
    attachments = []
    if outlook_data.get('hasAttachments') and outlook_data.get('attachments'):
        for att in outlook_data['attachments']:
            content_type = att.get('contentType', 'application/octet-stream')
            
            # Categorizar por tipo
            if content_type.startswith('image/'):
                category = 'image'
            elif content_type.startswith('video/'):
                category = 'video'
            else:
                category = 'document'
            
            attachments.append({
                'name': att.get('name'),
                'contentType': content_type,
                'size': att.get('size', 0),
                'url': att.get('@odata.mediaContentUrl'),
                'category': category
            })
    
    # Determinar prioridad
    importance = outlook_data.get('importance', 'normal')
    if importance == 'high':
        prioridad = 'alta'
    elif importance == 'low':
        prioridad = 'baja'
    else:
        prioridad = 'normal'
    
    # Crear JSON adaptado para Flask
    adapted_data = {
        'messageId': outlook_data.get('id'),
        'account': from_data.get('address', 'unknown'),
        'accountName': 'Cuenta Ventas Mundosol',
        'from': {
            'name': from_data.get('name', 'Sin nombre'),
            'email': from_data.get('address', 'unknown@unknown.com')
        },
        'subject': outlook_data.get('subject', 'Sin asunto'),
        'bodyPreview': outlook_data.get('bodyPreview', ''),
        'body': outlook_data.get('body', {}).get('content', ''),
        'bodyHtml': outlook_data.get('body', {}).get('content') 
                   if outlook_data.get('body', {}).get('contentType') == 'html' else None,
        'receivedDateTime': outlook_data.get('receivedDateTime'),
        'attachments': attachments,
        'webLink': outlook_data.get('webLink'),
        'conversationId': outlook_data.get('conversationId'),
        'prioridad': prioridad
    }
    
    return adapted_data

# Procesar
datos_adaptados = procesar_datos_outlook(outlook_raw)

print("✓ Datos adaptados para Flask:")
print(json.dumps(datos_adaptados, indent=2, default=str)[:800] + "...\n")

# ============================================================
# PASO 3: Enviar a Flask (HTTP Request Node)
# ============================================================
print("\n3️⃣  ENVIANDO A FLASK (HTTP Request Node):")
print("-" * 70)

WEBHOOK_URL = "http://localhost:5000/webhook/pedido/nuevo"
WEBHOOK_TOKEN = "mundosol-webhook-token-2024-cambiar"

headers = {
    "X-Webhook-Token": WEBHOOK_TOKEN,
    "Content-Type": "application/json"
}

print(f"📍 URL: {WEBHOOK_URL}")
print(f"🔐 Token: {WEBHOOK_TOKEN}")
print(f"📦 Headers: {headers}")

try:
    print("\n⏳ Enviando POST...\n")
    response = requests.post(WEBHOOK_URL, json=datos_adaptados, headers=headers)
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"📦 Response:")
    response_json = response.json()
    print(json.dumps(response_json, indent=2))
    
    if response.status_code == 201:
        print("\n" + "=" * 70)
        print("✓ ¡ÉXITO! Pedido creado correctamente")
        print("=" * 70)
        pedido_id = response_json.get('pedido_id')
        remitente = response_json.get('remitente')
        cuenta = response_json.get('cuenta_origen')
        print(f"\n📋 Detalles del pedido creado:")
        print(f"   ID: {pedido_id}")
        print(f"   Remitente: {remitente}")
        print(f"   Cuenta Outlook: {cuenta}")
        print(f"   Archivos adjuntos: {len(datos_adaptados['attachments'])}")
        print(f"\n   Archivos:")
        for att in datos_adaptados['attachments']:
            size_mb = att['size'] / (1024 * 1024)
            print(f"   - {att['name']} ({att['category']}) - {size_mb:.2f} MB")
    else:
        print(f"\n❌ Error: {response_json.get('error')}")
        
except Exception as e:
    print(f"\n❌ Error al enviar: {e}")

print("\n" + "=" * 70)
print("Flujo completado")
print("=" * 70)
