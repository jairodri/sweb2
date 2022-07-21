import zoneinfo

from django.forms import *
from core.sweb.mixins import CodigoBaseForm
from core.sweb.models import *
from core.sweb.utils import digitos_control
from schwifty import IBAN
from decouple import config
from datetime import datetime
from django.utils.timezone import get_current_timezone

# LIST_TABLES = [
#     ('01', 'Descuentos MO'),
#     ('02', 'Tipos de Cliente'),
#     ('03', 'Formas de Pago'),
#     ('04', 'Bancos'),
#     ('05', 'Clientes/Proveedores'),
# ]
#
#
# class ImportarForm(Form):
#     lista_tablas = CharField(widget=Select(choices=LIST_TABLES))
#     fichero_tabla = FileField()
#
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         # print(cleaned_data)


class FormaDePagoForm(CodigoBaseForm, ModelForm):

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


class TipoClienteRecambiosForm(CodigoBaseForm, ModelForm):

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


class DescuentoMOForm(CodigoBaseForm, ModelForm):

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
        # print(f'LOPD form: {cleaned_data}')
        return cleaned_data


class ClienteForm(CodigoBaseForm, ModelForm):

    confirm_cif = BooleanField(label='Confirmar CIF', required=False, widget=HiddenInput(attrs={'id': 'confirm_cif'}))

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
        # print('clean cliente')
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
        # print(f'indice:{int(nif) % 23}')
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
        # print(cleaned_data)

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


class NumeracionAutomaticaForm(CodigoBaseForm, ModelForm):

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


class UnidadMedidaForm(CodigoBaseForm, ModelForm):

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


class CodigoAproPiezaForm(CodigoBaseForm, ModelForm):

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


class CodigoIvaForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = CodigoIva
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'porcentaje': '%'
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
            'porcentaje': NumberInput(attrs={'required': True}),
        }


class FamiliaPiezaForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = FamiliaPieza
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class MarcaForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = Marca
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class CodigoContableForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = CodigoContable
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class ModeloVehPiezaForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = ModeloVehPieza
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class FamiliaMarketingForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = FamiliaMarketing
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            # 'descripcion': TextInput(attrs={'required': True}),
        }


class DescuentoRecambiosForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
            self.fields['codpieza'].disabled = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = DescuentoRecambios
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'codpieza': 'Código Pieza',
            'descuento': 'Descuento'
        }
        widgets = {
            'tipo': HiddenInput(),
            'codigo': TextInput(attrs={'required': True}),
            'codpieza': TextInput(attrs={'required': True}),
            'descuento': NumberInput(attrs={'required': True}),
        }

    def clean_codigo(self):
        # print('clean mixin')
        codigo = self.cleaned_data['codigo']
        if not codigo:
            raise ValidationError('El campo Código es obligatorio')

        # convertimos a mayúsculas
        codigo = codigo.upper()
        return codigo

    def clean_codpieza(self):
        codpieza = self.cleaned_data['codpieza']
        if not codpieza:
            raise ValidationError('El campo Código Pieza es obligatorio')

        # convertimos a mayúsculas
        codpieza = codpieza.upper()
        return codpieza


class ArticuloForm(ModelForm):

    funcionCitroen = CharField(label='Contractual (S) / Rotación (R)', required=False, max_length=1)
    nr = CharField(label='1 - Cambio Dígitos, 2 - Cambio Técnico', required=False, max_length=1, widget=HiddenInput(attrs={'id': 'id_nr'}))
    traspasarCosteMedio = BooleanField(label='Traspasar Precio Coste Medio', required=False, widget=HiddenInput(attrs={'id': 'traspasarCosteMedio'}))
    cod_dto_proveedor = ''
    codAproPieza_ant = None
    bloqueo_ant = None
    nuevaref_ant = None
    es_alta = None
    referencia_nueva = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['proveedor'].queryset = Cliente.objects.none()
        self.fields['familiaMarketing'].queryset = FamiliaMarketing.objects.none()

        if 'proveedor' in self.data:
            self.fields['proveedor'].queryset = Cliente.objects.all()
        elif self.instance.pk:
            self.fields['proveedor'].queryset = Cliente.objects.all().filter(pk=self.instance.proveedor.pk)

        if 'familiaMarketing' in self.data:
            self.fields['familiaMarketing'].queryset = FamiliaMarketing.objects.all()
        elif self.instance.pk and self.instance.familiaMarketing:    # La familia marketing no es obligatoria de modo que preguntamos primero si está relleno
            self.fields['familiaMarketing'].queryset = FamiliaMarketing.objects.all().filter(pk=self.instance.familiaMarketing.pk)

        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.es_alta = False
            self.fields['referencia'].disabled = True
            self.fields['existencias'].disabled = True
            self.codAproPieza_ant = self.get_initial_for_field(self.fields['codAproPieza'], 'codAproPieza')
            self.bloqueo_ant = self.get_initial_for_field(self.fields['bloqueo'], 'bloqueo')
            self.nuevaref_ant = self.get_initial_for_field(self.fields['nuevaReferencia'], 'nuevaReferencia')
            # print(self.bloqueo_ant)
        else:
            self.es_alta = True
            self.fields['referencia'].widget.attrs['autofocus'] = True
            # self.fields['codigoApro'].choices = {}

    class Meta:
        model = Articulo
        fields = ['referencia',
                  'descripcion',
                  'tarifa',
                  'codigoPromo',
                  'familia',
                  'codigoApro',
                  'unidadMedida',
                  'codigoUrgte',
                  'existencias',
                  'nuevaReferencia',
                  'ivaPieza',
                  'unidadCompra',
                  'unidadVenta',
                  'unidadStock',
                  'codigoContable',
                  'multiplo',
                  'ubicacion',
                  'codAproPieza',
                  'marca',
                  'codigoModelo',
                  'stockSeguridad',
                  'puntoPedido',
                  'stockMinimo',
                  'consumoMedio',
                  'codigoFuncion',
                  'panier',
                  'codigoObsoleto',
                  'codigoAbc',
                  'familiaMarketing',
                  'fechaUltimaCompra',
                  'fechaAlta',
                  'proveedor',
                  'observaciones',
                  'codigoCompetencia',
                  'bloqueoPieza',
                  'fechaBloqueo',
                  'bloqueo',
                  ]
        exclude = ['user_creation', 'user_updated']

        labels = {
            'referencia': 'Referencia',
            'descripcion': 'Descripción',
            'tarifa': 'Precio venta público',
            'codigoPromo': 'Descuento promoción',
            'familia': 'Familia',
            'codigoApro': 'Descuento aprovisionamiento',
            'unidadMedida': 'Unidad de medida',
            'codigoUrgte': 'Descuento urgente',
            'existencias': 'Existencias',
            'nuevaReferencia': 'Ref. que la sustituye',
            'ivaPieza': 'Código IVA',
            'unidadCompra': 'Unidad de compra',
            'unidadVenta': 'Unidad de venta',
            'unidadStock': 'Unidad de stock',
            'codigoContable': 'Código contable',
            'multiplo': 'Múltiplo',
            'ubicacion': 'Ubicación',
            'codAproPieza': 'Código aprov. pieza',
            'marca': 'Código marca',
            'codigoModelo': 'Código modelo',
            'stockSeguridad': 'Stock de seguridad',
            'puntoPedido': 'Punto de pedido',
            'stockMinimo': 'Stock mínimo',
            'consumoMedio': 'Consumo medio',
            'codigoFuncion': 'Código función',
            'panier': 'Panier',
            'codigoObsoleto': 'Código de obsoleto',
            'codigoAbc': 'Código ABC',
            'familiaMarketing': 'Código Marketing',
            'fechaUltimaCompra': 'Fecha última compra',
            'fechaAlta': 'Fecha de alta',
            'proveedor': 'Proveedor',
            'observaciones': 'Observaciones',
            'codigoCompetencia': 'Código Competencia',
        }
        widgets = {
            'observaciones': Textarea(attrs={'rows': 4}),
            # 'proveedor': Select(),
            'codigoApro': Select(),
            'unidadCompra': NumberInput(),
            'unidadVenta': NumberInput(),
            'unidadStock': NumberInput(),
            'multiplo': NumberInput(),
            'consumoMedio': NumberInput(),
        }

    def clean_referencia(self):
        # print('clean_referencia')
        referencia = self.cleaned_data['referencia']

        if not referencia:
            raise ValidationError('Referncia obligatoria')

        # convertimos a mayúsculas
        referencia = referencia.upper()

        # en altas comprobamos si ya existe en la tabla otro código igual
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            pass
        else:
            articulos = Articulo.objects.filter(referencia=referencia)
            if articulos:
                raise ValidationError('Ya existe un Artículo con esta Referencia: %(value)s', code='coddup', params={'value': referencia})

        return referencia

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']

        if descripcion is None or descripcion == '':
            raise ValidationError('Descripción es obligatoria')

        return descripcion

    def clean_proveedor(self):
        # print('clean_proveedor')
        proveedor = self.cleaned_data['proveedor']

        if proveedor is None:
            raise ValidationError('Proveedor es obligatorio')
        else:
            self.cod_dto_proveedor = proveedor.dtopieza
            # print(f'dtopieza: {self.cod_dto_proveedor}')

        return proveedor

    def clean_existencias(self):
        existencias = self.cleaned_data['existencias']

        if existencias is None:
            existencias = 0

        return existencias

    def clean_tarifa(self):
        tarifa = self.cleaned_data['tarifa']

        if tarifa > 0:
            pass
        else:
            raise ValidationError('El Precio venta público debe ser mayor de 0: %(value)s', code='pvpinvalid',
                                  params={'value': tarifa})
        return tarifa

    def clean_nuevaReferencia(self):
        nuevaReferencia = self.cleaned_data['nuevaReferencia']

        if not nuevaReferencia:
            return nuevaReferencia

        nuevaReferencia = nuevaReferencia.upper()

        try:
            nr = Articulo.objects.get(referencia=nuevaReferencia)
        except Exception as ex:
            raise ValidationError('Artículo inexistente:  %(value)s', code='refinex', params={'value': nuevaReferencia})
        return nuevaReferencia

    def clean_codigoApro(self):
        # print('clean_codigoApro')
        codigoApro = self.cleaned_data['codigoApro']

        if codigoApro is None:
            raise ValidationError('Código descuento es obligatorio')

        return codigoApro

    def clean_unidadMedida(self):
        unidadMedida = self.cleaned_data['unidadMedida']

        if not unidadMedida:
            unidadMedida = UnidadMedida.objects.get(codigo='1')

        return unidadMedida

    def clean_ivaPieza(self):
        ivaPieza = self.cleaned_data['ivaPieza']

        if not ivaPieza:
            raise ValidationError('Código IVA obligatorio')

        return ivaPieza

    def clean_unidadCompra(self):
        unidadCompra = self.cleaned_data['unidadCompra']

        if unidadCompra is None:
            unidadCompra = 1
        elif unidadCompra < 1:
            raise ValidationError('Unidad de compra debe ser mayor de 0')

        return unidadCompra

    def clean_unidadVenta(self):
        unidadVenta = self.cleaned_data['unidadVenta']

        if unidadVenta is None:
            unidadVenta = 1
        elif unidadVenta < 1:
            raise ValidationError('Unidad de venta debe ser mayor de 0')

        return unidadVenta

    def clean_codigoContable(self):
        codigoContable = self.cleaned_data['codigoContable']

        if not codigoContable:
            codigoContable = CodigoContable.objects.get(codigo='01')

        return codigoContable

    def clean_unidadStock(self):
        unidadStock = self.cleaned_data['unidadStock']

        if unidadStock is None:
            unidadStock = 1
        elif unidadStock < 1:
            raise ValidationError('Unidad de stock debe ser mayor de 0')

        return unidadStock

    def clean_multiplo(self):
        multiplo = self.cleaned_data['multiplo']

        if multiplo is None:
            multiplo = 1
        elif multiplo < 1:
            raise ValidationError('Múltiplo debe ser mayor de 0')

        return multiplo

    def clean_consumoMedio(self):
        consumoMedio = self.cleaned_data['consumoMedio']

        if consumoMedio is None:
            consumoMedio = 0

        return consumoMedio

    def clean_codigoFuncion(self):
        codigoFuncion = self.cleaned_data['codigoFuncion']

        if not codigoFuncion:
            return codigoFuncion

        codigoFuncion = codigoFuncion.upper()
        return codigoFuncion

    def clean_codigoObsoleto(self):
        codigoObsoleto = self.cleaned_data['codigoObsoleto']

        if codigoObsoleto is None:
            codigoObsoleto = '0'

        return codigoObsoleto

    def clean_fechaAlta(self):
        fechaAlta = self.cleaned_data['fechaAlta']

        if fechaAlta is None:
            fechaAlta = datetime.now()

        return fechaAlta

    def validar_nueva_referencia(self):
        # Comprobamos primero si está el campo referencia sustituida, puesto que hubo una validación anterior
        try:
            nuevaReferencia = self.cleaned_data['nuevaReferencia']
        except KeyError:
            # si no hay campo no continuamos con la validación
            return

        if nuevaReferencia is None:
            return

        if nuevaReferencia == self.nuevaref_ant:
            return

        if config('DEFSUST') != 'S':
            return

        nr = self.cleaned_data['nr']
        if nr == '1' or nr == '2':
            self.referencia_nueva = True
            self.fields['nr'].widget = widgets.HiddenInput(attrs={'id': 'id_nr'})
            self.fields['nr'].required = False
        else:
            self.fields['nr'].widget = widgets.TextInput(attrs={'id': 'id_nr', 'maxlength': '1'})
            self.fields['nr'].required = False
            self.fields['traspasarCosteMedio'].widget = widgets.CheckboxInput(attrs={'id': 'traspasarCosteMedio'})
            self.fields['traspasarCosteMedio'].required = False
            raise ValidationError('Seleccione: 1 - Cambio Dígitos, 2 - Cambio Técnico')


    def clean(self):
        cleaned_data = self.cleaned_data
        # print(self.cleaned_data)

        self.validar_nueva_referencia()

        funcionCitroen = cleaned_data['funcionCitroen']
        codigoFuncion = cleaned_data['codigoFuncion']
        # print(funcionCitroen)
        if config('DEFCLIEN') == 'CITROEN':
            if funcionCitroen is None or funcionCitroen == '':
                pass
            elif funcionCitroen.upper() != 'S' and funcionCitroen.upper() != 'R':
                raise ValidationError("Marcar Pieza Stock Contractual - 'S' ó Marcar Pieza Gran Rotación - 'R'")
            else:
                cleaned_data['funcionCitroen'] = funcionCitroen.upper()
                cleaned_data['codigoFuncion'] = funcionCitroen.upper()

        # Validamos que el código de pieza del proveedor corresponda al código elegido en los descuentos
        codigoApro = self.cleaned_data['codigoApro']
        if codigoApro is not None and codigoApro.codigo != self.cod_dto_proveedor:
            raise ValidationError('Código descuento no es válido para el código pieza del proveedor:  %(value)s', code='coddtoko', params={'value': self.cod_dto_proveedor})
        codigoPromo = self.cleaned_data['codigoPromo']
        if codigoPromo is not None and codigoPromo.codigo != self.cod_dto_proveedor:
            raise ValidationError('Código descuento promoción no es válido para el código pieza del proveedor:  %(value)s', code='coddtoko', params={'value': self.cod_dto_proveedor})
        codigoUrgte = self.cleaned_data['codigoUrgte']
        if codigoUrgte is not None and codigoUrgte.codigo != self.cod_dto_proveedor:
            raise ValidationError('Código descuento urgente no es válido para el código pieza del proveedor:  %(value)s', code='coddtoko', params={'value': self.cod_dto_proveedor})

        # En las modificaciones comprobamos si se ha cambiado el código aprovisionamiento
        if not self.es_alta:
            codAproPieza = cleaned_data['codAproPieza']
            bloqueoPieza = cleaned_data['bloqueoPieza']
            fechaBloqueo = cleaned_data['fechaBloqueo']

            if self.codAproPieza_ant != codAproPieza.id:
                if self.codAproPieza_ant is None:
                    bloqueoPieza = None
                    fechaBloqueo = None
                else:
                    bloqueoPieza = '*'
                    fechaBloqueo = datetime.now(tz=get_current_timezone())

                cleaned_data['bloqueoPieza'] = bloqueoPieza
                cleaned_data['fechaBloqueo'] = fechaBloqueo

        # No se puede modificar una pieza bloqueada para inventario
        if not self.es_alta:
            if self.bloqueo_ant:
                raise ValidationError('Artículo pendiente de inventario')

        # print(cleaned_data)
        return cleaned_data

    def procesar_nueva_referencia(self, articulo, articulo_nuevo):
        nr = self.cleaned_data['nr']
        traspasarCosteMedio = self.cleaned_data['traspasarCosteMedio']
        # print(f'nr: {nr}')
        # print(f'traspasarCosteMedio: {traspasarCosteMedio}')

        # Actualizamos datos de la nueva referencia
        if nr == '1':
            articulo_nuevo.unidadCompra = articulo.unidadCompra
            articulo_nuevo.unidadVenta = articulo.unidadVenta
            articulo_nuevo.multiplo = articulo.multiplo
            articulo_nuevo.unidadMedida = articulo.unidadMedida
            articulo_nuevo.unidadStock = articulo.unidadStock
            articulo_nuevo.codigoObsoleto = articulo.codigoObsoleto
            articulo_nuevo.entradasMes = articulo.entradasMes
            articulo_nuevo.salidasMes = articulo.salidasMes
            articulo_nuevo.fechaUltMovimiento = articulo.fechaUltMovimiento
            articulo_nuevo.stockSeguridad = articulo.stockSeguridad
            articulo_nuevo.stockMinimo = articulo.stockMinimo
            articulo_nuevo.puntoPedido = articulo.puntoPedido
            articulo_nuevo.consumoMedio = articulo.consumoMedio
            articulo_nuevo.codigoContable = articulo.codigoContable
            articulo_nuevo.codAproPieza = articulo.codAproPieza
            articulo_nuevo.codigoAbc = articulo.codigoAbc
            articulo_nuevo.marca = articulo.marca
            articulo_nuevo.difinventario = articulo.difinventario
            articulo_nuevo.fechaUltimoInventario = articulo.fechaUltimoInventario
            articulo_nuevo.entradasAcumuladas = articulo.entradasAcumuladas
            articulo_nuevo.salidasAcumuladas = articulo.salidasAcumuladas
            articulo_nuevo.codigoModelo = articulo.codigoModelo
            articulo_nuevo.unidadesVendidasMes = articulo.unidadesVendidasMes
            articulo_nuevo.unidadesVendidasm1 = articulo.unidadesVendidasm1
            articulo_nuevo.unidadesVendidasm2 = articulo.unidadesVendidasm2
            articulo_nuevo.unidadesVendidasm3 = articulo.unidadesVendidasm3
            articulo_nuevo.unidadesVendidasm4 = articulo.unidadesVendidasm4
            articulo_nuevo.unidadesVendidasm5 = articulo.unidadesVendidasm5
            articulo_nuevo.unidadesVendidasm6 = articulo.unidadesVendidasm6
            articulo_nuevo.unidadesVendidasAno = articulo.unidadesVendidasAno
            articulo_nuevo.unidadesVendidasAnoAnt = articulo.unidadesVendidasAnoAnt
            articulo_nuevo.importeVtasMesPvp = articulo.importeVtasMesPvp
            articulo_nuevo.importeVtasMesCoste = articulo.importeVtasMesCoste
            articulo_nuevo.importeDtoMes = articulo.importeDtoMes
            articulo_nuevo.importeVtasAnoPvp = articulo.importeVtasAnoPvp
            articulo_nuevo.importeVtasAnoCoste = articulo.importeVtasAnoCoste
            articulo_nuevo.importeDtoAno = articulo.importeDtoAno
            articulo_nuevo.importeVtasAnoAntPvp = articulo.importeVtasAnoAntPvp
            articulo_nuevo.importeVtasAnoAntCoste = articulo.importeVtasAnoAntCoste
            articulo_nuevo.unidadesCompradasMes = articulo.unidadesCompradasMes
            articulo_nuevo.unidadesCompradasAno = articulo.unidadesCompradasAno
            articulo_nuevo.unidadesCompradasAnoAnt = articulo.unidadesCompradasAnoAnt
            articulo_nuevo.importeComprasMes = articulo.importeComprasMes
            articulo_nuevo.importeComprasAno = articulo.importeComprasAno
            articulo_nuevo.importeComprasAnoAnt = articulo.importeComprasAnoAnt
            articulo_nuevo.unidadesSalTallerMes = articulo.unidadesSalTallerMes
            articulo_nuevo.unidadesSalTallerAno = articulo.unidadesSalTallerAno
            articulo_nuevo.importeSalTallerMes = articulo.importeSalTallerMes
            articulo_nuevo.importeSalTallerAno = articulo.importeSalTallerAno
            articulo_nuevo.existencias = articulo_nuevo.existencias + articulo.existencias
            articulo_nuevo.otrasSalidasMes = articulo.otrasSalidasMes
            articulo_nuevo.otrasSalidasAno = articulo.otrasSalidasAno
            articulo_nuevo.otrasEntradasMes = articulo.otrasEntradasMes
            articulo_nuevo.otrasEntradasAno = articulo.otrasEntradasAno
            articulo_nuevo.importeOtrasSalmes = articulo.importeOtrasSalmes
            articulo_nuevo.importeOtrasSalano = articulo.importeOtrasSalano
            articulo_nuevo.importeOtrasEntmes = articulo.importeOtrasEntmes
            articulo_nuevo.importeOtrasEntano = articulo.importeOtrasEntano
            articulo_nuevo.stockinicialano = articulo.stockinicialano
            articulo_nuevo.demandaNoServidaMes = articulo.demandaNoServidaMes
            articulo_nuevo.demandaNoServidaAno = articulo.demandaNoServidaAno
            articulo_nuevo.demandaNoServidaDia = articulo.demandaNoServidaDia
            articulo_nuevo.ns = articulo.ns
            articulo_nuevo.negativo = articulo.negativo
            articulo_nuevo.imprimir = articulo.imprimir
            articulo_nuevo.unidadesVendidasm7 = articulo.unidadesVendidasm7
            articulo_nuevo.unidadesVendidasm8 = articulo.unidadesVendidasm8
            articulo_nuevo.unidadesVendidasm9 = articulo.unidadesVendidasm9
            articulo_nuevo.unidadesVendidasm10 = articulo.unidadesVendidasm10
            articulo_nuevo.unidadesVendidasm11 = articulo.unidadesVendidasm11
            articulo_nuevo.unidadesVendidasm12 = articulo.unidadesVendidasm12
            articulo_nuevo.unidadesVendidas12m = articulo.unidadesVendidas12m
            articulo_nuevo.unidadesDq = articulo.unidadesDq
            articulo_nuevo.unidadesDq1 = articulo.unidadesDq1
            articulo_nuevo.unidadesDq2 = articulo.unidadesDq2
            articulo_nuevo.unidadesDq3 = articulo.unidadesDq3
            articulo_nuevo.unidadesDq4 = articulo.unidadesDq4
            articulo_nuevo.unidadesDq5 = articulo.unidadesDq5
            articulo_nuevo.unidadesDq6 = articulo.unidadesDq6
            articulo_nuevo.unidadesDq7 = articulo.unidadesDq7
            articulo_nuevo.unidadesDq8 = articulo.unidadesDq8
            articulo_nuevo.unidadesDq9 = articulo.unidadesDq9
            articulo_nuevo.unidadesDq10 = articulo.unidadesDq10
            articulo_nuevo.unidadesDq11 = articulo.unidadesDq11
            articulo_nuevo.unidadesDq12 = articulo.unidadesDq12
            articulo_nuevo.stockMinimoP = articulo.stockMinimoP
            articulo_nuevo.stockSeguridadP = articulo.stockSeguridadP
            articulo_nuevo.puntoPedidoP = articulo.puntoPedidoP
            articulo_nuevo.consumoP = articulo.consumoP
            articulo_nuevo.familia = articulo.familia
            articulo_nuevo.fechaUltimaCompra = articulo.fechaUltimaCompra
            articulo_nuevo.unidadesUltimaCompra = articulo.unidadesUltimaCompra
            articulo_nuevo.unidadesUltimaVenta = articulo.unidadesUltimaVenta
            articulo_nuevo.bloqueoPieza = articulo.bloqueoPieza
            articulo_nuevo.fechaBloqueo = articulo.fechaBloqueo
            articulo_nuevo.unidadesDqx = articulo.unidadesDqx
            articulo_nuevo.unidadesDq1x = articulo.unidadesDq1x
            articulo_nuevo.unidadesDq2x = articulo.unidadesDq2x
            articulo_nuevo.unidadesDq3x = articulo.unidadesDq3x
            articulo_nuevo.unidadesDq4x = articulo.unidadesDq4x
            articulo_nuevo.unidadesDq5x = articulo.unidadesDq5x
            articulo_nuevo.unidadesDq6x = articulo.unidadesDq6x
            articulo_nuevo.unidadesDq7x = articulo.unidadesDq7x
            articulo_nuevo.unidadesDq8x = articulo.unidadesDq8x
        elif nr == '2':
            articulo_nuevo.existencias = articulo_nuevo.existencias + articulo.existencias
            articulo_nuevo.codAproPieza = CodigoAproPieza.objects.get(codigo='E')

        if traspasarCosteMedio:
            articulo_nuevo.precioCosteMedio = articulo.precioCosteMedio

        articulo_nuevo.save()

        # Ahora actualizamos datos de la referencia actual
        articulo.existencias = 0
        articulo.codAproPieza = CodigoAproPieza.objects.get(codigo='F')
        if nr == '1':
            articulo.entradasMes = 0
            articulo.salidasMes = 0
            articulo.entradasAcumuladas = 0
            articulo.salidasAcumuladas = 0
            articulo.unidadesVendidasMes = 0
            articulo.unidadesVendidasMes1 = 0
            articulo.unidadesVendidasMes2 = 0
            articulo.unidadesVendidasMes3 = 0
            articulo.unidadesVendidasMes4 = 0
            articulo.unidadesVendidasMes5 = 0
            articulo.unidadesVendidasMes6 = 0
            articulo.unidadesVendidasMes7 = 0
            articulo.unidadesVendidasMes8 = 0
            articulo.unidadesVendidasMes9 = 0
            articulo.unidadesVendidasMes10 = 0
            articulo.unidadesVendidasMes11 = 0
            articulo.unidadesVendidasMes12 = 0
            articulo.unidadesVendidasAno = 0
            articulo.unidadesVendidasAnoAnt = 0
            articulo.importeVtasMesPvp = 0
            articulo.importeVtasMesCoste = 0
            articulo.importeDtoMes = 0
            articulo.importeVtasAnoPvp = 0
            articulo.importeVtasAnoCoste = 0
            articulo.importeDtoAno = 0
            articulo.importeVtasAnoAntPvp = 0
            articulo.importeVtasAnoAntCoste = 0
            articulo.unidadesCompradasMes = 0
            articulo.unidadesCompradasAno = 0
            articulo.unidadesCompradasAnoAnt = 0
            articulo.importeComprasMes = 0
            articulo.importeComprasAno = 0
            articulo.importeComprasAnoAnt = 0
            articulo.unidadesSalTallerMes = 0
            articulo.unidadesSalTallerAno = 0
            articulo.importeSalTallerMes = 0
            articulo.importeSalTallerAno = 0
            articulo.otrasSalidasMes = 0
            articulo.otrasSalidasAno = 0
            articulo.otrasEntradasMes = 0
            articulo.otrasEntradasAno = 0
            articulo.importeOtrasSalmes = 0
            articulo.importeOtrasSalano = 0
            articulo.importeOtrasEntmes = 0
            articulo.importeOtrasEntano = 0
            articulo.demandaNoServidaDia = 0
            articulo.demandaNoServidaMes = 0
            articulo.demandaNoServidaAno = 0
            articulo.unidadesVendidas12m = 0
            articulo.unidadesDq = 0
            articulo.unidadesDq1 = 0
            articulo.unidadesDq2 = 0
            articulo.unidadesDq3 = 0
            articulo.unidadesDq4 = 0
            articulo.unidadesDq5 = 0
            articulo.unidadesDq6 = 0
            articulo.unidadesDq7 = 0
            articulo.unidadesDq8 = 0
            articulo.unidadesDq9 = 0
            articulo.unidadesDq10 = 0
            articulo.unidadesDq11 = 0
            articulo.unidadesDq12 = 0
            articulo.consumoP = 0
            articulo.unidadesUltimaCompra = 0
            articulo.unidadesUltimaVenta = 0
            articulo.unidadesDqx = 0
            articulo.unidadesDq1x = 0
            articulo.unidadesDq2x = 0
            articulo.unidadesDq3x = 0
            articulo.unidadesDq4x = 0
            articulo.unidadesDq5x = 0
            articulo.unidadesDq6x = 0
            articulo.unidadesDq7x = 0
            articulo.unidadesDq8x = 0

        return articulo

    def save(self, commit=True):
        # print(f'save en forms.py')
        articulo = super().save(commit=False)

        # Datos calculados
        articulo.precioCoste = articulo.tarifa - (articulo.tarifa * articulo.codigoApro.descuento / 100)
        if articulo.codigoPromo is None:
            articulo.precioPromo = 0
        else:
            articulo.precioPromo = articulo.tarifa - (articulo.tarifa * articulo.codigoPromo.descuento / 100)

        if self.es_alta:
            # Inicializamos campos en altas
            articulo.precioCosteMedio = articulo.precioCoste

        if self.referencia_nueva:
            nuevaReferencia = self.cleaned_data['nuevaReferencia']
            articulo_nuevo = Articulo.objects.get(referencia=nuevaReferencia)
            articulo = self.procesar_nueva_referencia(articulo, articulo_nuevo)

        if commit:
            articulo.save()

        return articulo


