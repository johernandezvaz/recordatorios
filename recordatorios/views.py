from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Documento, RecordatorioRevision, TipoDocumento
from .forms import DocumentoForm, RecordatorioRevisionForm, CustomUserCreationForm

def registro(request):
    """Vista para registro de nuevos usuarios"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'¡Cuenta creada exitosamente para {user.username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/registro.html', {'form': form})
@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    # Estadísticas generales
    total_documentos = Documento.objects.count()
    documentos_activos = Documento.objects.filter(estado='aprobado').count()
    total_recordatorios = RecordatorioRevision.objects.count()
    recordatorios_pendientes = RecordatorioRevision.objects.filter(estado='pendiente').count()
    
    # Recordatorios próximos a vencer (próximos 7 días)
    fecha_limite = timezone.now() + timedelta(days=7)
    recordatorios_proximos = RecordatorioRevision.objects.filter(
        fecha_proxima_revision__lte=fecha_limite,
        estado='pendiente'
    ).order_by('fecha_proxima_revision')[:5]
    
    # Recordatorios vencidos
    recordatorios_vencidos = RecordatorioRevision.objects.filter(
        fecha_proxima_revision__lt=timezone.now(),
        estado='pendiente'
    ).order_by('fecha_proxima_revision')[:5]
    
    # Documentos por tipo
    documentos_por_tipo = TipoDocumento.objects.annotate(
        total_documentos=Count('documento')
    ).filter(total_documentos__gt=0)
    
    context = {
        'total_documentos': total_documentos,
        'documentos_activos': documentos_activos,
        'total_recordatorios': total_recordatorios,
        'recordatorios_pendientes': recordatorios_pendientes,
        'recordatorios_proximos': recordatorios_proximos,
        'recordatorios_vencidos': recordatorios_vencidos,
        'documentos_por_tipo': documentos_por_tipo,
    }
    
    return render(request, 'recordatorios/dashboard.html', context)

class DocumentoListView(LoginRequiredMixin, ListView):
    model = Documento
    template_name = 'recordatorios/documento_list.html'
    context_object_name = 'documentos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Documento.objects.select_related('tipo', 'creado_por')
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(codigo_documento__icontains=search) |
                Q(descripcion__icontains=search)
            )
        
        # Filtro por tipo
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_id=tipo)
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_documento'] = TipoDocumento.objects.filter(activo=True)
        context['estados'] = Documento.ESTADO_CHOICES
        return context

class DocumentoDetailView(LoginRequiredMixin, DetailView):
    model = Documento
    template_name = 'recordatorios/documento_detail.html'
    context_object_name = 'documento'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recordatorios'] = RecordatorioRevision.objects.filter(
            documento=self.object
        ).order_by('-fecha_revision')
        return context

class DocumentoCreateView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'recordatorios/documento_form.html'
    success_url = reverse_lazy('documento_list')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, 'Documento creado exitosamente.')
        return super().form_valid(form)

class DocumentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'recordatorios/documento_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Documento actualizado exitosamente.')
        return super().form_valid(form)

class RecordatorioListView(LoginRequiredMixin, ListView):
    model = RecordatorioRevision
    template_name = 'recordatorios/recordatorio_list.html'
    context_object_name = 'recordatorios'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = RecordatorioRevision.objects.select_related('documento', 'revisor')
        
        # Filtros
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        prioridad = self.request.GET.get('prioridad')
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        
        # Filtro especial para vencidos
        if self.request.GET.get('vencidos') == '1':
            queryset = queryset.filter(
                fecha_proxima_revision__lt=timezone.now(),
                estado='pendiente'
            )
        
        return queryset.order_by('-fecha_revision')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = RecordatorioRevision.ESTADO_CHOICES
        context['prioridades'] = RecordatorioRevision.PRIORIDAD_CHOICES
        return context

class RecordatorioDetailView(LoginRequiredMixin, DetailView):
    model = RecordatorioRevision
    template_name = 'recordatorios/recordatorio_detail.html'
    context_object_name = 'recordatorio'

class RecordatorioCreateView(LoginRequiredMixin, CreateView):
    model = RecordatorioRevision
    form_class = RecordatorioRevisionForm
    template_name = 'recordatorios/recordatorio_form.html'
    success_url = reverse_lazy('recordatorio_list')
    
    def get_initial(self):
        initial = super().get_initial()
        documento_id = self.request.GET.get('documento_id')
        if documento_id:
            initial['documento'] = documento_id
        return initial
    
    def form_valid(self, form):
        form.instance.revisor = self.request.user
        messages.success(self.request, 'Recordatorio de revisión creado exitosamente.')
        return super().form_valid(form)

class RecordatorioUpdateView(LoginRequiredMixin, UpdateView):
    model = RecordatorioRevision
    form_class = RecordatorioRevisionForm
    template_name = 'recordatorios/recordatorio_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Recordatorio actualizado exitosamente.')
        return super().form_valid(form)

@login_required
def marcar_completado(request, pk):
    """Vista para marcar un recordatorio como completado"""
    recordatorio = get_object_or_404(RecordatorioRevision, pk=pk)
    recordatorio.estado = 'completado'
    recordatorio.fecha_completado = timezone.now()
    recordatorio.save()
    
    messages.success(request, 'Recordatorio marcado como completado.')
    return redirect('recordatorio_detail', pk=pk)