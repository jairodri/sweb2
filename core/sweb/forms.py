from django.forms import *
from core.sweb.models import *


class FormaDePagoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = FormaDePago
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'recibos': 'Recibos',
            'diasvto': 'Días Vencimiento Factura'
        }
        widgets = {
            'codigo': TextInput(attrs={'minlength': 2, 'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
            'recibos': NumberInput(attrs={'required': True}),
            'diasvto': NumberInput(attrs={'required': True}),
        }


class TipoClienteRecambiosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
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
        widgets = {
            'codigo': TextInput(attrs={'minlength': 2, 'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
            'datocontable': TextInput(attrs={'required': True}),
        }


class DescuentoMOForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
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
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
            'descuento': NumberInput(attrs={'required': True}),
        }


class BancoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['codigo'].disabled = True
            self.fields['sucursal'].disabled = True
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
        widgets = {
            'codigo': NumberInput(attrs={'minlength': 4, 'required': True}),
            'sucursal': NumberInput(attrs={'minlength': 4, 'required': True}),
            'razonsocial': TextInput(attrs={'required': True}),
            'tipovia': TextInput(attrs={'required': True}),
            'nomvia': TextInput(attrs={'required': True}),
            'numvia': TextInput(attrs={'required': True}),
            'codpostal': TextInput(attrs={'required': True}),
            'municipio': TextInput(attrs={'required': True}),
            'provincia': TextInput(attrs={'required': True}),
        }


class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['codigo'].disabled = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = ['codigo',
                  'razonSocial',
                  'tipoCliente',
                  'direccion',
                  'codpostal',
                  'poblacion',
                  'provincia',
                  'cif',
                  'fechaNacimiento',
                  ]
        exclude = ['user_creation', 'user_updated']

        labels = {
            'codigo': 'Código',
            'razonSocial': 'Razón Social',
            'tipoCliente': 'Tipo',
            'direccion': 'Dirección',
            'codpostal': 'Código Postal',
            'poblacion': 'Población',
            'provincia': 'Provincia',
            'cif': 'CIF/NIF',
            'fechaNacimiento': 'Fecha Nacimiento',
        }
        widgets = {
            'codigo': TextInput(attrs={'maxlength': 6, 'required': True}),
            'tipoCliente': Select(attrs={'required': True}, ),
            'razonsocial': TextInput(),
            'direccion': TextInput(),
            'codpostal': TextInput(),
            'poblacion': TextInput(),
            'provincia': TextInput(),
            'cif': TextInput(),
            # 'fechaNacimiento': DateInput(),
        }
