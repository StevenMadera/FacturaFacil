from django.db import models
from django.utils.translation import gettext_lazy as _
from usuarios.models import Usuario

class Producto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='productos')
    codigo = models.CharField(_('Código'), max_length=20)
    nombre = models.CharField(_('Nombre'), max_length=100)
    descripcion = models.TextField(_('Descripción'), blank=True)
    precio = models.DecimalField(_('Precio'), max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(_('Impuesto (%)'), max_digits=5, decimal_places=2, default=0)
    activo = models.BooleanField(_('Activo'), default=True)
    creado = models.DateTimeField(_('Creado'), auto_now_add=True)
    actualizado = models.DateTimeField(_('Actualizado'), auto_now=True)

    class Meta:
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')
        ordering = ['nombre']
        unique_together = ['usuario', 'codigo']  # Código único por usuario

    def __str__(self):
        return f"{self.nombre} (${self.precio})"