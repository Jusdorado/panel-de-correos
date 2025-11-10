from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """Modelo de usuario del sistema"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='usuario', nullable=False)  # 'admin', 'logistica', 'usuario'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    pedidos_asignados = db.relationship('Pedido', foreign_keys='Pedido.asignado_a_id', backref='asignado_a', lazy='dynamic')
    pedidos_completados = db.relationship('Pedido', foreign_keys='Pedido.completado_por_id', backref='completado_por', lazy='dynamic')
    historial = db.relationship('HistorialPedido', backref='usuario', lazy='dynamic')
    
    def set_password(self, password):
        """Genera hash de contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Pedido(db.Model):
    """Modelo de pedido recibido desde Outlook"""
    __tablename__ = 'pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    outlook_message_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    remitente = db.Column(db.String(255), nullable=False)
    asunto = db.Column(db.String(500), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    archivos_adjuntos = db.Column(db.JSON, default=list)  # Lista de {filename, url}
    
    estado = db.Column(db.String(20), default='pendiente', nullable=False, index=True)  # 'pendiente', 'asignado', 'completado', 'archivado'
    prioridad = db.Column(db.String(10), default='normal', nullable=False)  # 'baja', 'normal', 'alta'
    
    asignado_a_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    fecha_asignacion = db.Column(db.DateTime, nullable=True)
    
    completado_por_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    fecha_completado = db.Column(db.DateTime, nullable=True)
    respuesta_enviada = db.Column(db.Text, nullable=True)
    
    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relaciones
    historial = db.relationship('HistorialPedido', backref='pedido', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Pedido {self.id} - {self.asunto[:30]}>'


class HistorialPedido(db.Model):
    """Modelo de auditoría de cambios en pedidos"""
    __tablename__ = 'historial_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    accion = db.Column(db.String(50), nullable=False)  # 'creado', 'asignado', 'completado', 'archivado', 'outlook_actualizado'
    detalles = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<HistorialPedido {self.id} - {self.accion}>'