class TasaCodigoForm(ModelForm):

    class Meta:
        model = TasaCodigo
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codcontable': 'Código contable',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'descuento': 'Descuento'
        }
        widgets = {
        }


class TasaNeumaticoForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = TasaNeumatico
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'precio': 'Precio'
        }
        widgets = {
        }


class TasaForm(ModelForm):

    codigoTasa = ModelChoiceField(queryset=TasaCodigo.objects.all(), required=False, label='Seleccione Tasa')
    tasaNeumatico = ModelChoiceField(queryset=TasaNeumatico.objects.all(), required=False, label='Seleccione Tasa')

    class Meta:
        model = Tasa
        fields = ['referencia',
                  'denominacion',
                  'precio',
                  'descuento',
                  ]
        exclude = ['user_creation', 'user_updated']
        labels = {
            'referencia': 'Referencia',
            'denominacion': 'Tasa',
            'precio': 'Precio',
            'descuento': 'Descuento',
        }
        widgets = {
            'precio': NumberInput(attrs={'required': True}),
        }


class GamaForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = Gama
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'objetivo': 'Objetivo'
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class ModeloForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = Modelo
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class ConcesionarioForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = Concesionario
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'compostaje': 'Compostaje'
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class VehiculoForm(ModelForm):

    freparacion = CharField(label='Fecha Reparación', required=False)
    ireparacion = CharField(label='Importe Reparación', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cliente'].queryset = Cliente.objects.none()
        self.fields['concesionario'].queryset = Concesionario.objects.none()
        self.fields['modelo'].queryset = Concesionario.objects.none()

        if 'cliente' in self.data:
            self.fields['cliente'].queryset = Cliente.objects.all()
        elif self.instance.pk:
            self.fields['cliente'].queryset = Cliente.objects.all().filter(pk=self.instance.cliente.pk)

        if 'concesionario' in self.data:
            self.fields['concesionario'].queryset = Concesionario.objects.all()
        elif self.instance.pk:
            self.fields['concesionario'].queryset = Concesionario.objects.all().filter(pk=self.instance.concesionario.pk)

        if 'modelo' in self.data:
            self.fields['modelo'].queryset = Modelo.objects.all()
        elif self.instance.pk:
            self.fields['modelo'].queryset = Modelo.objects.all().filter(pk=self.instance.modelo.pk)

        # En Vehículos dejamos Matrícula y Bastidor modificables
        # diferenciamos add/edit
        # instance = getattr(self, 'instance', None)
        # if instance and instance.pk:
        #     # Puede que la matrícula o el vin no estén rellenos
        #     # Por tanto, solo deshabilitamos el campo si está relleno
        #     matricula = self.instance.matricula
        #     vin = self.instance.vin
        #     # print(f'Matrícula: {matricula}')
        #     # print(f'VIN: {vin}')
        #     if matricula is not None:
        #         self.fields['matricula'].disabled = True
        #     if vin is not None:
        #         self.fields['vin'].disabled = True
        # else:
        self.fields['matricula'].widget.attrs['autofocus'] = True

    class Meta:
        model = Vehiculo
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'matricula': 'Matrícula',
            'vin': 'Nº Bastidor',
            'cliente': 'Cliente',
            'marca': 'Marca',
            'gama': 'Gama',
            'modelo': 'Modelo',
            'concesionario': 'Concesionario Vendedor',
            'kilometros': 'Kilometraje',
            'fechaVenta': 'Fecha de Venta',
            'fechaFinGarantia': 'Fecha Fin Garantía',
            'notas': 'Notas',
            'norgpr': 'Nº ORG PR',
            'aorgpr': 'A.O.PR',
            'arranque': 'Arranque',
            'llave': 'Llave',
            'mando': 'Mando',
            'radio': 'Radio',
        }
        widgets = {
            'notas': Textarea(attrs={'rows': 4}),
            'marca': Select(attrs={'required': True}),
        }

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if not matricula:
            return matricula

        matricula = matricula.upper()

        # comprobamos si ya existe en la tabla otro código igual
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # print(f'id: {instance.pk}')
            vehiculos = Vehiculo.objects.filter(matricula=matricula).exclude(pk=instance.pk)
        else:
            vehiculos = Vehiculo.objects.filter(matricula=matricula)
        if vehiculos:
            raise ValidationError('Ya existe un Vehículo con esta Matrícula: %(value)s', code='coddup', params={'value': matricula})

        return matricula

    def clean_vin(self):
        vin = self.cleaned_data['vin']
        if not vin:
            return vin

        vin = vin.upper()

        # comprobamos si ya existe en la tabla otro código igual
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # print(f'id: {instance.pk}')
            vehiculos = Vehiculo.objects.filter(vin=vin).exclude(pk=instance.pk)
        else:
            vehiculos = Vehiculo.objects.filter(vin=vin)
        if vehiculos:
            raise ValidationError('Ya existe un Vehículo con este Bastidor: %(value)s', code='coddup', params={'value': vin})

        return vin

    def clean_cliente(self):
        cliente = self.cleaned_data['cliente']

        if cliente is None:
            raise ValidationError('Cliente es obligatorio')

        return cliente

    def clean_marca(self):
        marca = self.cleaned_data['marca']

        if marca is None:
            raise ValidationError('Marca es obligatoria')

        return marca

    def clean_gama(self):
        gama = self.cleaned_data['gama']

        if gama is None:
            raise ValidationError('Gama es obligatoria')

        return gama

    def clean_modelo(self):
        modelo = self.cleaned_data['modelo']

        if modelo is None:
            raise ValidationError('Modelo es obligatorio')

        return modelo

    def clean_concesionario(self):
        concesionario = self.cleaned_data['concesionario']

        if concesionario is None:
            raise ValidationError('Concesionario Vendedor es obligatorio')

        return concesionario

    def clean(self):
        cleaned_data = self.cleaned_data
        print(self.cleaned_data)

        # NORGPR es obligatorio si la marca es Citroen
        try:
            norgpr = cleaned_data['norgpr']
            marca = cleaned_data['marca']
            if norgpr is None and str(marca).find('CITROEN') != -1:
                raise ValidationError('Nº ORG PR es obligatorio para vehículos Citroen')
        except KeyError:
            # si no hay campo no continuamos con la validación
            pass

        # Los campos Matrícula y VIN no pueden estar los dos vacíos
        # Comprobamos primero si está el campo, puesto que hubo una validación anterior
        try:
            matricula = cleaned_data['matricula']
            vin = cleaned_data['vin']
            if matricula is None and vin is None:
                raise ValidationError('Matrícula o Bastidor obligatorios')
        except KeyError:
            # si no hay campo no continuamos con la validación
            pass

        return cleaned_data


class TipoOrdenReparacionForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = TipoOrdenReparacion
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


class CategoriaOperarioForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = CategoriaOperario
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


class OperarioForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = Operario
        fields = '__all__'
        # excluimos los campos de auditoría
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código Operario',
            'nombre': 'Nombre',
            'categoria': 'Categoría',
            'actividad': 'Actividad',
            'efectivoMarca': 'Efectivo Marca',
            'costeHora': 'Coste Hora',
            'costeHoraExtra': 'Coste Hora Extra',
            'potencialMes': 'Potencial Horas Mes',
            'potencialAno': 'Potencial Horas Año',
            'horaEntrada1': 'Entrada Mañana',
            'horaSalida1': 'Salida Mañana',
            'horaEntrada2': 'Entrada Tarde',
            'horaSalida2': 'Salida Tarde',
            'horaEntradaEspecial': 'Entrada Especial',
            'horaSalidaEspecial': 'Salida Especial',
            'hExtCurInvertidoMes': 'Horas Externas Mes',
            'hExtFacInvertidoMes': 'Horas Externas Mes',
            'hExtFacBaremoMes': 'Horas Externas Mes',
            'horasExtraMes': 'Horas Extra Mes',
            'hExtCurInvertidoAno': 'Horas Externas Año',
            'hExtFacInvertidoAno': 'Horas Externas Año',
            'hExtFacBaremoAno': 'Horas Externas Año',
            'horasExtraAno': 'Horas Extra Año',
            'hIntCurInvertidoMes': 'Horas Internas Mes',
            'hIntFacInvertidoMes': 'Horas Internas Mes',
            'hIntFacBaremoMes': 'Horas Internas Mes',
            'absentismoMes': 'Horas Absentismo Mes',
            'hIntCurInvertidoAno': 'Horas Internas Año',
            'hIntFacInvertidoAno': 'Horas Internas Año',
            'hIntFacBaremoAno': 'Horas Internas Año',
            'absentismoAno': 'Horas Absentismo Año',
            'hGarCurInvertidoMes': 'Horas Garantías Mes',
            'hGarFacInvertidoMes': 'Horas Garantías Mes',
            'hGarFacBaremoMes': 'Horas Garantías Mes',
            'absentismoSocialMes': 'Horas Absentismo Social Mes',
            'hGarCurInvertidoAno': 'Horas Garantías Año',
            'hGarFacInvertidoAno': 'Horas Garantías Año',
            'hGarFacBaremoAno': 'Horas Garantías Año',
            'absentismoSocialAno': 'Horas Absentismo Social Año',
            'hImpCurInvertidoMes': 'Horas Improductivas Mes',
            'hImpFacInvertidoMes': 'Horas Improductivas Mes',
            'hImpFacBaremoMes': 'Horas Improductivas Mes',
            'hImpCurInvertidoAno': 'Horas Improductivas Año',
            'hImpFacInvertidoAno': 'Horas Improductivas Año',
            'hImpFacBaremoAno': 'Horas Improductivas Año',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'nombre': TextInput(attrs={'required': True}),
        }

    def clean_codigo(self):
        operario = self.cleaned_data['codigo']
        if not operario:
            return operario

        operario = operario.upper()

        # en altas comprobamos si ya existe en la tabla otro código igual
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            pass
        else:
            operarios = Operario.objects.filter(codigo=operario)
            if operarios:
                raise ValidationError('Ya existe un Operario con este Código Operario: %(value)s', code='coddup', params={'value': operario})

        return operario

    def clean_efectivoMarca(self):
        efectivoMarca = self.cleaned_data['efectivoMarca']
        print(f'efectivoMarca: {efectivoMarca}')

        if efectivoMarca is None:
            efectivoMarca = 1
        elif efectivoMarca > 1:
            efectivoMarca = 1

        return efectivoMarca

    def clean(self):
        cleaned_data = self.cleaned_data
        print(self.cleaned_data)

        horaEntrada1 = cleaned_data['horaEntrada1']
        horaSalida1 = cleaned_data['horaSalida1']
        if (horaEntrada1 is not None) and (horaSalida1 is not None) and (horaEntrada1 > horaSalida1):
            raise ValidationError('Hora Salida Mañana debe ser mayor que la de Entrada')

        horaEntrada2 = cleaned_data['horaEntrada2']
        horaSalida2 = cleaned_data['horaSalida2']
        if (horaEntrada2 is not None) and (horaSalida2 is not None) and (horaEntrada2 > horaSalida2):
            raise ValidationError('Hora Salida Tarde debe ser mayor que la de Entrada')

        horaEntradaEspecial = cleaned_data['horaEntradaEspecial']
        horaSalidaEspecial = cleaned_data['horaSalidaEspecial']
        if (horaEntradaEspecial is not None) and (horaSalidaEspecial is not None) and (horaEntradaEspecial > horaSalidaEspecial):
            raise ValidationError('Hora Salida Especial debe ser mayor que la de Entrada')

        return cleaned_data


class SeccionInternaForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = SeccionInterna
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'cuenta': 'Cuenta'
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class CapacidadDepositoForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = CapacidadDeposito
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class AmpliacionGarantiaForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = AmpliacionGarantia
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }


class SeccionTrabajoForm(CodigoBaseForm, ModelForm):

    class Meta:
        model = SeccionTrabajo
        fields = '__all__'
        exclude = ['user_creation', 'user_updated']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }
        widgets = {
            'codigo': TextInput(attrs={'required': True}),
            'descripcion': TextInput(attrs={'required': True}),
        }