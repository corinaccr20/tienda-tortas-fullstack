from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Usuario, Perfil, Producto, Categoria, Carrito, ItemCarrito, Orden, NotificacionEmail
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'clave-super-secreta-para-sessions'

# --- CONFIGURACIÓN PARA RENDER Y LOCAL ---
database_url = os.environ.get('DATABASE_URL', 'sqlite:///tienda.db')

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        # Verificar si el usuario ya existe
        user_exists = Usuario.query.filter_by(email=email).first()
        if user_exists:
            flash('El correo ya está registrado. Intenta iniciar sesión.')
            return redirect(url_for('registro'))
        
        # Crear nuevo usuario con contraseña encriptada
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Usuario.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.nombre
            flash(f'¡Bienvenido de nuevo, {user.nombre}!')
            return redirect(url_for('tienda'))
        else:
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.')
    return redirect(url_for('home'))

@app.route('/tienda')
def tienda():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver la tienda VIP.')
        return redirect(url_for('login'))
        
    productos = Producto.query.all()
    return render_template('tienda.html', productos=productos)

@app.route('/comprar/<int:producto_id>')
def comprar(producto_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para comprar.')
        return redirect(url_for('login'))
        
    producto = Producto.query.get_or_404(producto_id)
    
    # Lógica simple de compra (simulada, sin correo)
    # Aquí podrías crear una Orden en la base de datos si quisieras
    flash(f'¡Has comprado {producto.nombre} por ${producto.precio}! (Compra simulada)')
    
    return redirect(url_for('tienda'))

# --- INICIALIZACIÓN DE LA BASE DE DATOS Y DATOS SEMILLA ---
with app.app_context():
    db.create_all()
    
    # Si no hay productos, insertamos los 5 productos automáticamente
    if not Producto.query.first():
        categoria = Categoria(nombre='Tortas Especiales', descripcion='Nuestras mejores tortas')
        db.session.add(categoria)
        db.session.commit()
        
        productos_semilla = [
            Producto(nombre='Torta de Chocolate', descripcion='Deliciosa torta de chocolate con ganache y fresas.', precio=25.00, categoria_id=categoria.id),
            Producto(nombre='Torta de Vainilla', descripcion='Suave bizcocho de vainilla con crema pastelera.', precio=22.00, categoria_id=categoria.id),
            Producto(nombre='Torta Red Velvet', descripcion='Clásica torta roja con frosting de queso crema.', precio=28.00, categoria_id=categoria.id),
            Producto(nombre='Torta de Frutas', descripcion='Bizcocho esponjoso con frutas de temporada y crema.', precio=24.00, categoria_id=categoria.id),
            Producto(nombre='Torta de Limón', descripcion='Torta cítrica con glaseado de limón y merengue.', precio=20.00, categoria_id=categoria.id)
        ]
        db.session.add_all(productos_semilla)
        db.session.commit()
        print("Productos de prueba insertados exitosamente.")

if __name__ == '__main__':
    app.run(debug=True)