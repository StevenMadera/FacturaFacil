from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    razon_social = models.CharField(_('Razón Social'), max_length=100)
    nit = models.CharField(_('NIT'), max_length=20, unique=True)
    
    REGIMEN_CHOICES = [
        ('comun', 'Régimen Común'),
        ('simplificado', 'Régimen Simplificado'),
        ('simple', 'SIMPLE'),
        ('especial', 'Régimen Especial'),
    ]
    regimen_tributario = models.CharField(
        _('Régimen Tributario'), 
        max_length=20, 
        choices=REGIMEN_CHOICES,
        default='comun'
    )
    
    direccion_establecimiento = models.TextField(_('Dirección del Establecimiento'))
    telefono = models.CharField(_('Teléfono'), max_length=20)
    nombre_representante_legal = models.CharField(
        _('Nombre del Representante Legal'), 
        max_length=100
    )
    
    RESPONSABILIDAD_CHOICES = [
        ('ninguna', 'Ninguna'),
        ('gran_contribuyente', 'Gran Contribuyente'),
        ('autoretenedor', 'Autorretenedor'),
        ('responsable_iva', 'Responsable de IVA'),
    ]
    responsabilidad_tributaria = models.CharField(
        _('Responsabilidad Tributaria'), 
        max_length=20, 
        choices=RESPONSABILIDAD_CHOICES,
        default='ninguna'
    )
    
    agente_retenedor_iva = models.BooleanField(
        _('Agente Retenedor de IVA'), 
        default=False
    )

    sitio_web = models.URLField(_('Sitio Web'), blank=True, null=True)
    actividad_economica = models.CharField(
        _('Actividad Económica'), 
        max_length=100, 
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return f"{self.razon_social} (NIT: {self.nit})"

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')