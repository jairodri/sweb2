from django.forms import *
from core.sweb.models import FormaDePago


class FormaDePagoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for f in self.visible_fields():
        #     f.field.widget.attrs['class'] = 'form-control'
        self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = FormaDePago
        fields = '__all__'
        # se excluye el id por defecto
        # exclude = ['id']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'recibos': 'Recibos',
            'diasvto': 'Vencimiento Factura'
        }
        # widgets = {
        #     'codigo': TextInput(),
        #     'descripcion': TextInput(),
        #     'recibos': NumberInput(),
        #     'diasvto': NumberInput()
        # }
