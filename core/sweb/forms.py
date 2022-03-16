from django.forms import *
from core.sweb.models import *
from core.sweb.utils import digitos_control
from schwifty import IBAN
from django.contrib import messages

LIST_TABLES = [
    ('01', 'Descuentos MO'),
    ('02', 'Tipos de Cliente'),
    ('03', 'Formas de Pago'),
    ('04', 'Bancos'),
    ('05', 'Clientes/Proveedores'),
]


class ImportarForm(Form):
    lista_tablas = CharField(widget=Select(choices=LIST_TABLES))
    fichero_tabla = FileField()

    def clean(self):
        cleaned_data = self.cleaned_data
        # print(cleaned_data)


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


class ClientLopdForm(ModelForm):

    class Meta:
        model = Cliente
        fields = ['codigo',
                  'razonSocial',
                  'lopd1',
                  'lopd2',
                  'lopd3',
                  'lopdfirma',
                  ]
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'razonSocial': 'Razón Social',
            'lopd1': 'CITROEN y el Reparador incluidos medios electrónicos',
            'lopd2': 'El Reparador, incluido por medios electrónicos',
            'lopd3': 'Cualquier sociedad perteneciente al grupo que CITROEN en España, (Groupe PSA matriz - Peugeot, S.A.) dedicadas al sector de la automoción, y la financiación, incluido por medios electrónicos, y sus redes de distribuidores de vehículos y servicios oficiales de reparación.',
            'lopdfirma': 'Firmado LOPD',
        }
        widgets = {
            'codigo': TextInput(attrs={'maxlength': 6, 'required': True}),
            'lopd1': CheckboxInput(attrs={'id': 'lopd1'}),
            'lopd2': CheckboxInput(attrs={'id': 'lopd2'}),
            'lopd3': CheckboxInput(attrs={'id': 'lopd3'}),
            'lopdfirma': CheckboxInput(attrs={'id': 'lopdfirma'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        print(f'LOPD form: {cleaned_data}')
        return cleaned_data


class ClienteForm(ModelForm):

    confirm_cif = BooleanField(label='Confirmar CIF', required=False, widget=HiddenInput(attrs={'id': 'confirm_cif'}))
    # confirm_cif.required = False

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
                  'nombre',
                  'apellido1',
                  'apellido2',
                  'fechaUltimoMovimiento',
                  'creditoDispuesto',
                  'importeRecambiosMes',
                  'costeRecambiosMes',
                  'importeRecambiosAno',
                  'costeRecambiosAno',
                  'importeTallerMes',
                  'costeTallerMes',
                  'importeTallerAno',
                  'costeTallerAno',
                  'importeRecambiosTallerMes',
                  'importeRecambiosTallerAno',
                  'costeRecambiosTallerMes',
                  'costeRecambiosTallerAno',
                  'comprasMes',
                  'comprasAno',
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
            'telefono': 'Teléfono',
            'tlfmovil': 'Móvil',
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
            'nombre': 'Nombre',
            'apellido1': 'Apellido 1',
            'apellido2': 'Apellido 2',
            'fechaUltimoMovimiento': 'Fecha Último Movimiento',
            'creditoDispuesto': 'Crédito Dispuesto',
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
            'telefono': TextInput(attrs={'minlength': 9}),
            'tlfmovil': TextInput(attrs={'minlength': 9}),
            'ocultarCuenta': CheckboxInput(attrs={'id': 'ocultarCuenta'}),
            'emitirRecibos': CheckboxInput(attrs={'id': 'emitirRecibos'}),
            'email': EmailInput(),
            'cif': TextInput(attrs={'required': False}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']

        if not codigo:
            raise ValidationError('El campo Código es obligatorio')

        # convertimos a mayúsculas
        codigo = codigo.upper()

        # rellenamos con ceros a la izquierda
        if codigo.strip().isdecimal():
            codigo = codigo.strip().zfill(6)

        # en altas comprobamos si ya existe en la tabla otro código igual
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            pass
        else:
            clientes = Cliente.objects.filter(codigo=codigo)
            # print(clientes)
            if clientes:
                raise ValidationError('Ya existe un Cliente con este Código: %(value)s', code='coddup', params={'value': codigo})

        return codigo

    def validar_nif(self):
        cif = self.cleaned_data['cif']

        tabla_letras_nif = "TRWAGMYFPDXBNJZSQVHLCKE"
        numeros = "1234567890"
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
        print(f'indice:{int(nif) % 23}')
        indice = int(nif) % 23
        # if indice > 22:
        #     raise ValidationError('El formato del CIF/NIF es incorrecto')

        if tabla_letras_nif[indice] != letra:
            raise ValidationError('El formato del CIF/NIF es incorrecto')

        return cif

    def clean_cif(self):
        cif = self.cleaned_data['cif']

        if not cif:
            return cif
        cif = self.validar_nif()

        return cif

    def clean_email(self):
        email = self.cleaned_data['email']
        # print(email)

        # Hay que tener cuidado antes de hacer el lower porque cuando está vacío devuelve None
        if not email:
            return email

        # convertimos los email a minúsculas
        email = str(email).lower()
        return email

    def clean_dtopieza(self):
        dtopieza = self.cleaned_data['dtopieza']

        # Si el código de descuento de pieza no está relleno, lo inicializamos con '0'
        if not dtopieza:
            dtopieza = '0'
        return dtopieza

    def clean_ivaEpecial(self):
        iva_epecial = self.cleaned_data['ivaEpecial']

        # Si el iva especial no está relleno, lo inicializamos con 0
        if not iva_epecial:
            iva_epecial = 0
        else:
            validar_porcentaje(iva_epecial)
        return iva_epecial

    def clean_precioMo(self):
        precio_mo = self.cleaned_data['precioMo']

        # el precio de mo no puede ser de 1000 o superior
        if precio_mo and precio_mo > 999.99:
            raise ValidationError('Precio MO tiene que ser menor de 1000: %(value)s', code='pvpinvalid',
                                  params={'value': precio_mo})
        return precio_mo

    def clean_dtoEpecial(self):
        dto_epecial = self.cleaned_data['dtoEpecial']

        # Si el descuento especial no está relleno, lo inicializamos con 0
        if not dto_epecial:
            dto_epecial = 0
        else:
            validar_porcentaje(dto_epecial)
        return dto_epecial

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

    def clean_cuenta(self):
        cuenta = self.cleaned_data['cuenta']

        # si existe cuenta debe ser de 10 dígitos
        if cuenta:
            if len(cuenta) == 10 and cuenta.isdigit():
                pass
            else:
                raise ValidationError('Cuenta debe tener 10 dígitos: %(value)s', code='ctainvalid', params={'value': cuenta})
        return cuenta

    # definimos método para obtener DC e IBAN
    def clean_dc_iban(self):
        cleaned_data = self.cleaned_data

        cuenta = cleaned_data['cuenta']
        banco = cleaned_data['banco']

        # obenemos el DC
        dc = banco.dgc + digitos_control(cuenta)

        # obenemos el IBAN
        country_code = 'ES'
        bank_code = banco.codigo + banco.sucursal
        account_code = dc + cuenta
        iban_obj = IBAN.generate(country_code=country_code, bank_code=bank_code, account_code=account_code)
        iban = country_code + iban_obj.checksum_digits

        cleaned_data['dc'] = dc
        cleaned_data['iban'] = iban
        return cleaned_data

    def validar_cif_duplicado(self):
        # Comprobamos primero si hay código, puesto que hubo una validación anterior
        try:
            codigo = self.cleaned_data['codigo']
            cif = self.cleaned_data['cif']
        except KeyError:
            # si no hay código no continuamos con la validación
            return

        confirm_cif = self.cleaned_data['confirm_cif']
        # cif = self.cleaned_data['cif']
        # print(f'cif:{cif} - confirm_cif:{confirm_cif}')

        if not cif:
            return

        clientes = Cliente.objects.filter(cif=cif).exclude(codigo=codigo)
        if clientes and not confirm_cif:
            self.fields['confirm_cif'].widget = widgets.CheckboxInput(attrs={'id': 'confirm_cif'})
            self.fields['confirm_cif'].required = False
            raise ValidationError('El CIF/NIF ya existe en el cliente: %(value)s. Confirme para validar', code='cifdup',
                                  params={'value': clientes[0].codigo})
        else:
            self.fields['confirm_cif'].widget = widgets.HiddenInput(attrs={'id': 'confirm_cif'})
            self.fields['confirm_cif'].required = False

    def clean(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)

        # validamos si el cif está duplicado
        self.validar_cif_duplicado()

        # Si la validación de la cuenta ha fallado (clean_cuenta) y se ha lanzado el ValidationError
        # ya no tenemos ese campo en cleaned_data por lo que obtenemos KeyError al ir a buscarlo
        try:
            # obtenemos DC e IBAN dependiendo del contenido de los campos Cuenta y Banco
            cuenta = cleaned_data['cuenta']
            banco = cleaned_data['banco']
            if (not cuenta) or (not banco):
                dc = None
                iban = None
                cleaned_data['dc'] = dc
                cleaned_data['iban'] = iban
            else:
                cleaned_data = self.clean_dc_iban()
        except KeyError:
            # ya ha habido una validación errónea en la cuenta por lo que no tenemos que hacer nada
            pass

        # Si está activo el envío SMS el teléfono móvil debe estar relleno
        enviarSms = cleaned_data['enviarSms']
        tlfmovil = cleaned_data['tlfmovil']
        if enviarSms != '0':
            if not tlfmovil:
                raise ValidationError('Si se activa el envío SMS es necesario rellenar el teléfono móvil')

        return cleaned_data


class NumeracionAutomaticaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = NumeracionAutomatica
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'tabla': 'Tipo de Movimiento',
            'serie': 'Serie',
            'contador': 'Contador',
            'activo': 'Activo',
        }
        widgets = {
            'codigo': TextInput(attrs={'minlength': 2, 'required': True}),
            'tabla': TextInput(attrs={'required': True}),
            'activo': CheckboxInput(attrs={'id': 'activo'}),
        }


class UnidadMedidaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = UnidadMedida
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'minlength': 1, 'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class CodigoAproPiezaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = CodigoAproPieza
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'minlength': 1, 'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }
