# Usamos una imagen base de Python ligera (slim)
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero los requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código (main.py)
COPY . .

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para iniciar el servidor de producción (Gunicorn)
# -w 2: Usa 2 "workers" (procesos) para manejar peticiones simultáneas
# -b 0.0.0.0:8000: Escucha en todas las interfaces en el puerto 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "main:app"]