from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documento'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Documento(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('revision', 'En Revisión'),
        ('aprobado', 'Aprobado'),
        ('obsoleto', 'Obsoleto'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    codigo_documento = models.CharField(max_length=50, unique=True, verbose_name='Código del Documento')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, verbose_name='Tipo de Documento')
    version = models.CharField(max_length=10, default='1.0', verbose_name='Versión')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador', verbose_name='Estado')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Creado por')
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_modificacion']
    
    def __str__(self):
        return f'{self.codigo_documento} - {self.titulo}'
    
    def get_absolute_url(self):
        return reverse('documento_detalle', kwargs={'pk': self.pk})

class RecordatorioRevision(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, verbose_name='Documento')
    fecha_revision = models.DateTimeField(verbose_name='Fecha de Revisión')
    fecha_proxima_revision = models.DateTimeField(blank=True, null=True, verbose_name='Próxima Revisión')
    revisor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Revisor')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name='Estado')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='media', verbose_name='Prioridad')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    hallazgos = models.TextField(blank=True, verbose_name='Hallazgos')
    acciones_correctivas = models.TextField(blank=True, verbose_name='Acciones Correctivas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_completado = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Completado')
    
    class Meta:
        verbose_name = 'Recordatorio de Revisión'
        verbose_name_plural = 'Recordatorios de Revisión'
        ordering = ['-fecha_revision']
    
    def __str__(self):
        return f'Revisión: {self.documento.titulo} - {self.fecha_revision.strftime("%d/%m/%Y")}'
    
    def save(self, *args, **kwargs):
        if self.estado == 'completado' and not self.fecha_completado:
            self.fecha_completado = timezone.now()
        
        # Si no hay fecha de próxima revisión, calcular automáticamente (30 días por defecto)
        if not self.fecha_proxima_revision and self.fecha_revision:
            self.fecha_proxima_revision = self.fecha_revision + timedelta(days=30)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recordatorio_detalle', kwargs={'pk': self.pk})
    
    @property
    def dias_hasta_revision(self):
        if self.fecha_proxima_revision:
            delta = self.fecha_proxima_revision.date() - timezone.now().date()
            return delta.days
        return None
    
    @property
    def es_vencido(self):
        if self.fecha_proxima_revision:
            return timezone.now().date() > self.fecha_proxima_revision.date()
        return False
    
    @property
    def es_proximo_a_vencer(self):
        dias = self.dias_hasta_revision
        return dias is not None and 0 <= dias <= 7