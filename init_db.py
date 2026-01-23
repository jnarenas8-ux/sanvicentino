"""
Script para inicializar la base de datos y crear un usuario administrador
Ejecutar: python init_db.py
"""

import os
import sys
from pathlib import Path

# Agregar la carpeta app al path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

# Crear carpeta instance si no existe
instance_path = Path(__file__).resolve().parent / "instance"
instance_path.mkdir(exist_ok=True)

from run import app, db
from models import User, Product
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def init_database():
    """Inicializa la base de datos y crea las tablas"""
    with app.app_context():
        print("Creando tablas de la base de datos...")
        db.create_all()
        print("✓ Tablas creadas correctamente")

def create_admin_user():
    """Crea un usuario administrador por defecto"""
    with app.app_context():
        # Verificar si ya existe un admin
        admin = User.query.filter_by(email="admin@sanvicentino.com").first()
        
        if admin:
            print("✓ Usuario administrador ya existe")
            return
        
        print("\n📋 Creando usuario administrador...")
        admin = User(
            username="admin",
            email="admin@sanvicentino.com",
            password=generate_password_hash("admin123"),
            provider="local",
            is_admin=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("✓ Usuario administrador creado:")
        print("  Email: admin@sanvicentino.com")
        print("  Contraseña: admin123")
        print("  ⚠️  IMPORTANTE: Cambia esta contraseña después de iniciar sesión")

def create_sample_products():
    """Crea algunos productos de ejemplo"""
    with app.app_context():
        # Verificar si ya existen productos
        if Product.query.first():
            print("✓ Ya existen productos en la base de datos")
            return
        
        print("\n📦 Creando productos de ejemplo...")
        
        products = [
            {
                "nombre": "Agua Purificada 500ml",
                "descripcion": "Agua purificada de alta calidad, ideal para hidratación diaria",
                "precio": 1.50,
                "categoria": "Agua",
                "imagen": "https://via.placeholder.com/300x300?text=Agua+500ml",
                "stock": 100
            },
            {
                "nombre": "Agua Natural 1L",
                "descripcion": "Agua mineral natural con minerales esenciales",
                "precio": 2.50,
                "categoria": "Agua",
                "imagen": "https://via.placeholder.com/300x300?text=Agua+1L",
                "stock": 80
            },
            {
                "nombre": "Jugo de Naranja 1L",
                "descripcion": "Jugo de naranja natural 100% sin azúcar añadida",
                "precio": 4.50,
                "categoria": "Bebidas",
                "imagen": "https://via.placeholder.com/300x300?text=Jugo+Naranja",
                "stock": 50
            },
            {
                "nombre": "Refresco Fresa 500ml",
                "descripcion": "Refresco refrescante con sabor a fresa natural",
                "precio": 3.00,
                "categoria": "Bebidas",
                "imagen": "https://via.placeholder.com/300x300?text=Refresco+Fresa",
                "stock": 60
            },
            {
                "nombre": "Yogur Natural 180g",
                "descripcion": "Yogur natural con probióticos vivos",
                "precio": 2.00,
                "categoria": "Lácteos",
                "imagen": "https://via.placeholder.com/300x300?text=Yogur",
                "stock": 40
            },
            {
                "nombre": "Queso Fresco 200g",
                "descripcion": "Queso fresco de calidad premium",
                "precio": 8.00,
                "categoria": "Lácteos",
                "imagen": "https://via.placeholder.com/300x300?text=Queso",
                "stock": 30
            }
        ]
        
        for product_data in products:
            product_data['publicado'] = True  # Los productos de ejemplo se crean publicados
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f"✓ {len(products)} productos de ejemplo creados")

def main():
    """Función principal"""
    print("=" * 50)
    print("Inicializando Base de Datos - San Vicentino")
    print("=" * 50)
    
    try:
        init_database()
        create_admin_user()
        create_sample_products()
        
        print("\n" + "=" * 50)
        print("✓ Inicialización completada exitosamente")
        print("=" * 50)
        print("\nPróximos pasos:")
        print("1. Inicia la aplicación: python app/run.py")
        print("2. Accede a: http://localhost:5000")
        print("3. Inicia sesión con las credenciales del admin")
        print("4. Cambia la contraseña del admin")
        print("\n¡Bienvenido a San Vicentino Online!")
        
    except Exception as e:
        print(f"\n✗ Error durante la inicialización: {str(e)}")
        print("Por favor, verifica tu configuración y vuelve a intentar")
        sys.exit(1)

if __name__ == "__main__":
    main()
