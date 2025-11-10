from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.auth import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/users')
@login_required
@role_required('admin')
def users():
    """Listar todos los usuarios (solo admin)"""
    usuarios = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', usuarios=usuarios)


@admin_bp.route('/users/create', methods=['POST'])
@login_required
@role_required('admin')
def create_user():
    """Crear nuevo usuario (solo admin)"""
    data = request.get_json()
    
    # Validar campos requeridos
    required_fields = ['username', 'email', 'password', 'role']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Campo requerido: {field}'}), 400
    
    username = data['username'].strip()
    email = data['email'].strip()
    password = data['password']
    role = data['role']
    
    # Validar rol
    if role not in ['admin', 'logistica', 'usuario']:
        return jsonify({'error': 'Rol inválido'}), 400
    
    # Verificar si el usuario ya existe
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'El nombre de usuario ya existe'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    try:
        # Crear usuario
        user = User(
            username=username,
            email=email,
            role=role,
            is_active=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Usuario {username} creado correctamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_user(user_id):
    """Editar usuario (solo admin)"""
    user = User.query.get_or_404(user_id)
    
    # No permitir que el admin se desactive a sí mismo
    if user.id == current_user.id and 'is_active' in request.json and not request.json['is_active']:
        return jsonify({'error': 'No puedes desactivar tu propia cuenta'}), 400
    
    data = request.get_json()
    
    try:
        # Actualizar campos permitidos
        if 'username' in data and data['username'].strip():
            new_username = data['username'].strip()
            # Verificar que no exista otro usuario con ese username
            existing = User.query.filter(User.username == new_username, User.id != user_id).first()
            if existing:
                return jsonify({'error': 'El nombre de usuario ya existe'}), 400
            user.username = new_username
        
        if 'email' in data and data['email'].strip():
            new_email = data['email'].strip()
            # Verificar que no exista otro usuario con ese email
            existing = User.query.filter(User.email == new_email, User.id != user_id).first()
            if existing:
                return jsonify({'error': 'El email ya está registrado'}), 400
            user.email = new_email
        
        if 'role' in data:
            if data['role'] not in ['admin', 'logistica', 'usuario']:
                return jsonify({'error': 'Rol inválido'}), 400
            # No permitir que el admin cambie su propio rol
            if user.id == current_user.id:
                return jsonify({'error': 'No puedes cambiar tu propio rol'}), 400
            user.role = data['role']
        
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Usuario {user.username} actualizado correctamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active
            }
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@login_required
@role_required('admin')
def reset_password(user_id):
    """Resetear contraseña de usuario (solo admin)"""
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    
    if 'new_password' not in data or not data['new_password']:
        return jsonify({'error': 'Nueva contraseña requerida'}), 400
    
    new_password = data['new_password']
    
    if len(new_password) < 6:
        return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
    
    try:
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Contraseña de {user.username} actualizada correctamente'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>/delete', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_user(user_id):
    """Eliminar usuario (solo admin)"""
    user = User.query.get_or_404(user_id)
    
    # No permitir que el admin se elimine a sí mismo
    if user.id == current_user.id:
        return jsonify({'error': 'No puedes eliminar tu propia cuenta'}), 400
    
    try:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Usuario {username} eliminado correctamente'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
