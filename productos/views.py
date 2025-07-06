from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm
from django.contrib import messages

@login_required
def lista_productos(request):
    productos = Producto.objects.filter(usuario=request.user, activo=True)
    productos = Producto.objects.filter(usuario=request.user, activo=True)
    return render(request, 'productos/lista.html', {'productos': productos})
@login_required
def nuevo_producto(request):
    form = ProductoForm(request.POST or None, usuario=request.user)
    if request.method == 'POST' and form.is_valid():
        producto = form.save(commit=False)
        producto.usuario = request.user
        producto.save()
        messages.success(request, 'Producto creado correctamente')
        return redirect('productos:lista')
    return render(request, 'productos/nuevo.html', {'form': form})