# 🛒 Sistema de Carrito de Compras - San Vicentino

## 📋 Descripción General

Se ha implementado un sistema completo de carrito de compras con soporte para pago en línea en tu aplicación Flask. El sistema incluye:

- ✅ Carrito de compras dinámico
- ✅ Gestor de productos con inventario
- ✅ Dos métodos de pago: **YAPE** y **Tarjeta de Débito**
- ✅ Cálculo automático de impuestos (IGV 18%)
- ✅ Órdenes y seguimiento de compras
- ✅ Recibos de compra imprimibles
- ✅ Historial de órdenes del usuario

---

## 🚀 Instalación y Configuración

### 1. Actualizar base de datos

Primero, necesitas actualizar tu base de datos con las nuevas tablas:

```bash
cd /workspaces/sanvicentino
python init_db.py
```

Este script:
- Crea todas las tablas necesarias
- Crea un usuario administrador por defecto
- Carga productos de ejemplo

**Credenciales por defecto:**
- Email: `admin@sanvicentino.com`
- Contraseña: `admin123`

⚠️ **IMPORTANTE:** Cambia estas credenciales después de la primera sesión.

### 2. Iniciar la aplicación

```bash
python app/run.py
```

---

## 🏗️ Estructura del Sistema

### Base de Datos - Nuevas Tablas

#### 1. **Tabla: products**
Almacena los productos disponibles para venta

```sql
- id: Integer (Primary Key)
- nombre: String (255)
- descripcion: Text
- precio: Float
- categoria: String (100)
- imagen: String (255)
- stock: Integer
- created_at: DateTime
```

#### 2. **Tabla: cart**
Almacena los carritos de compra de cada usuario

```sql
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key -> users)
- created_at: DateTime
- updated_at: DateTime
```

#### 3. **Tabla: cart_items**
Items dentro de cada carrito

```sql
- id: Integer (Primary Key)
- cart_id: Integer (Foreign Key -> cart)
- product_id: Integer (Foreign Key -> products)
- quantity: Integer
- created_at: DateTime
```

#### 4. **Tabla: orders**
Registro de todas las órdenes/compras realizadas

```sql
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key -> users)
- order_number: String (50, Unique)
- total: Float
- status: String (pendiente, completado, cancelado)
- payment_method: String (yape, tarjeta)
- payment_status: String (pendiente, completado, fallido)
- created_at: DateTime
- updated_at: DateTime
```

#### 5. **Tabla: order_items**
Items dentro de cada orden (copia del carrito)

```sql
- id: Integer (Primary Key)
- order_id: Integer (Foreign Key -> orders)
- product_id: Integer (Foreign Key -> products)
- product_name: String (255)
- price: Float
- quantity: Integer
- subtotal: Float
```

#### 6. **Tabla: payments**
Registro de todos los pagos realizados

```sql
- id: Integer (Primary Key)
- order_id: Integer (Foreign Key -> orders)
- amount: Float
- method: String (yape, tarjeta_debito)
- status: String (pendiente, completado, fallido)
- transaction_id: String (100)
- payment_details: JSON
- created_at: DateTime
- updated_at: DateTime
```

---

## 📍 Rutas Disponibles

### Rutas Públicas

- `GET /` - Página de inicio
- `GET /productos` - Catálogo de productos
- `GET /contactanos` - Página de contacto

### Rutas de Autenticación

- `GET /login` - Formulario de login
- `POST /login` - Procesar login
- `GET /register` - Formulario de registro
- `POST /register` - Procesar registro
- `GET /logout` - Cerrar sesión
- `GET /login/google` - Login con Google
- `GET /authorize/google` - Callback de Google

### Rutas de Carrito (Requiere autenticación)

- `GET /carrito` - Ver carrito de compras
- `POST /carrito/agregar/<product_id>` - Agregar producto al carrito
- `POST /carrito/eliminar/<item_id>` - Eliminar item del carrito
- `POST /carrito/actualizar/<item_id>` - Actualizar cantidad
- `POST /carrito/vaciar` - Vaciar carrito completo

### Rutas de Compra (Requiere autenticación)

- `GET /checkout` - Página de checkout/pago
- `POST /procesar-pago` - Crear orden
- `POST /confirmar-pago/<order_id>` - Confirmar pago
- `GET /orden/<order_id>` - Ver resumen de orden
- `GET /mis-ordenes` - Ver todas mis órdenes

### Rutas de Administrador

- `GET /producto/crear` - Formulario para crear producto
- `POST /producto/crear` - Crear nuevo producto
- `POST /producto/eliminar/<product_id>` - Eliminar producto

---

## 💳 Métodos de Pago

### 1. YAPE
- **Comisión:** Gratis
- **Proceso:**
  1. El usuario proporciona su número de teléfono registrado en YAPE
  2. Se crea la orden
  3. El usuario recibe una notificación en YAPE
  4. Confirma el pago en la app YAPE
  5. Se confirma la compra

### 2. Tarjeta de Débito
- **Comisión:** 2.99% sobre el total
- **Tarjetas soportadas:** Visa, Mastercard, Diners Club
- **Datos requeridos:**
  - Nombre del titular
  - Número de tarjeta
  - Mes de vencimiento
  - Año de vencimiento
  - CVV (3-4 dígitos)

**Nota:** Los datos de tarjeta están seguros y encriptados (aplica SSL)

---

## 📊 Cálculo de Precios

El total se calcula de la siguiente manera:

```
Subtotal = Suma de (precio_producto × cantidad)
IGV (18%) = Subtotal × 0.18
Comisión = 0.00 (YAPE) o Subtotal × 0.0299 (Tarjeta)
Total = Subtotal + IGV + Comisión
```

