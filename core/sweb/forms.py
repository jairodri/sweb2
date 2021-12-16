from django.forms import *
from core.sweb.models import *


class FormaDePagoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for f in self.visible_fields():
        #     f.field.widget.attrs['class'] = 'form-control'
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
            self.fields['descripcion'].widget.attrs['autofocus'] = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = FormaDePago
        fields = '__all__'
        # se excluye el id por defecto
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'recibos': 'Recibos',
            'diasvto': 'Vencimiento Factura'
        }


class TipoClienteRecambiosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
            self.fields['descripcion'].widget.attrs['autofocus'] = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = TipoClienteRecambios
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'datocontable': 'Dato Contable'
        }


class DescuentoMOForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
            self.fields['descripcion'].widget.attrs['autofocus'] = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = DescuentoMO
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'descuento': 'Descuento'
        }


class BancoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
            self.fields['sucursal'].disabled = True
            # self.fields['descripcion'].widget.attrs['autofocus'] = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Banco
        fields = ['codigo',
                  'sucursal',
                  'razonsocial',
                  'tipovia',
                  'nomvia',
                  'numvia',
                  'codpostal',
                  'municipio',
                  'provincia',
                  'telefono',
                  'telex',
                  'contacto',
                  'extension',
                  'telperso'
                  ]
        exclude = ['user_creation', 'user_updated']

        labels = {
            'codigo': 'Código Banco',
            'sucursal': 'Código Sucursal',
            'razonsocial': 'Razón Social',
            'tipovia': 'Tipo Vía',
            'nomvia': 'Nombre',
            'numvia': 'Número',
            'codpostal': 'Código Postal',
            'municipio': 'Población',
            'provincia': 'Provincia',
            'telefono': 'Teléfono',
            'telex': 'Telex',
            'contacto': 'Contacto',
            'extension': 'Ext. Teléfono',
            'telperso': 'Teléfono Personal',
        }
