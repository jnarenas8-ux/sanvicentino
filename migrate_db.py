"""
Script para migrar la base de datos a la nueva versión con el campo 'publicado'
"""

import os
import sys
import sqlite3
from pathlib import Path

# Agregar la carpeta app al path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

def migrate_database():
    """Migra la BD agregando la columna publicado si no existe"""
    
    db_path = Path(__file__).resolve().parent / "instance" / "sanvicentino.db"
    
    # Si la BD no existe aún, no hay nada que migrar
    if not db_path.exists():
        print("Base de datos no existe aún. Se creará en la próxima ejecución.")
        return
    
    print(f"Verificando base de datos en: {db_path}")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Obtener información de la tabla products
        cursor.execute("PRAGMA table_info(products)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'publicado' not in columns:
            print("Columna 'publicado' no encontrada. Agregando...")
            cursor.execute("ALTER TABLE products ADD COLUMN publicado BOOLEAN DEFAULT 0")
            conn.commit()
            print("✓ Columna 'publicado' agregada exitosamente")
            print("✓ Todos los productos existentes se marcaron como NO publicados (0)")
        else:
            print("✓ La columna 'publicado' ya existe en la tabla")
        
        # Verificar también que los productos de ejemplo estén publicados
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        
        if product_count > 0:
            # Marcar productos demo como publicados (primeros 6 son los de ejemplo)
            cursor.execute("""
                UPDATE products 
                SET publicado = 1 
                WHERE id <= 6 AND publicado = 0
            """)
            updated = cursor.rowcount
            if updated > 0:
                conn.commit()
                print(f"✓ {updated} productos marcados como publicados")
        
        conn.close()
        print("✓ Migración completada exitosamente")
        
    except sqlite3.OperationalError as e:
        print(f"✗ Error al migrar: {str(e)}")
        print("La base de datos podría estar corrupta. Considera eliminarla y reiniciar.")
    except Exception as e:
        print(f"✗ Error inesperado: {str(e)}")

if __name__ == "__main__":
    migrate_database()
