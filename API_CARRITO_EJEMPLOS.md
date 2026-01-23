# API del Carrito de Compras - Ejemplos de Uso

## 🔗 Endpoints REST

### 1. Agregar Producto al Carrito

**Endpoint:**
```
POST /carrito/agregar/<product_id>
```

**Autenticación:** Requerida ✅

**Ejemplo con JavaScript:**
```javascript
async function agregarAlCarrito(productId) {
    const response = await fetch(`/carrito/agregar/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    const data = await response.json();
    
    if (data.success) {
        console.log('Producto agregado:', data);
        // data.cart_count - Número de items en el carrito
        // data.cart_total - Total del carrito
    }
}
```

**Respuesta Exitosa (200):**
```json
{
    "success": true,
    "message": "Producto agregado al carrito",
    "cart_count": 3,
    "cart_total": 150.50
}
```

**Posibles Errores:**
- 404: Producto no encontrado
- 400: Producto agotado o stock insuficiente

---

### 2. Actualizar Cantidad

**Endpoint:**
```
POST /carrito/actualizar/<item_id>
```

**Parámetros JSON:**
```json
{
    "quantity": 5
}
```

**Ejemplo:**
```javascript
async function actualizarCantidad(itemId, cantidad) {
    const response = await fetch(`/carrito/actualizar/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity: cantidad })
    });
    
    const data = await response.json();
    console.log('Carrito actualizado:', data.cart_total);
}
```

**Respuesta:**
```json
{
    "success": true,
    "message": "Carrito actualizado",
    "cart_count": 5,
    "cart_total": 200.00,
    "subtotal": 180.50
}
```

---

### 3. Eliminar Producto del Carrito

**Endpoint:**
```
POST /carrito/eliminar/<item_id>
```

**Ejemplo:**
```javascript
async function eliminarDelCarrito(itemId) {
    const response = await fetch(`/carrito/eliminar/${itemId}`, {
        method: 'POST'
    });
    
    const data = await response.json();
    if (data.success) {
        // Remover elemento del DOM
        document.getElementById(`item-${itemId}`).remove();
    }
}
```

**Respuesta:**
```json
{
    "success": true,
    "message": "Producto eliminado del carrito",
    "cart_count": 2,
    "cart_total": 100.00
}
```

---

### 4. Vaciar Carrito

**Endpoint:**
```
POST /carrito/vaciar
```

**Ejemplo:**
```javascript
async function vaciarCarrito() {
    if (!confirm('¿Vaciar carrito?')) return;
    
    const response = await fetch('/carrito/vaciar', {
        method: 'POST'
    });
    
    const data = await response.json();
    if (data.success) {
        location.reload(); // Recargar página
    }
}
```

---

### 5. Procesar Pago

**Endpoint:**
```
POST /procesar-pago
```

**Parámetros JSON:**
```json
{
    "payment_method": "yape"  // o "tarjeta"
}
```

**Ejemplo:**
```javascript
async function procesarPago(metodoPago) {
    const response = await fetch('/procesar-pago', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            payment_method: metodoPago
        })
    });
    
    const data = await response.json();
    
    if (data.success) {
        console.log('Orden creada:', data.order_number);
        console.log('ID Orden:', data.order_id);
        // Proceder a confirmar pago
    }
}
```

**Respuesta:**
```json
{
    "success": true,
    "order_id": 1,
    "order_number": "ORD-1-1642000000",
    "message": "Orden creada exitosamente"
}
```

---

### 6. Confirmar Pago

**Endpoint:**
```
POST /confirmar-pago/<order_id>
```

**Parámetros JSON (YAPE):**
```json
{
    "payment_method": "yape",
    "yape_info": "+51 9 1234 5678"
}
```

**Parámetros JSON (Tarjeta):**
```json
{
    "payment_method": "tarjeta",
    "last_digits": "9010",
    "card_holder": "JUAN PEREZ"
}
```

**Ejemplo:**
```javascript
async function confirmarPago(orderId, metodoPago, detalles) {
    const response = await fetch(`/confirmar-pago/${orderId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            payment_method: metodoPago,
            ...detalles
        })
    });
    
    const data = await response.json();
    
    if (data.success) {
        // Redirigir a resumen
        window.location.href = data.redirect_url;
    }
}
```

**Respuesta:**
```json
{
    "success": true,
    "message": "Pago confirmado",
    "redirect_url": "/orden/1"
}
```

---

## 🔄 Flujo Completo de Compra

### Con autenticación
```
1. Usuario inicia sesión
2. Usuario navega a productos
3. Usuario hace clic en "Agregar al Carrito"
   → POST /carrito/agregar/<product_id>
