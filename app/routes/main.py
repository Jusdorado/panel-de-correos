from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Redirige al dashboard si está autenticado, sino al login"""
    if current_user.is_authenticated:
        return redirect(url_for('pedidos.dashboard'))
    return redirect(url_for('main.login'))


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Formulario de login y validación de credenciales"""
    if current_user.is_authenticated:
        return redirect(url_for('pedidos.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Por favor ingresa usuario y contraseña', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('login.html')
        
        if not user.is_active:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'warning')
            return render_template('login.html')
        
        login_user(user, remember=remember)
        
        # Redirigir a la página solicitada o al dashboard
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        
        flash(f'Bienvenido, {user.username}!', 'success')
        return redirect(url_for('pedidos.dashboard'))
    
    return render_template('login.html')


@main_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('main.login'))
