from flask import Blueprint, request, jsonify
from datetime import datetime
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
        
        # Validar campos requeridos
        required_fields = ['messageId', 'subject', 'body']
        for field in required_fields:
            if field not in data:
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
        
        # Crear nuevo pedido con toda la información
        pedido = Pedido(
            outlook_message_id=data['messageId'],
            correo_origen=data.get('account', data.get('accountName', '')),
            remitente_nombre=remitente_nombre,
            remitente_email=remitente_email,
            remitente=remitente,
            asunto=data['subject'],
            contenido=data.get('body', data.get('bodyPreview', '')),
            contenido_html=data.get('bodyHtml'),
            archivos_adjuntos=data.get('attachments', []),
            fecha_correo=data.get('receivedDateTime'),
            prioridad=data.get('prioridad', 'normal'),
            estado='pendiente'
        )
        
        db.session.add(pedido)
        db.session.flush()  # Para obtener el ID
        
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
