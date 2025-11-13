from flask import Blueprint, request, jsonify
from datetime import datetime
from dateutil import parser as date_parser
from app import db
from app.models import Pedido, HistorialPedido
from config import Config

webhooks_bp = Blueprint('webhooks', __name__, url_prefix='/webhook')


def validate_webhook_token():
    """Valida el token de webhook en el header"""
    token = request.headers.get('X-Webhook-Token')
    if token != Config.WEBHOOK_TOKEN:
        return False
    return True


@webhooks_bp.route('/pedido/nuevo', methods=['POST'])
def nuevo_pedido():
    """
    Recibe nuevo pedido desde n8n workflow con toda la información del correo.
    No requiere login pero valida token.
    """
    # Validar token
    if not validate_webhook_token():
        return jsonify({'error': 'Token de webhook inválido'}), 401
    
    try:
        data = request.get_json()
        
        # LOG: Mostrar datos recibidos
        print("\n" + "="*60)
        print("📨 WEBHOOK RECIBIDO")
        print("="*60)
        print(f"Headers: {dict(request.headers)}")
        print(f"Datos recibidos: {data}")
        print(f"Tipo de data: {type(data)}")
        if data:
            print(f"Claves en data: {list(data.keys())}")
            print(f"\n📋 DETALLES:")
            print(f"  messageId: {data.get('messageId')}")
            print(f"  subject: {data.get('subject')}")
            print(f"  body (primeros 100 chars): {str(data.get('body', ''))[:100]}")
            print(f"  bodyHtml (primeros 100 chars): {str(data.get('bodyHtml', ''))[:100]}")
            print(f"  bodyPlain (primeros 100 chars): {str(data.get('bodyPlain', ''))[:100]}")
            print(f"  from: {data.get('from')}")
            print(f"  attachments count: {len(data.get('attachments', []))}")
        print("="*60 + "\n")
        
        # Validar campos requeridos
        required_fields = ['messageId', 'subject', 'body']
        for field in required_fields:
            if field not in data:
                print(f"❌ Campo faltante: {field}")
                return jsonify({'error': f'Campo requerido faltante: {field}'}), 400
        
        # Verificar si el pedido ya existe
        existing = Pedido.query.filter_by(outlook_message_id=data['messageId']).first()
        if existing:
            return jsonify({
                'success': True,
                'message': 'Pedido ya existe',
                'pedido_id': existing.id
            }), 200
        
        # Extraer información del remitente
        from_data = data.get('from', {})
        if isinstance(from_data, dict):
            remitente_nombre = from_data.get('name', '')
            remitente_email = from_data.get('email', 'unknown@unknown.com')
            remitente = f"{remitente_nombre} <{remitente_email}>" if remitente_nombre else remitente_email
        else:
            remitente = str(from_data)
            remitente_email = str(from_data)
            remitente_nombre = ''
        
        # Parsear fecha del correo
        fecha_correo = None
        if data.get('receivedDateTime'):
            try:
                fecha_correo = date_parser.parse(data['receivedDateTime'])
            except Exception as e:
                print(f"⚠️  Error parseando fecha: {e}")
                fecha_correo = None
        
        # Procesar archivos adjuntos - validar que tengan contenido base64
        archivos_procesados = []
        archivos_raw = data.get('attachments', [])
        
        if isinstance(archivos_raw, list):
            for idx, archivo in enumerate(archivos_raw):
                if isinstance(archivo, dict):
                    # Validar que tenga contenido
                    if archivo.get('content') and archivo.get('encoding') == 'base64':
                        archivos_procesados.append({
                            'filename': archivo.get('filename', f'archivo_{idx}'),
                            'mimeType': archivo.get('mimeType', 'application/octet-stream'),
                            'size': archivo.get('size', 0),
                            'sizeKB': archivo.get('sizeKB', 0),
                            'type': archivo.get('type', 'otro'),
                            'content': archivo.get('content'),
                            'encoding': 'base64',
                            'isInline': archivo.get('isInline', False)
                        })
                        print(f"✅ Archivo procesado: {archivo.get('filename')} ({archivo.get('sizeKB', 0)} KB)")
                    else:
                        print(f"⚠️  Archivo sin contenido base64: {archivo.get('filename', f'archivo_{idx}')}")
        
        # Crear nuevo pedido con toda la información
        pedido = Pedido(
            outlook_message_id=data['messageId'],
            correo_origen=data.get('account', data.get('accountName', '')),
            remitente_nombre=remitente_nombre,
            remitente_email=remitente_email,
            remitente=remitente,
            asunto=data['subject'],
            contenido=data.get('bodyPlain', data.get('body', data.get('bodyPreview', ''))),
            contenido_html=data.get('bodyHtml', data.get('body', '')).encode('utf-8') if data.get('bodyHtml', data.get('body', '')) else None,
            archivos_adjuntos=archivos_procesados,
            fecha_correo=fecha_correo,
            tipo_mensaje=data.get('tipoMensaje', 'nuevo'),
            es_respuesta=data.get('esRespuesta', False),
            es_reenviado=data.get('esReenviado', False),
            destinatarios_cc=data.get('cc', []),
            destinatarios_bcc=data.get('bcc', []),
            es_leido=data.get('isRead', False),
            conversation_id=data.get('conversationId'),
            conversation_topic=data.get('conversationTopic'),
            parent_message_id=data.get('parentMessageId'),
            in_reply_to=data.get('inReplyTo'),
            prioridad=data.get('importance', 'normal'),
            estado='pendiente'
        )
        
        db.session.add(pedido)
        db.session.flush()  # Para obtener el ID
        
        # LOG: Mostrar qué se guardó
        print(f"\n✅ PEDIDO CREADO:")
        print(f"  ID: {pedido.id}")
        print(f"  Asunto: {pedido.asunto}")
        print(f"  Remitente: {pedido.remitente}")
        print(f"  Contenido (primeros 100 chars): {pedido.contenido[:100]}")
        print(f"  Contenido HTML (primeros 100 chars): {str(pedido.contenido_html)[:100]}")
        print(f"  Archivos: {len(pedido.archivos_adjuntos)}")
        print()
        
        # Crear entrada en historial
        detalles = f'Pedido recibido desde Outlook\n'
        detalles += f'Cuenta: {pedido.correo_origen}\n'
        detalles += f'De: {remitente}\n'
        if data.get('attachments'):
            detalles += f'Archivos adjuntos: {len(data["attachments"])}'
        
        historial = HistorialPedido(
            pedido_id=pedido.id,
            usuario_id=None,
            accion='creado',
            detalles=detalles
        )
        
        db.session.add(historial)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido creado correctamente',
            'pedido_id': pedido.id,
            'remitente': remitente,
            'cuenta_origen': pedido.correo_origen
        }), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear pedido: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@webhooks_bp.route('/pedido/outlook-actualizado', methods=['POST'])
def outlook_actualizado():
    """
    Confirmación desde n8n de que Outlook fue actualizado.
    No requiere login pero valida token.
    """
    # Validar token
    if not validate_webhook_token():
        return jsonify({'error': 'Token de webhook inválido'}), 401
    
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if 'message_id' not in data:
            return jsonify({'error': 'Campo message_id requerido'}), 400
        
        # Buscar pedido
        pedido = Pedido.query.filter_by(outlook_message_id=data['message_id']).first()
        if not pedido:
            return jsonify({'error': 'Pedido no encontrado'}), 404
        
        # Crear entrada en historial
        detalles = 'Outlook actualizado correctamente'
        if 'estado' in data:
            detalles += f' - Estado: {data["estado"]}'
        
        historial = HistorialPedido(
            pedido_id=pedido.id,
            usuario_id=None,
            accion='outlook_actualizado',
            detalles=detalles
        )
        
        db.session.add(historial)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Confirmación registrada'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        print(f"Error al procesar confirmación: {e}")
        return jsonify({'error': str(e)}), 500
