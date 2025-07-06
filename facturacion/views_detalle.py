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
    get_object_or_404(Factura, pk=pk, usuario=request.user).delete()
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
    return render(request, 'facturacion/detalle_factura.html', {
        'factura': factura,
        'detalles': factura.detalles.select_related('producto').all()
    })



@login_required
def factura_pdf(request, pk):
    from usuarios.models import Usuario
    factura = get_object_or_404(Factura, pk=pk, usuario=request.user)
    if factura.estado != 'enviada':
        factura.estado = 'enviada'
        factura.save(update_fields=['estado'])
    empresa = None
    if hasattr(request.user, 'razon_social'):
        empresa = {
            'razon_social': getattr(request.user, 'razon_social', ''),
            'nit': getattr(request.user, 'nit', ''),
            'direccion_establecimiento': getattr(request.user, 'direccion_establecimiento', ''),
            'telefono': getattr(request.user, 'telefono', ''),
            'email': getattr(request.user, 'email', ''),
            'regimen_tributario': getattr(request.user, 'regimen_tributario', ''),
        }

    detalles = factura.detalles.select_related('producto').all()
    if detalles:
        impuestos_set = set([float(d.impuesto) for d in detalles])
        if len(impuestos_set) == 1:
            porcentaje_iva = impuestos_set.pop()
        else:
            porcentaje_iva = 0
    else:
        porcentaje_iva = 0



    html = get_template('facturacion/pdf_factura.html').render({
        'factura': factura,
        'detalles': detalles,
        'empresa': empresa,
        'impuesto': porcentaje_iva
    })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="factura_{factura.numero}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
