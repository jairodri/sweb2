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
                  'telefono',
                  'tlfmovil',
                  'fax',
                  'email',
                  'notas',
                  'aplicarIva',
                  'listarnetodto',
                  'exentoMail',
                  'bloquearCredito',
                  'fechaUltimaFactura',
                  'dtopieza',
                  'dtomo',
                  'dtoEpecial',
                  'precioMo',
                  'ivaEpecial',
                  'enviarSms',
                  'diaPagoDesde',
                  'diaPagoHasta',
                  'creditoDisponible',
                  'formaDePago',
                  'banco',
                  'iban',
                  'cuenta',
                  'dc',
                  'ocultarCuenta',
                  'emitirRecibos',
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
            'telefono': 'Teléfono 1',
            'tlfmovil': 'Teléfono 2',
            'fax': 'Fax',
            'email': 'Correo electrónico',
            'notas': 'Nota',
            'aplicarIva': 'Aplicar IVA',
            'listarnetodto': 'Listar Neto y Dto.',
            'exentoMail': 'Exento Mail',
            'bloquearCredito': 'Bloquear Crédito',
            'fechaUltimaFactura': 'Fecha ültima Factura',
            'dtopieza': 'Código Descuento Piezas',
            'dtomo': 'Código Descuento M.O.',
            'dtoEpecial': 'Descuento Especial',
            'precioMo': 'Precio M.O.',
            'ivaEpecial': 'IVA Especial',
            'enviarSms': 'Enviar SMS',
            'diaPagoDesde': 'Días Pago-De',
            'diaPagoHasta': 'Días Pago-A',
            'creditoDisponible': 'Crédito',
            'formaDePago': 'Forma de Pago',
            'banco': 'Banco',
            'iban': 'IBAN',
            'cuenta': 'Cuenta',
            'dc': 'DC',
            'ocultarCuenta': 'Ocultar Cuenta',
            'emitirRecibos': 'Recibos',
        }
        widgets = {
            'codigo': TextInput(attrs={'maxlength': 6, 'required': True}),
            'tipoCliente': Select(attrs={'required': True}, ),
            'notas': Textarea(attrs={'rows': 4}),
            'aplicarIva': CheckboxInput(attrs={'id': 'aplicarIva'}),
            'listarnetodto': CheckboxInput(attrs={'id': 'listarnetodto'}),
            'exentoMail': CheckboxInput(attrs={'id': 'exentoMail'}),
            'bloquearCredito': CheckboxInput(attrs={'id': 'bloquearCredito'}),
            'dtomo': Select(attrs={'required': True}, ),
            'enviarSms': Select(attrs={'required': True}, ),
            'diaPagoDesde': NumberInput(),
            'diaPagoHasta': NumberInput(),
            'formaDePago': Select(attrs={'required': True}, ),
            'banco': Select(),
            'ocultarCuenta': CheckboxInput(attrs={'id': 'ocultarCuenta'}),
            'emitirRecibos': CheckboxInput(attrs={'id': 'emitirRecibos'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']

        # convertimos a mayúsculas
        codigo = codigo.upper()

        # rellenamos con ceros a la izquierda
        if codigo.strip().isdecimal():
            codigo = codigo.strip().zfill(6)
        return codigo

    def clean_diaPagoDesde(self):
        diaPagoDesde = self.cleaned_data['diaPagoDesde']

        # si el día de pago desde no está relleno, lo inicializamos a 1
        if not diaPagoDesde:
            diaPagoDesde = 1
        else:
            if diaPagoDesde < 1 or diaPagoDesde > 31:
                raise ValidationError('Días Pago debe estar entre 1 y 31')
        return diaPagoDesde

    def clean_diaPagoHasta(self):
        diaPagoHasta = self.cleaned_data['diaPagoHasta']

        # si el día de pago hasta no está relleno, lo inicializamos a 31
        if not diaPagoHasta:
            diaPagoHasta = 31
        else:
            if diaPagoHasta < 1 or diaPagoHasta > 31:
                raise ValidationError('Días Pago debe estar entre 1 y 31')
        return diaPagoHasta

    def clean_dtopieza(self):
        dtopieza = self.cleaned_data['dtopieza']

        # Si el código de descuento de pieza no está relleno, lo inicializamos con '0'
        if not dtopieza:
            dtopieza = '0'
        return dtopieza

    def clean_dtoEpecial(self):
        dtoEpecial = self.cleaned_data['dtoEpecial']

        # Si el descuento especial no está relleno, lo inicializamos con 0
        if not dtoEpecial:
            dtoEpecial = 0
        return dtoEpecial

    def clean_ivaEpecial(self):
        ivaEpecial = self.cleaned_data['ivaEpecial']

        # Si el iva especial no está relleno, lo inicializamos con 0
        if not ivaEpecial:
            ivaEpecial = 0
        return ivaEpecial

    def clean_cif(self):
        cif = self.cleaned_data['cif']
        tabla_letras_nif = "TRWAGMYFPDXBNJZSQVHCKE"
        numeros = "1234567890"

        if not cif:
            return cif

        cif = cif.upper()

        # si la longitud es mayor de 9, no es un nif, puede ser un pasaporte
        if len(cif) > 9:
            return cif

        # si el primer carácter es una letra, es un cif, así que no seguimos
        if cif[0].isalpha():
            return cif

        # si el último carácter no es una letra, no es un nif válido
        if not cif[-1].isalpha():
            raise ValidationError('El formato del CIF/NIF es incorrecto')

        # la longitud del nif no puede ser menor de 8, si es 8 le añadimos un cero al principio
        if len(cif) < 8:
            raise ValidationError('El formato del CIF/NIF es incorrecto')
        elif len(cif) == 8:
            cif = '0' + cif

        letra = cif[-1]
        nif = cif[:8]
        # print(f'letra:{letra}-nif:{nif}')

        # si alguno de los valores del nif menos el último no es numérico, es un error
        if len(nif) != len([n for n in nif if n in numeros]):
            raise ValidationError('El formato del CIF/NIF es incorrecto')

        # si la letra del nif no corresponde a la calculada, es un error
        # print(f'indice:{int(nif) % 23}')
        if tabla_letras_nif[int(nif) % 23] != letra:
            raise ValidationError('El formato del CIF/NIF es incorrecto')

        return cif
