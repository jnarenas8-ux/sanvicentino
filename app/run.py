from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import (
    LoginManager, login_user,
    login_required, logout_user, current_user
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
from pathlib import Path
import secrets
import time
import uuid
from datetime import datetime
from sqlalchemy.exc import OperationalError
from PIL import Image
from models import (
    db, User, Product, Cart, CartItem, Order, OrderItem, Payment
)

# ========================
# CARGAR VARIABLES DE ENTORNO
# ========================
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
OAUTH_ENABLED = (
    GOOGLE_CLIENT_ID and 
    GOOGLE_CLIENT_SECRET and 
    not GOOGLE_CLIENT_ID.startswith("placeholder") and 
    not GOOGLE_CLIENT_SECRET.startswith("placeholder")
)

# ========================
# APP CONFIG
# ========================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-key-sanvicentino-2024")
# Usar SQLite para desarrollo
import os
from pathlib import Path

db_path = Path(__file__).parent.parent / "instance" / "sanvicentino.db"
db_url = f"sqlite:///{db_path}"

# Usar DATABASE_URL si está disponible, sino usar la ruta construida
if os.getenv("DATABASE_URL"):
    db_url = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ========================
# CONFIGURACIÓN DE CARGA DE ARCHIVOS
# ========================
UPLOAD_FOLDER = Path(__file__).parent / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Hacer current_user disponible en todos los templates
@app.context_processor
def inject_user():
    return dict(current_user=current_user, oauth_enabled=OAUTH_ENABLED)

oauth = OAuth(app)

# ========================
# GOOGLE OAUTH (solo si está configurado)
# ========================
google = None
if OAUTH_ENABLED:
    google = oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v2/',
        client_kwargs={'scope': 'email profile'},
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========================
# FUNCIONES AUXILIARES
# ========================
def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload_image(file):
    """
    Guarda una imagen subida, la optimiza y retorna el nombre de archivo
    Args:
        file: Objeto de archivo de Flask
    Returns:
        str: Nombre del archivo guardado o None si hay error
    """
    try:
        if not file or file.filename == '':
            return None
        
        if not allowed_file(file.filename):
            flash('Tipo de archivo no permitido. Use: PNG, JPG, JPEG, GIF, WebP', 'danger')
            return None
        
        if file.content_length > MAX_FILE_SIZE:
            flash('El archivo es demasiado grande. Máximo: 5MB', 'danger')
            return None
        
        # Generar nombre único para el archivo
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Abrir y optimizar imagen
        img = Image.open(file.stream)
        
        # Convertir RGBA a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Redimensionar si es muy grande (máximo 1920x1080)
        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        
        # Guardar imagen optimizada
        img.save(filepath, 'JPEG', quality=85, optimize=True)
        
        return unique_filename
    except Exception as e:
        flash(f'Error al procesar la imagen: {str(e)}', 'danger')
        return None

# ========================
# FORMULARIOS
# ========================
class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

# ========================
# RUTAS
# ========================
@app.route('/api/check-auth')
def check_auth():
    """API para verificar si el usuario está autenticado"""
    return jsonify({
        'authenticated': current_user.is_authenticated,
        'user_id': current_user.id if current_user.is_authenticated else None
    })

@app.route('/')
def index():
    # Si el usuario está autenticado, obtén su carrito
    cart_count = 0
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_count = cart.get_item_count()
    
    # Si es admin, mostrar todos los productos; si no, solo los publicados
    if current_user.is_authenticated and current_user.is_admin:
        products = Product.query.all()
    else:
        products = Product.query.filter_by(publicado=True).all()
    
    return render_template('index.html', cart_count=cart_count, products=products)


@app.route('/productos')
def productos():
    cart_count = 0
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_count = cart.get_item_count()
    
    # Si es admin, mostrar todos los productos; si no, solo los publicados
    if current_user.is_authenticated and current_user.is_admin:
        products = Product.query.all()
    else:
        products = Product.query.filter_by(publicado=True).all()
    
    return render_template('productos.html', productos=products, cart_count=cart_count)


# ========================
# RUTAS DE CARRITO
# ========================
@app.route('/carrito')
@login_required
def ver_carrito():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    cart_count = cart.get_item_count()
    return render_template('carrito.html', cart=cart, cart_count=cart_count)


@app.route('/carrito/agregar/<int:product_id>', methods=['POST'])
@login_required
def agregar_al_carrito(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    if product.stock <= 0:
        return jsonify({'error': 'Producto agotado'}), 400
    
    # Obtener o crear el carrito
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    # Verificar si el producto ya está en el carrito
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        # Si ya existe, aumentar cantidad
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
        else:
            return jsonify({'error': 'Stock insuficiente'}), 400
    else:
        # Si no existe, crear nuevo item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Producto agregado al carrito',
        'cart_count': cart.get_item_count(),
        'cart_total': cart.get_total()
    }), 200


