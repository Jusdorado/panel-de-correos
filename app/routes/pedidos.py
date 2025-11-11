from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime
import requests
from app import db
from app.models import Pedido, User, HistorialPedido
from app.auth import role_required
from config import Config

pedidos_bp = Blueprint('pedidos', __name__)


@pedidos_bp.route('/dashboard')
@login_required
def dashboard():
    """Vista principal tipo inbox con filtros"""
    # Obtener parámetros de filtrado
    estado_filter = request.args.get('estado', '')
    asignado_a_filter = request.args.get('asignado_a', '')
    buscar = request.args.get('buscar', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    # Query base
    query = Pedido.query
    
    # Aplicar filtros según rol
    if current_user.role == 'usuario':
        # Usuarios normales solo ven sus pedidos asignados
        query = query.filter(Pedido.asignado_a_id == current_user.id)
    
    # Filtro por estado
    if estado_filter:
        query = query.filter(Pedido.estado == estado_filter)
    
    # Filtro por asignado a
    if asignado_a_filter:
        if asignado_a_filter == 'mis_asignaciones':
            query = query.filter(Pedido.asignado_a_id == current_user.id)
        else:
            query = query.filter(Pedido.asignado_a_id == int(asignado_a_filter))
    
    # Búsqueda por texto
    if buscar:
        search_term = f'%{buscar}%'
        query = query.filter(
            or_(
                Pedido.remitente.ilike(search_term),
                Pedido.asunto.ilike(search_term),
                Pedido.contenido.ilike(search_term)
            )
        )
    
    # Ordenar por fecha de recepción descendente
    query = query.order_by(Pedido.fecha_recepcion.desc())
    
    # Paginación
    pedidos_paginados = query.paginate(page=page, per_page=per_page, error_out=False)
    pedidos = pedidos_paginados.items
    
    # Contar pedidos por estado (para badges en sidebar)
    if current_user.role == 'usuario':
        base_count_query = Pedido.query.filter(Pedido.asignado_a_id == current_user.id)
    else:
        base_count_query = Pedido.query
    
    counts = {
        'pendiente': base_count_query.filter(Pedido.estado == 'pendiente').count(),
        'asignado': base_count_query.filter(Pedido.estado == 'asignado').count(),
        'completado': base_count_query.filter(Pedido.estado == 'completado').count(),
        'archivado': base_count_query.filter(Pedido.estado == 'archivado').count(),
        'total': base_count_query.count()
    }
    
    # Obtener usuarios de logística para asignación
    usuarios_logistica = User.query.filter(
        User.role.in_(['logistica', 'admin']),
        User.is_active == True
    ).all()
    
    return render_template(
        'dashboard.html',
        pedidos=pedidos,
        counts=counts,
        usuarios_logistica=usuarios_logistica,
        pagination=pedidos_paginados,
        estado_filter=estado_filter,
        asignado_a_filter=asignado_a_filter,
        buscar=buscar
    )


@pedidos_bp.route('/pedidos/<int:pedido_id>/detalle')
@login_required
def detalle_pedido(pedido_id):
    """Retorna HTML parcial con detalle completo del pedido"""
    pedido = Pedido.query.get_or_404(pedido_id)
    
    # Todos pueden ver los detalles de cualquier pedido
    # Las restricciones de acción se manejan en el template y en las rutas de acción
    
    # Obtener historial ordenado
    historial = pedido.historial.order_by(HistorialPedido.timestamp.desc()).all()
    
    # Obtener usuarios de logística para asignación
    usuarios_logistica = User.query.filter(
        User.role.in_(['logistica', 'admin']),
        User.is_active == True
    ).all()
    
    return render_template(
        'pedidos/detalle.html',
        pedido=pedido,
        historial=historial,
        usuarios_logistica=usuarios_logistica
    )


@pedidos_bp.route('/pedidos/<int:pedido_id>/asignar', methods=['POST'])
@login_required
@role_required('admin', 'logistica')
def asignar_pedido(pedido_id):
    """Asignar pedido a un usuario de logística"""
    pedido = Pedido.query.get_or_404(pedido_id)
    
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'error': 'Debe especificar un usuario'}), 400
    
    usuario = User.query.get(usuario_id)
    if not usuario or usuario.role not in ['logistica', 'admin']:
        return jsonify({'error': 'Usuario no válido'}), 400
    
    try:
        # Actualizar pedido
        pedido.estado = 'asignado'
        pedido.asignado_a_id = usuario_id
        pedido.fecha_asignacion = datetime.utcnow()
        
        # Crear entrada en historial
        historial = HistorialPedido(
            pedido_id=pedido.id,
            usuario_id=current_user.id,
            accion='asignado',
            detalles=f'Asignado a {usuario.username}'
        )
        
        db.session.add(historial)
        db.session.commit()
        
        # Llamar webhook de n8n para actualizar Outlook
        try:
            webhook_url = f"{Config.N8N_WEBHOOK_URL}/actualizar-outlook"
            payload = {
                'message_id': pedido.outlook_message_id,
                'estado': 'asignado',
                'asignado_a': usuario.username
            }
            requests.post(webhook_url, json=payload, timeout=5)
        except Exception as e:
            print(f"Error al llamar webhook n8n: {e}")
            # No fallar la operación si el webhook falla
        
        return jsonify({
            'success': True,
            'message': f'Pedido asignado a {usuario.username}',
            'pedido': {
                'id': pedido.id,
                'estado': pedido.estado,
                'asignado_a': usuario.username
            }
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@pedidos_bp.route('/pedidos/<int:pedido_id>/completar', methods=['POST'])
@login_required
def completar_pedido(pedido_id):
    """Marcar pedido como completado"""
    pedido = Pedido.query.get_or_404(pedido_id)
    
    # Verificar permisos: 
    # - Admin puede completar cualquier pedido
    # - Logística solo puede completar si está asignado a ellos
    # - Usuario solo puede completar si está asignado a ellos
    if current_user.role != 'admin':
        if pedido.asignado_a_id != current_user.id:
            return jsonify({'error': 'No tienes permiso para completar este pedido. Solo el usuario asignado o un administrador puede hacerlo.'}), 403
    
    if pedido.estado == 'completado':
        return jsonify({'error': 'El pedido ya está completado'}), 400
    
    data = request.get_json()
    respuesta_email = data.get('respuesta_email', '').strip()
    
    try:
        # Actualizar pedido
        pedido.estado = 'completado'
        pedido.completado_por_id = current_user.id
        pedido.fecha_completado = datetime.utcnow()
        pedido.respuesta_enviada = respuesta_email if respuesta_email else None
        
        # Crear entrada en historial
        detalles = f'Completado por {current_user.username}'
        if respuesta_email:
            detalles += f'\nRespuesta: {respuesta_email[:100]}...'
        
        historial = HistorialPedido(
            pedido_id=pedido.id,
            usuario_id=current_user.id,
            accion='completado',
            detalles=detalles
        )
        
        db.session.add(historial)
        db.session.commit()
        
        # Llamar webhook de n8n para completar pedido
        try:
            webhook_url = f"{Config.N8N_WEBHOOK_URL}/completar-pedido"
            payload = {
                'message_id': pedido.outlook_message_id,
                'estado': 'completado',
                'respuesta': respuesta_email
            }
            requests.post(webhook_url, json=payload, timeout=5)
        except Exception as e:
            print(f"Error al llamar webhook n8n: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Pedido completado correctamente',
            'pedido': {
                'id': pedido.id,
                'estado': pedido.estado,
                'completado_por': current_user.username
            }
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@pedidos_bp.route('/pedidos/<int:pedido_id>/archivar', methods=['POST'])
@login_required
@role_required('admin')
def archivar_pedido(pedido_id):
    """Archivar pedido (solo admin)"""
    pedido = Pedido.query.get_or_404(pedido_id)
    
    try:
        # Actualizar pedido
        pedido.estado = 'archivado'
        
        # Crear entrada en historial
        historial = HistorialPedido(
            pedido_id=pedido.id,
            usuario_id=current_user.id,
            accion='archivado',
            detalles=f'Archivado por {current_user.username}'
        )
        
        db.session.add(historial)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido archivado correctamente',
            'pedido': {
                'id': pedido.id,
                'estado': pedido.estado
            }
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@pedidos_bp.route('/pedidos/historial')
@login_required
def historial():
    """Vista de historial de pedidos"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    # Query base según rol
    if current_user.role == 'usuario':
        query = Pedido.query.filter(Pedido.asignado_a_id == current_user.id)
    else:
        query = Pedido.query
    
    # Solo pedidos completados o archivados
    query = query.filter(Pedido.estado.in_(['completado', 'archivado']))
    query = query.order_by(Pedido.fecha_completado.desc())
    
    pedidos_paginados = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'pedidos/historial.html',
        pedidos=pedidos_paginados.items,
        pagination=pedidos_paginados
    )
