from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    correo = forms.EmailField(required=False, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'apellido',
            'telefono',
            'correo',
            'direccion',
        ]
