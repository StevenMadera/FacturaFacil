

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from .models import Factura
import weasyprint


@login_required
@require_POST
def eliminar_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk, usuario=request.user)
    factura.delete()
    return JsonResponse({'ok': True})


@login_required
@require_POST
def marcar_factura_enviada(request, pk):
    factura = get_object_or_404(Factura, pk=pk, usuario=request.user)
    if factura.estado != 'enviada':
        factura.estado = 'enviada'
        factura.save(update_fields=['estado'])
    return JsonResponse({'ok': True, 'estado': factura.estado})

@login_required
def detalle_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk, usuario=request.user)
    detalles = factura.detalles.select_related('producto').all()
    return render(request, 'facturacion/detalle_factura.html', {
        'factura': factura,
        'detalles': detalles
    })


@login_required
def factura_pdf(request, pk):
    factura = get_object_or_404(Factura, pk=pk, usuario=request.user)
    detalles = factura.detalles.select_related('producto').all()
    
    if factura.estado != 'enviada':
        factura.estado = 'enviada'
        factura.save(update_fields=['estado'])
    template = get_template('facturacion/pdf_factura.html')
    html = template.render({'factura': factura, 'detalles': detalles})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="factura_{factura.numero}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
