# Usar imagen oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos primero (para cache de Docker)
COPY requirements.txt .

# Instalar dependencias del sistema si son necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Exponer el puerto (ajustar según tu app, normalmente 5000 para Flask, 8000 para Django)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]
