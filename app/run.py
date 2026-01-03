from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
from pathlib import Path
import secrets
import time
from sqlalchemy.exc import OperationalError
# ========================
# CARGAR VARIABLES DE ENTORNO
# ========================
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

assert os.getenv("GOOGLE_CLIENT_ID"), "GOOGLE_CLIENT_ID NO CARGADO"
assert os.getenv("GOOGLE_CLIENT_SECRET"), "GOOGLE_CLIENT_SECRET NO CARGADO"

# ========================
# APP CONFIG
# ========================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://usuario_app:password_app@mysql:3306/sanvicentino"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
oauth = OAuth(app)

# ========================
# GOOGLE OAUTH
# ========================
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'email profile'},
)

# ========================
# MODELO
# ========================
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    provider = db.Column(db.String(50), default="local")  # local | google


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize/google')
def google_authorize():
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

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            provider="local"
        )

        db.session.add(user)
        db.session.commit()

        flash('Cuenta creada correctamente.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.provider == "local" and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Credenciales inválidas.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

