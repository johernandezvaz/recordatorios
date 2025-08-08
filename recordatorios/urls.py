from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # URLs para documentos
    path('documentos/', views.DocumentoListView.as_view(), name='documento_list'),
    path('documentos/<int:pk>/', views.DocumentoDetailView.as_view(), name='documento_detalle'),
    path('documentos/nuevo/', views.DocumentoCreateView.as_view(), name='documento_crear'),
    path('documentos/<int:pk>/editar/', views.DocumentoUpdateView.as_view(), name='documento_editar'),
    
    # URLs para recordatorios
    path('recordatorios/', views.RecordatorioListView.as_view(), name='recordatorio_list'),
    path('recordatorios/<int:pk>/', views.RecordatorioDetailView.as_view(), name='recordatorio_detalle'),
    path('recordatorios/nuevo/', views.RecordatorioCreateView.as_view(), name='recordatorio_crear'),
    path('recordatorios/<int:pk>/editar/', views.RecordatorioUpdateView.as_view(), name='recordatorio_editar'),
    path('recordatorios/<int:pk>/completar/', views.marcar_completado, name='recordatorio_completar'),
]