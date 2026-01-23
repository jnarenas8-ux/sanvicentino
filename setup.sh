#!/bin/bash
# Script de configuración rápida para el carrito de compras

echo "=========================================="
echo "Configuración Rápida - Carrito San Vicentino"
echo "=========================================="
echo ""

# Verificar si estamos en la carpeta correcta
if [ ! -f "app/run.py" ]; then
    echo "❌ Error: Ejecuta este script desde la carpeta raíz del proyecto"
    exit 1
fi

echo "📦 Paso 1: Verificando dependencias..."
pip list | grep -q flask
if [ $? -ne 0 ]; then
    echo "📥 Instalando dependencias..."
    pip install -r app/requirements.txt
else
    echo "✅ Dependencias ya instaladas"
fi

echo ""
echo "🗄️  Paso 2: Inicializando base de datos..."
python init_db.py

if [ $? -ne 0 ]; then
    echo "❌ Error al inicializar la base de datos"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Configuración completada exitosamente"
echo "=========================================="
echo ""
echo "Para iniciar la aplicación, ejecuta:"
echo "  python app/run.py"
echo ""
echo "Luego accede a: http://localhost:5000"
echo ""
echo "Credenciales de admin:"
echo "  Email: admin@sanvicentino.com"
echo "  Contraseña: admin123"
echo ""
echo "⚠️  Recuerda cambiar la contraseña después de iniciar sesión"
echo ""
