from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from .models import Usuario

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
           
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, _('¡Registro exitoso! Bienvenido a Factura Fácil.'))
                return redirect('usuarios:inicio')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('usuarios:inicio')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is None:
                try:
                    user_by_nit = Usuario.objects.get(nit=username)
                    user = authenticate(
                        username=user_by_nit.username, 
                        password=password
                    )
                except Usuario.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, _('¡Bienvenido de nuevo!'))
                next_url = request.GET.get('next', 'usuarios:inicio')
                return redirect(next_url)
            
        messages.error(request, _('Usuario/NIT o contraseña incorrectos.'))
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, _('Has cerrado sesión correctamente.'))
    return redirect('usuarios:login')

@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html', {'user': request.user})

class HomeView(TemplateView):
    template_name = 'usuarios/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['nombre_comercio'] = self.request.user.razon_social
        return context