@app.route('/carrito/eliminar/<int:item_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(item_id):
    cart_item = CartItem.query.get(item_id)
    
    if not cart_item:
        return jsonify({'error': 'Item no encontrado'}), 404
    
    # Verificar que pertenece al usuario
    if cart_item.cart.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    cart = cart_item.cart
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Producto eliminado del carrito',
        'cart_count': cart.get_item_count(),
        'cart_total': cart.get_total()
    }), 200


@app.route('/carrito/actualizar/<int:item_id>', methods=['POST'])
@login_required
def actualizar_carrito(item_id):
    data = request.get_json()
    quantity = data.get('quantity', 1)
    
    cart_item = CartItem.query.get(item_id)
    
    if not cart_item:
        return jsonify({'error': 'Item no encontrado'}), 404
    
    # Verificar que pertenece al usuario
    if cart_item.cart.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    # Validar cantidad
    if quantity <= 0:
        return jsonify({'error': 'Cantidad inválida'}), 400
    
    if quantity > cart_item.product.stock:
        return jsonify({'error': 'Stock insuficiente'}), 400
    
    cart_item.quantity = quantity
    db.session.commit()
    
    cart = cart_item.cart
    return jsonify({
        'success': True,
        'message': 'Carrito actualizado',
        'cart_count': cart.get_item_count(),
        'cart_total': cart.get_total(),
        'subtotal': cart_item.get_subtotal()
    }), 200


@app.route('/carrito/vaciar', methods=['POST'])
@login_required
def vaciar_carrito():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if cart:
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
    
    return jsonify({'success': True, 'message': 'Carrito vaciado'}), 200


# ========================
# RUTAS DE CHECKOUT Y PAGO
# ========================
@app.route('/checkout')
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if not cart or not cart.items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('ver_carrito'))
    
    cart_count = cart.get_item_count()
    return render_template('checkout.html', cart=cart, cart_count=cart_count)


@app.route('/procesar-pago', methods=['POST'])
@login_required
def procesar_pago():
    data = request.get_json()
    
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if not cart or not cart.items:
        return jsonify({'error': 'Carrito vacío'}), 400
    
    payment_method = data.get('payment_method')
    if payment_method not in ['yape', 'tarjeta']:
        return jsonify({'error': 'Método de pago inválido'}), 400
    
    try:
        # Crear la orden
        order_number = f"ORD-{current_user.id}-{int(time.time())}"
        total = cart.get_total()
        
        order = Order(
            user_id=current_user.id,
            order_number=order_number,
            total=total,
            payment_method=payment_method,
            status="pendiente"
        )
        
        # Crear items de la orden
        for cart_item in cart.items:
            order_item = OrderItem(
                product_id=cart_item.product_id,
                product_name=cart_item.product.nombre,
                price=cart_item.product.precio,
                quantity=cart_item.quantity,
                subtotal=cart_item.get_subtotal()
            )
            order.items.append(order_item)
            
            # Reducir stock del producto
            cart_item.product.stock -= cart_item.quantity
        
        db.session.add(order)
        db.session.commit()
        
        # Crear registro de pago
        payment = Payment(
            order_id=order.id,
            amount=total,
            method=payment_method,
            transaction_id=str(uuid.uuid4())
        )
        
        db.session.add(payment)
        
        # Vaciar carrito
        CartItem.query.filter_by(cart_id=cart.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_id': order.id,
            'order_number': order_number,
            'message': 'Orden creada exitosamente. Proceda a confirmar el pago.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al procesar la orden: {str(e)}'}), 500


