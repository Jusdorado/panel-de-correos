from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=Config):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    # Registrar user_loader
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    from app.routes.main import main_bp
    from app.routes.pedidos import pedidos_bp
    from app.routes.webhooks import webhooks_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(webhooks_bp)
    app.register_blueprint(admin_bp)
    
    # Registrar filtros Jinja personalizados
    from datetime import datetime
    import re
    
    @app.template_filter('timeago')
    def timeago_filter(dt):
        """Convierte datetime a formato relativo (hace X tiempo)"""
        if not dt:
            return ''
        
        now = datetime.utcnow()
        diff = now - dt
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return 'hace un momento'
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f'hace {minutes} minuto{"s" if minutes != 1 else ""}'
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f'hace {hours} hora{"s" if hours != 1 else ""}'
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f'hace {days} día{"s" if days != 1 else ""}'
        else:
            weeks = int(seconds / 604800)
            return f'hace {weeks} semana{"s" if weeks != 1 else ""}'
    
    @app.template_filter('fix_email_html')
    def fix_email_html(html_content):
        """Procesa HTML de correo para asegurar que las imágenes base64 se rendericen correctamente y los enlaces abran en nueva pestaña"""
        if not html_content:
            return ''
        
        # Asegurar que las imágenes base64 tengan el formato correcto
        html_content = re.sub(
            r'src\s*=\s*["\']?data:image/([^;]+);base64,([A-Za-z0-9+/=]+)["\']?',
            r'src="data:image/\1;base64,\2"',
            html_content,
            flags=re.IGNORECASE
        )
        
        # Agregar target="_blank" a TODOS los enlaces <a>
        # Primero, agregar target="_blank" a los que no tienen target
        html_content = re.sub(
            r'<a\s+([^>]*?)href\s*=\s*["\']([^"\']*)["\']([^>]*)>',
            lambda m: f'<a {m.group(1)}href="{m.group(2)}" target="_blank"{m.group(3)}>' if 'target' not in m.group(0).lower() else m.group(0),
            html_content,
            flags=re.IGNORECASE
        )
        
        # Segundo, reemplazar cualquier target existente que no sea "_blank" por "_blank"
        html_content = re.sub(
            r'target\s*=\s*["\']([^"\']*)["\']',
            r'target="_blank"',
            html_content,
            flags=re.IGNORECASE
        )
        
        return html_content
    
    # Manejadores de errores
    @app.errorhandler(403)
    def forbidden(e):
        return {'error': 'No tienes permisos para acceder a este recurso'}, 403
    
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Recurso no encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return {'error': 'Error interno del servidor'}, 500
    
    return app
