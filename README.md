# Sistema de Recordatorios de Documentos - Laboratorio

Sistema web desarrollado en Django para la gestión y seguimiento de recordatorios de revisión de documentos en un laboratorio de pruebas mecánicas.

## Características

- **Gestión de Documentos**: Creación, edición y seguimiento de documentos técnicos
- **Recordatorios de Revisión**: Sistema automatizado para programar y realizar seguimiento de revisiones
- **Dashboard Interactivo**: Panel principal con estadísticas y alertas importantes
- **Sistema de Usuarios**: Autenticación y control de acceso
- **Interfaz Moderna**: Diseño responsive con Bootstrap 5
- **Alertas Automáticas**: Notificaciones para recordatorios próximos a vencer

## Tecnologías Utilizadas

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Base de Datos**: SQLite (configurable a PostgreSQL)
- **Despliegue**: Docker + Nginx + Gunicorn

## Instalación con Docker

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd laboratorio-recordatorios
```

2. **Construir y ejecutar con Docker Compose**:
```bash
docker-compose up --build -d
```

3. **Acceder a la aplicación**:
- URL: http://localhost
- Usuario admin: `admin`
- Contraseña: `admin123`

## Instalación Manual

1. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Crear superusuario**:
```bash
python manage.py createsuperuser
```

5. **Ejecutar servidor de desarrollo**:
```bash
python manage.py runserver
```

## Uso del Sistema

### 1. Gestión de Documentos
- Crear y editar documentos técnicos
- Clasificar por tipos y estados
- Versionado de documentos
- Búsqueda y filtrado avanzado

### 2. Recordatorios de Revisión
- Programar revisiones periódicas
- Establecer prioridades y fechas
- Registrar hallazgos y acciones correctivas
- Seguimiento del estado de las revisiones

### 3. Dashboard y Reportes
- Estadísticas generales del sistema
- Alertas de recordatorios vencidos
- Recordatorios próximos a vencer
- Distribución de documentos por tipo

## Estructura del Proyecto

```
laboratorio/
├── laboratorio/          # Configuración principal de Django
├── recordatorios/        # Aplicación principal
├── templates/           # Plantillas HTML
├── static/             # Archivos estáticos (CSS, JS, imágenes)
├── Dockerfile          # Configuración Docker
├── docker-compose.yml  # Orquestación de servicios
├── nginx.conf         # Configuración Nginx
└── requirements.txt   # Dependencias Python
```

## Características del Sistema

### Modelos Principales

1. **TipoDocumento**: Clasificación de documentos
2. **Documento**: Documentos del laboratorio
3. **RecordatorioRevision**: Seguimiento de revisiones

### Funcionalidades Destacadas

- **Cálculo automático** de fechas de próxima revisión
- **Sistema de alertas** visual para recordatorios vencidos
- **Interfaz responsive** para dispositivos móviles
- **Filtros avanzados** en todas las listas
- **Exportación de datos** (funcionalidad preparada)
- **Sistema de permisos** integrado con Django

### Seguridad

- Autenticación requerida para todas las funciones
- Control de acceso basado en usuarios
- Validación de formularios
- Protección CSRF
- Configuración de seguridad para producción

## Configuración para Producción

### Variables de Entorno

```bash
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgres://usuario:password@localhost/laboratorio
```

### Base de Datos PostgreSQL

Para usar PostgreSQL en producción, actualiza `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'laboratorio',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Despliegue en Producción

1. **Con Docker (Recomendado)**:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

2. **En servidor tradicional**:
```bash
# Recopilar archivos estáticos
python manage.py collectstatic

# Usar Gunicorn
gunicorn --bind 0.0.0.0:8000 laboratorio.wsgi:application
```

## Mantenimiento

### Respaldos
```bash
# Respaldar base de datos
python manage.py dumpdata > backup.json

# Restaurar
python manage.py loaddata backup.json
```

### Logs
Los logs del sistema se encuentran en:
- Docker: `docker-compose logs -f`
- Manual: Configurar en `settings.py`

## Soporte

Para soporte técnico o reportar problemas:
- Revisar logs del sistema
- Verificar configuración de base de datos
- Comprobar permisos de archivos estáticos

## Licencia

Este proyecto está diseñado para uso interno del laboratorio de pruebas mecánicas.

---

**Desarrollado para mejorar el sistema de calidad del laboratorio de pruebas mecánicas** 🔬⚙️