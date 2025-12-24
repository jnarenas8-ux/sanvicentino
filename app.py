#importaciones
from flask import Flask , render_template
from flask_tailwind import Tailwind    
#inicializacion de la plicacion
app = Flask(__name__)
# Configuración de Tailwind
Tailwind = Tailwind(app)
# Rutas de la aplicación
@app.route('/')

def index():
    productos = [
        {"nombre": "Smartphone X", "precio": 1200, "imagen": "https://via.placeholder.com/150", "categoria": "Tecnología"},
        {"nombre": "Vestido Mujer", "precio": 85, "imagen": "https://via.placeholder.com/150", "categoria": "Mujer"},
        {"nombre": "Zapatos Hombre", "precio": 100, "imagen": "https://via.placeholder.com/150", "categoria": "Hombre"},
        {"nombre": "Juguetes Niños", "precio": 55, "imagen": "https://via.placeholder.com/150", "categoria": "Moda Infantil"},
        {"nombre": "Refrigeradora", "precio": 1450, "imagen": "https://via.placeholder.com/150", "categoria": "Electrodomésticos"},
        {"nombre": "Bebida Energética", "precio": 7, "imagen": "https://via.placeholder.com/150", "categoria": "Bebidas"},
    ]
    return render_template('index.html', productos=productos)

#prender la aplicación
if __name__ == "__main__":
    app.run(debug=True)
