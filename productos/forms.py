from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'precio', 'impuesto', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Producto.objects.filter(usuario=self.usuario, codigo=codigo).exists():
            raise forms.ValidationError('Ya tienes un producto con este código')
        return codigo