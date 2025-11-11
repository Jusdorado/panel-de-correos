"""
Script para insertar usuarios de logística de prueba
"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Datos de usuarios de logística
    usuarios_logistica = [
        {'username': 'logistica1', 'password': 'logistica123'},
        {'username': 'logistica2', 'password': 'logistica123'},
        {'username': 'logistica3', 'password': 'logistica123'},
        {'username': 'logistica4', 'password': 'logistica123'},
        {'username': 'logistica5', 'password': 'logistica123'},
        {'username': 'logistica6', 'password': 'logistica123'},
        {'username': 'logistica7', 'password': 'logistica123'},
        {'username': 'logistica8', 'password': 'logistica123'},
        {'username': 'logistica9', 'password': 'logistica123'},
        {'username': 'logistica10', 'password': 'logistica123'},
    ]
    
    for usuario_data in usuarios_logistica:
        # Verificar si el usuario ya existe
        existing = User.query.filter_by(username=usuario_data['username']).first()
        if existing:
            print(f"⚠️  Usuario {usuario_data['username']} ya existe")
            continue
        
        # Crear usuario
        user = User(
            username=usuario_data['username'],
            role='logistica',
            is_active=True
        )
        user.set_password(usuario_data['password'])
        
        db.session.add(user)
        print(f"✓ Usuario {usuario_data['username']} creado")
    
    try:
        db.session.commit()
        print("\n" + "=" * 60)
        print("✓ 10 usuarios de logística creados correctamente")
        print("=" * 60)
        print("\nCredenciales de acceso:")
        print("Usuario: logistica1 - logistica10")
        print("Contraseña: logistica123")
        print("=" * 60)
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al crear usuarios: {e}")
