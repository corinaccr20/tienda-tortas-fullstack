from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabla 1: Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    perfil = db.relationship('Perfil', backref='usuario', uselist=False)
    ordenes = db.relationship('Orden', backref='usuario')

# Tabla 2: Perfil (extiende información del usuario)
class Perfil(db.Model):
    __tablename__ = 'perfiles'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)

# Tabla 3: Categoria
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200))
    productos = db.relationship('Producto', backref='categoria')

# Tabla 4: Producto (aquí van tus 5 tortas)
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)  # más de 30 chars
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=10)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    imagenes = db.relationship('ImagenProducto', backref='producto')

# Tabla 5: ImagenProducto
class ImagenProducto(db.Model):
    __tablename__ = 'imagenes_producto'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    url_s3 = db.Column(db.String(300), nullable=False)  # dónde está en AWS S3
    es_principal = db.Column(db.Boolean, default=False)

# Tabla 6: Carrito (carrito de compras activo)
class Carrito(db.Model):
    __tablename__ = 'carritos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    items = db.relationship('ItemCarrito', backref='carrito')

# Tabla 7: ItemCarrito (productos dentro del carrito)
class ItemCarrito(db.Model):
    __tablename__ = 'items_carrito'
    id = db.Column(db.Integer, primary_key=True)
    carrito_id = db.Column(db.Integer, db.ForeignKey('carritos.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float)

# Tabla 8: Orden (cuando se confirma la compra)
class Orden(db.Model):
    __tablename__ = 'ordenes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, pagado, enviado
    metodo_pago = db.Column(db.String(50))
    pago = db.relationship('Pago', backref='orden', uselist=False)

# Tabla 9: Pago
class Pago(db.Model):
    __tablename__ = 'pagos'
    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes.id'))
    monto = db.Column(db.Float)
    fecha_pago = db.Column(db.DateTime)
    transaccion_id = db.Column(db.String(100))

# Tabla 10: NotificacionEmail (registro de correos enviados)
class NotificacionEmail(db.Model):
    __tablename__ = 'notificaciones_email'
    id = db.Column(db.Integer, primary_key=True)
    destinatario = db.Column(db.String(100))
    asunto = db.Column(db.String(200))
    contenido = db.Column(db.Text)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    exito = db.Column(db.Boolean, default=False)