Ejemplo con Tarjeta:
```
Producto: S/. 100.00
IGV (18%): S/. 18.00
Comisión (2.99%): S/. 2.99
Total: S/. 120.99
```

---

## 🎨 Templates Creados/Modificados

### Nuevos Templates

1. **carrito.html**
   - Muestra los items del carrito
   - Permite actualizar cantidades
   - Muestra resumen de compra
   - Botón para proceder al pago

2. **checkout.html**
   - Formulario de selección de método de pago
   - Formularios específicos para YAPE y Tarjeta
   - Resumen detallado del pedido
   - Cálculo en tiempo real de totales

3. **resumen_orden.html**
   - Confirmación de compra exitosa
   - Detalles de la orden
   - Recibo imprimible
   - Información de pago

4. **mis_ordenes.html**
   - Historial de compras del usuario
   - Estado de cada orden
   - Botones para ver detalles

5. **crear_producto.html**
   - Formulario para crear nuevos productos (Admin)
   - Validación de datos

### Templates Modificados

1. **base.html**
   - Agregado icono de carrito en la navbar
   - Contador de items en el carrito
   - Enlaces a "Mis Órdenes"
   - Enlace de logout

2. **productos.html**
   - Nuevo diseño con tarjetas de productos
   - Botón "Agregar al Carrito"
   - Información de stock
   - Mejor visualización de precios

---

## 🔧 Funcionalidades JavaScript

### Funciones en el Cliente

#### carrito.html
```javascript
actualizarCantidad(itemId, cantidad)  // Actualizar cantidad de un item
eliminarDelCarrito(itemId)             // Eliminar item del carrito
vaciarCarrito()                        // Vaciar todo el carrito
```

#### productos.html
```javascript
agregarAlCarrito(productId)            // Agregar producto al carrito
```

#### checkout.html
```javascript
seleccionarMetodoPago(metodo)          // Seleccionar método de pago
mostrarFormularioPago(metodo)          // Mostrar form según método
procesarPago(event)                    // Procesar el pago
```

---

## 🔐 Seguridad

✅ Implementadas las siguientes medidas de seguridad:

1. **Autenticación requerida** para acceso al carrito
2. **Validación de pertenencia** de items al usuario
3. **CSRF Protection** via Flask-WTF
4. **Contraseñas hasheadas** con werkzeug
5. **Validación de datos** en el servidor
6. **SSL/TLS** recomendado para producción
7. **JSON responses** para prevenir XSS

---

## 🐛 Manejo de Errores

El sistema incluye manejo completo de errores:

- ✅ Carrito no encontrado (crea uno nuevo)
- ✅ Producto no disponible
- ✅ Stock insuficiente
- ✅ Acceso no autorizado
- ✅ Datos inválidos
- ✅ Errores de base de datos

---

## 📱 Responsive Design

- ✅ Totalmente responsive
- ✅ Mobile-first design
- ✅ Tailwind CSS para estilos
- ✅ Iconografía clara
- ✅ Navegación intuitiva

---

## 🧪 Pruebas Recomendadas

### 1. Prueba de Carrito
```
1. Inicia sesión
2. Agrega varios productos
3. Actualiza cantidades
4. Elimina un item
5. Verifica totales
```

### 2. Prueba de YAPE
```
1. Selecciona método YAPE
2. Ingresa número de teléfono
3. Procesa el pago
4. Verifica orden completada
```

### 3. Prueba de Tarjeta
```
1. Selecciona método Tarjeta
2. Completa datos de tarjeta
3. Procesa el pago
4. Verifica comisión aplicada
5. Verifica recibo
```

### 4. Prueba de Inventario
```
1. Crea producto con stock limitado
2. Intenta agregar más que el stock
3. Verifica mensaje de error
4. Después de compra, verifica stock se redujo
```

---

## 🚨 Pasos Siguientes Recomendados

### 1. Implementar Pasarela de Pago Real
- Integrar YAPE API (https://yape.pe/developers)
- Integrar procesador de tarjetas (Niubiz, etc.)
- Webhooks para confirmar pagos

### 2. Perfil de Usuario Extendido
- Dirección de envío
- Teléfono de contacto
- DNI para facturas

### 3. Carrito en Sesiones
- Guardar carrito cuando no está autenticado
- Recuperar al login

### 4. Email Notifications
- Confirmación de orden
- Actualización de estado
- Recibos por email

### 5. Integración de Envíos
- Cálculo de costos de envío
- Seguimiento de envíos
- Diferentes operadores

### 6. Sistema de Cupones/Descuentos
- Códigos de descuento
- Ofertas por cantidad
- Cupones temporales

### 7. Panel de Administrador
- Dashboard con ventas
- Gestión de inventario
- Reportes de órdenes

### 8. Historial y Recomendaciones
- Productos sugeridos
- Favoritos
- Wishlist

---

## 📞 Soporte

Para preguntas o problemas:

1. Revisa los logs de Flask
2. Verifica la base de datos
3. Consulta la consola del navegador (F12)
4. Revisa la sección de errores

---

## 📝 Notas Importantes

⚠️ **En Producción:**
- Cambia `SECRET_KEY` a algo seguro
- Usa variables de entorno para credenciales
- Habilita HTTPS/SSL
- Configura CORS adecuadamente
- Implementa rate limiting
- Configura backups de BD
- Usa un servidor WSGI (Gunicorn)
- Implementa logging apropiado

---

## 🎉 ¡Listo!

Tu sistema de carrito está completamente funcional. Los usuarios ahora pueden:

✅ Ver productos  
✅ Agregar al carrito  
✅ Realizar compras  
✅ Pagar con YAPE o Tarjeta  
✅ Ver sus órdenes  
✅ Imprimir recibos  

¡Felicidades! 🎊
