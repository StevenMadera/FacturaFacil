from django import forms
from .models import Cliente
from productos.models import Producto
from .models import DetalleFactura

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'identificacion', 'direccion', 'telefono', 'email']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class DetalleFacturaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if self.usuario:
            self.fields['producto'].queryset = self.get_productos_queryset()

    def get_productos_queryset(self):
        return Producto.objects.filter(
            usuario=self.usuario,
            activo=True
        ).order_by('nombre')

    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control select-producto'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'})
        }