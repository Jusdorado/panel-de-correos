"""
Script para probar el webhook de pedidos manualmente
Simula un correo completo con múltiples tipos de archivos adjuntos
"""
import requests
import json
from datetime import datetime

# Configuración
WEBHOOK_URL = "http://localhost:5000/webhook/pedido/nuevo"
WEBHOOK_TOKEN = "mundosol-webhook-token-2024-cambiar"

# Headers
headers = {
    "X-Webhook-Token": WEBHOOK_TOKEN,
    "Content-Type": "application/json"
}

# Datos de prueba - Simular un correo completo de Outlook
test_data = {
    "messageId": f"test-message-{datetime.now().timestamp()}",
    "account": "ventas@mundosol.com",
    "accountName": "Cuenta Ventas Mundosol",
    "subject": "URGENTE: Nuevo pedido grande - Cliente Premium XYZ",
    "from": {
        "name": "Juan Carlos García López",
        "email": "juan.garcia@clientepremium.com"
    },
    "bodyPreview": "Hola, necesitamos hacer un pedido urgente de varios productos. Adjunto encontrarás los detalles...",
    "body": """Hola equipo de Mundosol,

Espero que se encuentren bien. Les escribo para hacer un pedido urgente de los siguientes productos:

DETALLES DEL PEDIDO:
- 50 unidades de Producto Premium A (Ref: PRD-001)
- 30 unidades de Producto Premium B (Ref: PRD-002)
- 20 unidades de Producto Premium C (Ref: PRD-003)
- 15 unidades de Producto Premium D (Ref: PRD-004)

INFORMACIÓN DE ENTREGA:
- Dirección: Calle Principal 123, Piso 5, Oficina 501
- Ciudad: Madrid
- Código Postal: 28001
- Teléfono: +34 91 123 4567

NOTAS ESPECIALES:
- Necesitamos entrega urgente (máximo 48 horas)
- Por favor, incluir factura proforma
- Solicitamos descuento por volumen (>100 unidades)

Total estimado: €2,500.00

Adjunto encontrarás:
1. Especificaciones técnicas de los productos
2. Fotos de referencia
3. Presupuesto anterior
4. Autorización de compra firmada
5. Vídeo demostrativo del producto

Quedo atento a cualquier duda.

Saludos cordiales,
Juan Carlos García López
Gerente de Compras
Cliente Premium XYZ S.L.
Teléfono: +34 91 123 4567
Email: juan.garcia@clientepremium.com""",
    "bodyHtml": """<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #003366; color: white; padding: 20px; }
        .content { padding: 20px; }
        .section { margin: 20px 0; border-left: 4px solid #003366; padding-left: 15px; }
        .product { background-color: #f0f0f0; padding: 10px; margin: 10px 0; }
        .footer { color: #666; font-size: 12px; margin-top: 30px; }
        strong { color: #003366; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Nuevo Pedido - Cliente Premium XYZ</h2>
    </div>
    <div class="content">
        <p>Hola equipo de Mundosol,</p>
        <p>Espero que se encuentren bien. Les escribo para hacer un <strong>pedido urgente</strong> de los siguientes productos:</p>
        
        <div class="section">
            <h3>📦 DETALLES DEL PEDIDO:</h3>
            <div class="product">
                <strong>50 unidades</strong> de Producto Premium A (Ref: PRD-001)
            </div>
            <div class="product">
                <strong>30 unidades</strong> de Producto Premium B (Ref: PRD-002)
            </div>
            <div class="product">
                <strong>20 unidades</strong> de Producto Premium C (Ref: PRD-003)
            </div>
            <div class="product">
                <strong>15 unidades</strong> de Producto Premium D (Ref: PRD-004)
            </div>
        </div>
        
        <div class="section">
            <h3>📍 INFORMACIÓN DE ENTREGA:</h3>
            <p>
                Dirección: Calle Principal 123, Piso 5, Oficina 501<br>
                Ciudad: Madrid<br>
                Código Postal: 28001<br>
                Teléfono: +34 91 123 4567
            </p>
        </div>
        
        <div class="section">
            <h3>⚠️ NOTAS ESPECIALES:</h3>
            <ul>
                <li>Necesitamos entrega urgente (máximo 48 horas)</li>
                <li>Por favor, incluir factura proforma</li>
                <li>Solicitamos descuento por volumen (&gt;100 unidades)</li>
            </ul>
        </div>
        
        <div class="section">
            <h3>💰 TOTAL ESTIMADO: €2,500.00</h3>
        </div>
        
        <div class="section">
            <h3>📎 ARCHIVOS ADJUNTOS:</h3>
            <ul>
                <li>✓ Especificaciones técnicas de los productos</li>
                <li>✓ Fotos de referencia</li>
                <li>✓ Presupuesto anterior</li>
                <li>✓ Autorización de compra firmada</li>
                <li>✓ Vídeo demostrativo del producto</li>
            </ul>
        </div>
        
        <p>Quedo atento a cualquier duda.</p>
        
        <div class="footer">
            <p>
                <strong>Juan Carlos García López</strong><br>
                Gerente de Compras<br>
                Cliente Premium XYZ S.L.<br>
                Teléfono: +34 91 123 4567<br>
                Email: juan.garcia@clientepremium.com
            </p>
        </div>
    </div>
</body>
</html>""",
    "receivedDateTime": datetime.now().isoformat(),
    "attachments": [
        {
            "name": "especificaciones_tecnicas.pdf",
            "contentType": "application/pdf",
            "size": 2500000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/especificaciones_tecnicas.pdf"
        },
        {
            "name": "fotos_productos.zip",
            "contentType": "application/zip",
            "size": 15000000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/fotos_productos.zip"
        },
        {
            "name": "foto_1.jpg",
            "contentType": "image/jpeg",
            "size": 3500000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/foto_1.jpg"
        },
        {
            "name": "foto_2.jpg",
            "contentType": "image/jpeg",
            "size": 4200000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/foto_2.jpg"
        },
        {
            "name": "foto_3.png",
            "contentType": "image/png",
            "size": 2800000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/foto_3.png"
        },
        {
            "name": "presupuesto_anterior.xlsx",
            "contentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "size": 850000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/presupuesto_anterior.xlsx"
        },
        {
            "name": "autorizacion_compra.pdf",
            "contentType": "application/pdf",
            "size": 1200000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/autorizacion_compra.pdf"
        },
        {
            "name": "video_demostrativo.mp4",
            "contentType": "video/mp4",
            "size": 125000000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/video_demostrativo.mp4"
        },
        {
            "name": "catalogo_productos.docx",
            "contentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "size": 5600000,
            "url": "https://outlook.office365.com/api/v2.0/me/messages/AAMkADU5NTk1/attachments/catalogo_productos.docx"
        }
    ],
    "prioridad": "alta"
}

print("=" * 60)
print("🧪 TEST WEBHOOK - Nuevo Pedido")
print("=" * 60)
print(f"\n📍 URL: {WEBHOOK_URL}")
print(f"🔐 Token: {WEBHOOK_TOKEN}")
print(f"\n📨 Datos de prueba:")
print(json.dumps(test_data, indent=2, default=str))

try:
    print("\n⏳ Enviando POST...")
    response = requests.post(WEBHOOK_URL, json=test_data, headers=headers)
    
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"📦 Response:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 201:
        print("\n✓ ¡Pedido creado exitosamente!")
        pedido_id = response.json().get('pedido_id')
        print(f"  ID del pedido: {pedido_id}")
    else:
        print(f"\n❌ Error: {response.json().get('error')}")
        
except Exception as e:
    print(f"\n❌ Error al enviar: {e}")

print("\n" + "=" * 60)
