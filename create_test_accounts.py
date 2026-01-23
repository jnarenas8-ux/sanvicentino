#!/usr/bin/env python3
"""
Script para crear cuentas de usuario (Admin y Cliente)
"""

import os
import sys
from pathlib import Path

# Agregar el directorio de la app al path
sys.path.insert(0, str(Path(__file__).parent / "app"))

# Configurar variables de entorno
os.environ['FLASK_ENV'] = 'development'

from run import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_accounts():
    """Crea cuentas de admin y cliente para pruebas"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("👥 CREADOR DE CUENTAS - SAN VICENTINO")
        print("="*60)
        
        # Crear tabla si no existe
        db.create_all()
        
        # Admin account
        admin_email = "admin.sanvicentino@gmail.com"
        admin_user = User.query.filter_by(email=admin_email).first()
        
        if not admin_user:
            admin = User(
                username="Administrador",
                email=admin_email,
                password=generate_password_hash("Admin@123456"),
                is_admin=True,
                provider="local"
            )
            db.session.add(admin)
            print(f"\n✅ Cuenta Admin creada:")
            print(f"   📧 Email: {admin_email}")
            print(f"   🔐 Contraseña: Admin@123456")
            print(f"   🎯 Rol: Administrador (puede crear y editar productos)")
        else:
            print(f"\n⚠️  La cuenta admin ya existe: {admin_email}")
        
        # Cliente account (usando la que proporcionaste)
        cliente_email = "admin@sanvicentino.com"
        cliente_user = User.query.filter_by(email=cliente_email).first()
        
        if not cliente_user:
            cliente = User(
                username="Cliente",
                email=cliente_email,
                password=generate_password_hash("Cliente@123456"),
                is_admin=False,
                provider="local"
            )
            db.session.add(cliente)
            print(f"\n✅ Cuenta Cliente creada:")
            print(f"   📧 Email: {cliente_email}")
            print(f"   🔐 Contraseña: Cliente@123456")
            print(f"   🎯 Rol: Cliente (solo puede ver productos y comprar)")
        else:
            print(f"\n⚠️  La cuenta cliente ya existe: {cliente_email}")
        
        # Commit changes
        db.session.commit()
        
        print("\n" + "-"*60)
        print("📝 DIFERENCIAS ENTRE CUENTAS:")
        print("-"*60)
        print("\n🔑 ADMIN (admin.sanvicentino@gmail.com):")
        print("   ✓ Ve menú desplegable '⚙️ Admin'")
        print("   ✓ Puede crear nuevos productos")
        print("   ✓ Puede editar productos")
        print("   ✓ Puede eliminar productos")
        print("   ✓ Puede publicar/despublicar productos")
        
        print("\n👤 CLIENTE (admin@sanvicentino.com):")
        print("   ✓ NO ve el menú de Admin")
        print("   ✓ Solo ve productos publicados")
        print("   ✓ Puede agregar productos al carrito")
        print("   ✓ Puede hacer compras")
        print("   ✓ Puede ver sus órdenes")
        
        print("\n" + "="*60)
        print("✨ ¡Cuentas configuradas correctamente!")
        print("="*60 + "\n")

if __name__ == "__main__":
    create_accounts()