4. Usuario ve el carrito
   → GET /carrito
5. Usuario puede actualizar cantidades
   → POST /carrito/actualizar/<item_id>
6. Usuario hace clic en "Proceder al Pago"
   → GET /checkout
7. Usuario selecciona método de pago
8. Usuario hace clic en "Confirmar Pago"
   → POST /procesar-pago (crea orden)
   → POST /confirmar-pago/<order_id> (confirma pago)
9. Sistema muestra resumen
   → GET /orden/<order_id>
10. Usuario puede ver todas sus órdenes
    → GET /mis-ordenes
```

---

## 💾 Estructura de Datos

### CarritoItem
```python
{
    "id": 1,
    "product_id": 5,
    "quantity": 2,
    "product": {
        "id": 5,
        "nombre": "Agua 500ml",
        "precio": 1.50,
        "imagen": "..."
    }
}
```

### Orden
```python
{
    "id": 1,
    "order_number": "ORD-1-1642000000",
    "user_id": 1,
    "total": 120.99,
    "status": "completado",
    "payment_method": "yape",
    "payment_status": "completado",
    "created_at": "2024-01-22 10:30:00",
    "items": [
        {
            "product_name": "Agua 500ml",
            "quantity": 2,
            "price": 1.50,
            "subtotal": 3.00
        }
    ]
}
```

---

## 🛠️ Personalización

### Cambiar Comisión de Tarjeta

En `checkout.html` busca:
```javascript
comision = cartTotal * 0.0299; // 2.99%
```

Y cámbialo al porcentaje deseado.

### Agregar Métodos de Pago

En `run.py`, en la función `procesar_pago()`:

```python
payment_method = data.get('payment_method')
if payment_method not in ['yape', 'tarjeta', 'tu_nuevo_metodo']:
    return jsonify({'error': 'Método de pago inválido'}), 400
```

### Cambiar Impuesto (IGV)

En `checkout.html`:
```javascript
const taxRate = 0.18; // Cambiar este valor
```

---

## 📊 Estadísticas Disponibles

### Para Administradores

```python
from models import Order, Payment
from datetime import datetime, timedelta

# Total de ventas hoy
today_orders = Order.query.filter(
    Order.created_at >= datetime.today().date()
).all()
total_today = sum(o.total for o in today_orders)

# Ordenes completadas
completed_orders = Order.query.filter_by(
    status='completado',
    payment_status='completado'
).all()

# Método de pago más usado
from sqlalchemy import func
most_used_payment = db.session.query(
    Order.payment_method,
    func.count(Order.id)
).group_by(Order.payment_method).all()
```

---

## 🚨 Errores Comunes

### Error 1: "Carrito vacío"
**Causa:** El usuario intenta acceder al checkout sin items
**Solución:** Validar que el carrito tenga items antes de mostrar checkout

### Error 2: "Stock insuficiente"
**Causa:** Se intenta comprar más de lo disponible
**Solución:** Limitar cantidad máxima en el input a `product.stock`

### Error 3: "No autorizado"
**Causa:** Usuario intenta acceder a carrito de otro usuario
**Solución:** Verificar siempre que `cart.user_id == current_user.id`

### Error 4: "Producto no encontrado"
**Causa:** El producto fue eliminado pero está en el carrito
**Solución:** Limpiar carrito al eliminar producto

---

## 🔒 Seguridad en API

### CSRF Protection
Todos los POST requieren token CSRF:
```html
<form method="POST">
    {{ csrf_token() }}
    ...
</form>
```

### Validación de Datos
```python
# Siempre validar en el servidor
if not isinstance(quantity, int) or quantity < 1:
    return error

if price < 0:
    return error
```

### Rate Limiting (Recomendado)
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: current_user.id,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/carrito/agregar/<int:product_id>', methods=['POST'])
@limiter.limit("10 per minute")
```

---

¡Listo para vender en línea! 🎉