@app.route('/confirmar-pago/<int:order_id>', methods=['POST'])
@login_required
def confirmar_pago(order_id):
    """Confirma el pago y completa la orden"""
    order = Order.query.get(order_id)
    
    if not order or order.user_id != current_user.id:
        return jsonify({'error': 'Orden no encontrada'}), 404
    
    data = request.get_json()
    
    try:
        payment_details = {
            'payment_method': data.get('payment_method'),
            'confirmed_at': datetime.utcnow().isoformat()
        }
        
        if data.get('payment_method') == 'yape':
            payment_details['yape_info'] = data.get('yape_info', '')
        elif data.get('payment_method') == 'tarjeta':
            payment_details['last_digits'] = data.get('last_digits', '')
            payment_details['card_holder'] = data.get('card_holder', '')
        
        # Actualizar estado de pago
        order.payment.status = 'completado'
        order.payment.payment_details = payment_details
        order.status = 'completado'
        order.payment_status = 'completado'
        
        db.session.commit()
        
        flash('¡Pago completado exitosamente!', 'success')
        
        return jsonify({
            'success': True,
            'message': 'Pago confirmado',
            'redirect_url': url_for('resumen_orden', order_id=order.id)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al confirmar pago: {str(e)}'}), 500


@app.route('/orden/<int:order_id>')
@login_required
def resumen_orden(order_id):
    order = Order.query.get(order_id)
    
    if not order or order.user_id != current_user.id:
        flash('Orden no encontrada', 'danger')
        return redirect(url_for('index'))
    
    cart_count = 0
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart_count = cart.get_item_count()
    
    return render_template('resumen_orden.html', order=order, cart_count=cart_count)


@app.route('/mis-ordenes')
@login_required
def mis_ordenes():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    cart_count = 0
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart_count = cart.get_item_count()
    
    return render_template('mis_ordenes.html', orders=orders, cart_count=cart_count)


@app.route('/login/google')
def google_login():
    if not OAUTH_ENABLED or google is None:
        flash('Google OAuth no está configurado. Por favor usa login con usuario y contraseña.', 'warning')
        return redirect(url_for('login'))
    
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize/google')
def google_authorize():
    if not OAUTH_ENABLED or google is None:
        flash('Google OAuth no está configurado.', 'danger')
        return redirect(url_for('login'))
    
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()

    email = user_info['email']
    name = user_info.get('name', email.split('@')[0])

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            username=name,
            email=email,
            password=generate_password_hash(secrets.token_hex(16)),
            provider="google"
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first():
            flash('El usuario o correo ya existen.', 'danger')
            return render_template('register.html', form=form)

        # Obtener el rol seleccionado (cliente o admin)
        role = request.form.get('role', 'client')
        is_admin = role == 'admin'

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            provider="local",
            is_admin=is_admin
        )

        db.session.add(user)
        db.session.commit()

        role_name = "Administrador" if is_admin else "Cliente"
        flash(f'Cuenta de {role_name} creada correctamente. ¡Bienvenido!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.provider == "local" and check_password_hash(user.password, form.password.data):
            login_user(user)
            
            # Mensaje personalizado según el rol
            if user.is_admin:
                flash(f'¡Bienvenido Administrador {user.username}! 🔑 Ahora puedes gestionar productos.', 'success')
            else:
                flash(f'¡Bienvenido {user.username}! 👤 Disfruta comprando nuestros productos.', 'success')
            
            return redirect(url_for('index'))
        flash('Credenciales inválidas.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')


# ========================
# RUTAS DE PRODUCTOS
# ========================
@app.route('/producto/eliminar/<int:product_id>', methods=['POST'])
@login_required
def eliminar_producto(product_id):
    """Elimina un producto (solo administrador)"""
    if not current_user.is_admin:
        flash('No tienes permiso para realizar esta acción', 'danger')
        return redirect(url_for('productos'))
    
    product = Product.query.get(product_id)
    if not product:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos'))
    
    try:
        # Primero eliminar todos los CartItems que hacen referencia a este producto
        CartItem.query.filter_by(product_id=product_id).delete()
        
        # Luego eliminar todos los OrderItems que hacen referencia a este producto
        OrderItem.query.filter_by(product_id=product_id).delete()
        
        # Finalmente eliminar el producto
        db.session.delete(product)
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el producto: {str(e)}', 'danger')
    
    return redirect(url_for('productos'))


@app.route('/producto/toggle-publicado/<int:product_id>', methods=['POST'])
@login_required
def toggle_publicado(product_id):
    """Publica o despublica un producto (solo administrador)"""
    if not current_user.is_admin:
        flash('No tienes permiso para realizar esta acción', 'danger')
        return redirect(url_for('productos'))
    
    product = Product.query.get(product_id)
    if not product:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos'))
    
    try:
        product.publicado = not product.publicado
        db.session.commit()
        
        estado = "publicado" if product.publicado else "despublicado"
        flash(f'Producto {estado} exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar el producto: {str(e)}', 'danger')
    
    return redirect(url_for('productos'))


@app.route('/producto/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    """Crea un nuevo producto (solo administrador)"""
    if not current_user.is_admin:
        flash('No tienes permiso para realizar esta acción', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            precio = float(request.form.get('precio', 0))
            categoria = request.form.get('categoria')
            stock = int(request.form.get('stock', 0))
            
            # Procesar imagen
            imagen_url = None
            
            # Prioridad 1: Archivo subido
            if 'imagen_archivo' in request.files:
                file = request.files['imagen_archivo']
                if file and file.filename != '':
                    filename = save_upload_image(file)
                    if filename:
                        imagen_url = f"/static/uploads/{filename}"
            
            # Prioridad 2: URL si no hay archivo
            if not imagen_url:
                imagen_url = request.form.get('imagen')
            
            # Crear producto
            product = Product(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                categoria=categoria,
                imagen=imagen_url,
                stock=stock,
                publicado=False  # Los nuevos productos se crean sin publicar
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash('Producto creado exitosamente (aún no está publicado)', 'success')
            return redirect(url_for('productos'))
        except ValueError as e:
            db.session.rollback()
            flash(f'Error: Datos inválidos - {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el producto: {str(e)}', 'danger')
    
    cart_count = 0
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_count = cart.get_item_count()
    
    return render_template('crear_producto.html', cart_count=cart_count)

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

