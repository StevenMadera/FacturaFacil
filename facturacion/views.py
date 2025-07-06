from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import Cliente, Factura, SecuenciaFactura, DetalleFactura
from .forms import ClienteForm, DetalleFacturaForm, FacturaPagoForm
from django.contrib import messages
from django.utils import timezone



DetalleFacturaFormSet = formset_factory(DetalleFacturaForm, extra=1)

@login_required
def crear_factura(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        pago_form = FacturaPagoForm(request.POST)
        detalle_formset = DetalleFacturaFormSet(
            request.POST,
            prefix='detalles',
            form_kwargs={'usuario': request.user}
        )
        if cliente_form.is_valid() and pago_form.is_valid() and detalle_formset.is_valid():
            try:
                cliente = cliente_form.save(commit=False)
                cliente.usuario = request.user
                cliente.save()

                secuencia, _ = SecuenciaFactura.objects.get_or_create(id=1)
                secuencia.ultimo_numero += 1
                secuencia.save(update_fields=["ultimo_numero"])
                numero_factura = f"FAC-{secuencia.ultimo_numero}"

                factura = Factura.objects.create(
                    usuario=request.user,
                    cliente=cliente,
                    numero=numero_factura,
                    subtotal=0,
                    impuestos=0,
                    total=0,
                    metodo_pago=pago_form.cleaned_data['metodo_pago']
                )

                subtotal = 0
                total_impuestos = 0
                for form in detalle_formset:
                    if form.cleaned_data:
                        producto = form.cleaned_data['producto']
                        cantidad = form.cleaned_data['cantidad']
                        precio_unitario = producto.precio
                        valor_impuesto = producto.impuesto
                        subtotal_detalle = cantidad * precio_unitario
                        impuesto_detalle = subtotal_detalle * (valor_impuesto / 100)
                        DetalleFactura.objects.create(
                            factura=factura,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=valor_impuesto
                        )
                        subtotal += subtotal_detalle
                        total_impuestos += impuesto_detalle
                factura.subtotal = subtotal
                factura.impuestos = total_impuestos
                factura.total = subtotal + total_impuestos
                factura.save()
                messages.success(request, f'Factura {factura.numero} creada exitosamente!')
                return redirect('facturacion:lista_facturas')
            except Exception as e:
                messages.error(request, f'Error al crear factura: {str(e)}')
                print(f"Error detallado: {str(e)}")
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        cliente_form = ClienteForm()
        pago_form = FacturaPagoForm()
        detalle_formset = DetalleFacturaFormSet(
            prefix='detalles',
            form_kwargs={'usuario': request.user}
        )
    return render(request, 'facturacion/crear_factura.html', {
        'cliente_form': cliente_form,
        'pago_form': pago_form,
        'detalle_formset': detalle_formset,
    })

@login_required
def lista_facturas(request):
    facturas = Factura.objects.filter(usuario=request.user)
    facturas = facturas.select_related('cliente').prefetch_related('detalles').order_by('-fecha', '-id')
    return render(request, 'facturacion/lista_facturas.html', {
        'facturas': facturas,
        'now': timezone.now()
    })