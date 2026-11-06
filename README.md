# 🍰 Tienda de Tortas - Proyecto Fullstack

Proyecto final para el Diplomado Fullstack. Una tienda web de tortas y pasteles con 5 productos, registro de usuarios, y despliegue en AWS.

## 🚀 Tecnologías Utilizadas

- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Mail.
- **Frontend:** HTML5, CSS3 (Diseño responsivo con colores rosado y morado).
- **Base de Datos:** SQLAlchemy (SQLite local, migrado a RDS en AWS).
- **Contenedores:** Docker con imagen base de Ubuntu 22.04 desde DockerHub.
- **Infraestructura (AWS):**
    - **VPC:** Personalizada, con subredes públicas y tabla de rutas.
    - **EC2:** Instancia con Amazon Linux 2023, corriendo la aplicación en Docker.
    - **S3:** Bucket para almacenar las imágenes de las tortas.
- **Monitoreo:** Sentry (Configurado para tracking de logs).
- **Control de Versiones:** Git y GitHub.

## 🛠️ Características Principales

- Registro e inicio de sesión de usuarios.
- Catálogo de 5 productos (tortas) con imágenes, descripción y precio.
- Proceso de compra simulado.
- Envío de correo de confirmación al usuario al comprar.
- Productos VIP visibles solo para usuarios registrados.

## 📂 Estructura del Proyecto

```bash
tienda_tortas/
├── app.py                 # Aplicación principal Flask
├── models.py              # Definición de las 10 tablas de la base de datos
├── requirements.txt       # Dependencias de Python
├── Dockerfile             # Configuración para construir la imagen Docker
├── .gitignore             # Archivos y carpetas ignorados por Git
├── templates/             # Plantillas HTML
│   ├── home.html
│   ├── registro.html
│   ├── login.html
│   └── tienda.html
└── README.md    
