"""
Mundosol - Sistema de Gestión de Pedidos
Archivo principal de ejecución
"""

from app import create_app, db
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Crear usuario admin por defecto si no existe
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("=" * 60)
            print("✓ Usuario administrador creado")
            print("  Usuario: admin")
            print("  Contraseña: admin123")
            print("  ⚠️  CAMBIAR CONTRASEÑA EN PRODUCCIÓN")
            print("=" * 60)
        else:
            print("=" * 60)
            print("✓ Base de datos inicializada")
            print("=" * 60)
    
    print("\n🚀 Iniciando servidor Mundosol...")
    print("📍 URL: http://localhost:5000")
    print("🔐 Login: admin / admin123\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
