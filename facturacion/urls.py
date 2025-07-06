from django.urls import path
from .views import crear_factura, lista_facturas
from .views_detalle import detalle_factura, factura_pdf, marcar_factura_enviada, eliminar_factura
from django.contrib.auth.decorators import login_required

app_name = 'facturacion'

urlpatterns = [
    path('', login_required(lista_facturas), name='lista_facturas'),
    path('nueva/', login_required(crear_factura), name='crear_factura'),
    path('detalle/<int:pk>/', login_required(detalle_factura), name='detalle_factura'),
    path('detalle/<int:pk>/pdf/', login_required(factura_pdf), name='factura_pdf'),
    path('detalle/<int:pk>/marcar_enviada/', login_required(marcar_factura_enviada), name='marcar_factura_enviada'),
    path('detalle/<int:pk>/eliminar/', login_required(eliminar_factura), name='eliminar_factura'),
]