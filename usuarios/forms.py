from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Correo Electrónico'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Correo electrónico')}),
        required=True
    )
    
    password1 = forms.CharField(
        label=_('Contraseña'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Contraseña')}),
        help_text=_('La contraseña debe tener al menos 8 caracteres y no ser demasiado común.')
    )
    
    password2 = forms.CharField(
        label=_('Confirmar Contraseña'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirmar contraseña')}),
        help_text=_('Ingrese la misma contraseña que antes, para verificación.')
    )
    
    razon_social = forms.CharField(
        label=_('Razón Social'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Razón social o nombre del comercio')}),
        max_length=100,
        required=True
    )
    
    nit = forms.CharField(
        label=_('NIT'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Número de Identificación Tributaria')}),
        max_length=20,
        required=True,
        help_text=_('Ingrese el NIT sin puntos ni guiones.')
    )
    username = forms.CharField(
        label=_('Nombre de usuario'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre de usuario único')}),
        help_text=_('Será usado junto con tu NIT para iniciar sesión. Puede contener letras, números y @/./+/-/_ solamente.'),
    )
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'telefono', 
            'nit', 'nombre_representante_legal', 'razon_social',
            'regimen_tributario', 'actividad_economica',
            'responsabilidad_tributaria',
            'agente_retenedor_iva', 'sitio_web', 'direccion_establecimiento', 
            'password1', 'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre de usuario')}),
            'regimen_tributario': forms.Select(attrs={'class': 'form-control'}),
            'direccion_establecimiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Teléfono de contacto')}),
            'nombre_representante_legal': forms.TextInput(attrs={'class': 'form-control'}),
            'responsabilidad_tributaria': forms.Select(attrs={'class': 'form-control'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com'}),
            'actividad_economica': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_nit(self):
        nit = self.cleaned_data.get('nit')
        if not nit.isdigit():
            raise forms.ValidationError(_('El NIT debe contener solo números.'))
        return nit

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Usuario o NIT'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Usuario o NIT')}),
    )
    password = forms.CharField(
        label=_('Contraseña'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Contraseña')}),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            user_by_username = authenticate(
                self.request,
                username=username,
                password=password
            )
            
            if user_by_username is None:
                try:
                    user_by_nit = Usuario.objects.get(nit=username)
                    user_by_nit = authenticate(
                        self.request,
                        username=user_by_nit.username,
                        password=password
                    )
                    if user_by_nit is not None:
                        self.user_cache = user_by_nit
                    else:
                        raise forms.ValidationError(
                            self.error_messages['invalid_login'],
                            code='invalid_login',
                            params={'username': self.username_field.verbose_name},
                        )
                except Usuario.DoesNotExist:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
            
            else:
                self.user_cache = user_by_username

        return self.cleaned_data