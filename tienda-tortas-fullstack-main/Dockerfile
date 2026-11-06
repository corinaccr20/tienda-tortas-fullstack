# Usamos Ubuntu desde DockerHub (como pide el proyecto)
FROM ubuntu:22.04

# Instalar Python y herramientas
RUN apt-get update && apt-get install -y python3 python3-pip

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip3 install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Puerto donde corre Flask
EXPOSE 5000

# Comando para correr la app
CMD ["python3", "app.py"]