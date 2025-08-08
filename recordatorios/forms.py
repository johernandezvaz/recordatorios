from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Documento, RecordatorioRevision, TipoDocumento

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'correo@laboratorio.com'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apellidos'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
        
        # Personalizar etiquetas en español
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        
        # Personalizar mensajes de ayuda
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Solo letras, números y @/./+/-/_ permitidos.'
        self.fields['password1'].help_text = 'Su contraseña debe contener al menos 8 caracteres.'
        self.fields['password2'].help_text = 'Ingrese la misma contraseña para verificación.'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'codigo_documento', 'descripcion', 'tipo', 'version', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título del documento'
            }),
            'codigo_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: LAB-DOC-001'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del documento'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1.0'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class RecordatorioRevisionForm(forms.ModelForm):
    class Meta:
        model = RecordatorioRevision
        fields = [
            'documento', 'fecha_revision', 'fecha_proxima_revision',
            'estado', 'prioridad', 'observaciones', 'hallazgos', 'acciones_correctivas'
        ]
        widgets = {
            'documento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_revision': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_proxima_revision': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones generales de la revisión'
            }),
            'hallazgos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Hallazgos encontrados durante la revisión'
            }),
            'acciones_correctivas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Acciones correctivas a implementar'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['documento'].queryset = Documento.objects.filter(estado='aprobado')
        
        # Establecer fecha actual como predeterminada
        if not self.instance.pk:
            self.fields['fecha_revision'].initial = timezone.now()