from django.contrib import admin
from .models import TipoDocumento, Documento, RecordatorioRevision

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'fecha_creacion', 'version', 'estado']
    list_filter = ['tipo', 'estado', 'fecha_creacion']
    search_fields = ['titulo', 'codigo_documento', 'descripcion']
    date_hierarchy = 'fecha_creacion'

@admin.register(RecordatorioRevision)
class RecordatorioRevisionAdmin(admin.ModelAdmin):
    list_display = ['documento', 'fecha_revision', 'revisor', 'estado', 'fecha_proxima_revision']
    list_filter = ['estado', 'fecha_revision', 'fecha_proxima_revision']
    search_fields = ['documento__titulo', 'revisor__username', 'observaciones']
    date_hierarchy = 'fecha_revision'
    readonly_fields = ['fecha_creacion']

# Personalización del sitio de administración
admin.site.site_header = 'Laboratorio de Pruebas Mecánicas'
admin.site.site_title = 'Sistema de Calidad'
admin.site.index_title = 'Panel de Administración'