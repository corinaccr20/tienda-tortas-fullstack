from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Usuario, Perfil, Producto, Categoria, Carrito, ItemCarrito, Orden, NotificacionEmail
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os # <--- IMPORTANTE: Añadimos la librería os

# Sentry comentado por ahora
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(__name__)
app.secret_key = 'clave-super-secreta-para-sessions'

# --- CONFIGURACIÓN PARA RENDER Y LOCAL ---
# 1. Busca si existe la variable DATABASE_URL (Render). 
# 2. Si no existe (tu compu), usa sqlite:///tienda.db
database_url = os.environ.get('DATABASE_URL', 'sqlite:///tienda.db')

# Render a veces da la URL con "postgres://", pero SQLAlchemy necesita "postgresql://"
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurar correo (Si no tienes correo real, déjalo así, el código ya maneja el error)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'  # <--- CAMBIA ESTO
app.config['MAIL_PASSWORD'] = 'tu_contraseña_de_app'  # <--- CAMBIA ESTO

mail = Mail(app)
db.init_app(app)
# ----------------------------------------

# El resto de tu código (crear tablas, rutas, etc.) queda igual...
with app.app_context():
    db.create_all()
    # ... (todo lo demás sigue igual)