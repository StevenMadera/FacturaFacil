from django.urls import path
from .views import lista_productos, nuevo_producto
from django.contrib.auth.decorators import login_required

app_name = 'productos'

urlpatterns = [
    path('', login_required(lista_productos), name='lista'),
    path('nuevo/', login_required(nuevo_producto), name='nuevo'),
]