from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm
from django.contrib import messages

@login_required
def lista_productos(request):
    productos = Producto.objects.filter(usuario=request.user, activo=True)
    return render(request, 'productos/lista.html', {'productos': productos})

@login_required
def nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, usuario=request.user)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user
            producto.save()
            messages.success(request, 'Producto creado correctamente')
            return redirect('productos:lista')
    else:
        form = ProductoForm(usuario=request.user)
    
    return render(request, 'productos/nuevo.html', {'form': form})