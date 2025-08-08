FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=laboratorio.settings

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/media

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Crear migraciones y aplicarlas
RUN python manage.py makemigrations
RUN python manage.py migrate

# Crear superusuario (opcional, para demo)
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@laboratorio.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "laboratorio.wsgi:application"]