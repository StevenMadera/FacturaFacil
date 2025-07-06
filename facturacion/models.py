
from django.db import models
from django.utils.translation import gettext_lazy as _
from usuarios.models import Usuario
from productos.models import Producto

class SecuenciaFactura(models.Model):
    ultimo_numero = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name = _('Secuencia de Factura')
        verbose_name_plural = _('Secuencias de Factura')
    def __str__(self):
        return f"Secuencia actual: {self.ultimo_numero}"

class Cliente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='clientes')
    nombre = models.CharField(_('Nombre completo/Razón social'), max_length=100)
    identificacion = models.CharField(_('Identificación (NIT/Cédula)'), max_length=20)
    direccion = models.TextField(_('Dirección'))
    telefono = models.CharField(_('Teléfono'), max_length=20, blank=True)
    email = models.EmailField(_('Email'), blank=True)

    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def __str__(self):
        return f"{self.nombre} ({self.identificacion})"

class Factura(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='facturas')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='facturas')
    fecha = models.DateField(_('Fecha de emisión'), auto_now_add=True)
    numero = models.CharField(_('Número de factura'), max_length=20, unique=True)
    subtotal = models.DecimalField(_('Subtotal'), max_digits=12, decimal_places=2)
    impuestos = models.DecimalField(_('Impuestos'), max_digits=12, decimal_places=2)
    total = models.DecimalField(_('Total'), max_digits=12, decimal_places=2)
    pagada = models.BooleanField(_('Pagada'), default=False)
    ESTADO_CHOICES = [
        ('borrador', _('Borrador')),
        ('emitida', _('Emitida')),
        ('enviada', _('Enviada')),
    ]
    estado = models.CharField(_('Estado de envío'), max_length=10, choices=ESTADO_CHOICES, default='emitida')

    class Meta:
        verbose_name = _('Factura')
        verbose_name_plural = _('Facturas')

    def __str__(self):
        return f"Factura #{self.numero} - {self.cliente.nombre}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(_('Cantidad'), max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(_('Precio unitario'), max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(_('Impuesto (%)'), max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = _('Detalle de factura')
        verbose_name_plural = _('Detalles de factura')

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    @property
    def total_impuesto(self):
        return self.subtotal * (self.impuesto / 100)

    @property
    def total(self):
        return self.subtotal + self.total_impuesto