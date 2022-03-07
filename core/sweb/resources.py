from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget, DateTimeWidget, DateWidget
from core.sweb.models import *


class DescuentoMOResource(resources.ModelResource):

    class Meta:
        model = DescuentoMO
        fields = (
            'id',
            'codigo',
            'descripcion',
            'descuento',
        )


class BancoResource(resources.ModelResource):

    class Meta:
        model = Banco
        fields = (
            'id',
            'codigo',
            'sucursal',
            'cuenta',
            'dgc',
            'dgc2',
            'codbcoe',
            'razonsocial',
            'tipovia',
            'nomvia',
            'numvia',
            'codpostal',
            'municipio',
            'provincia',
            'telefono',
            'telex',
            'prefijo',
            'contacto',
            'extension',
            'telperso',
        )


class FormaDePagoResource(resources.ModelResource):

    class Meta:
        model = FormaDePago
        fields = (
            'id',
            'codigo',
            'descripcion',
            'recibos',
            'diasvto',
        )


class TipoClienteRecambiosResource(resources.ModelResource):

    class Meta:
        model = TipoClienteRecambios
        fields = (
            'id',
            'codigo',
            'descripcion',
            'datocontable',
        )


class ForeignkeyBancoWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return super().clean(value)

        # separamos codigo y sucursal
        valores = value.split('|')

        # obtenemos el id correspondiente
        qbancos = Banco.objects.get(codigo=valores[0], sucursal=valores[1])
        return super().clean(qbancos.id)


class ClienteResource(resources.ModelResource):

    tipoCliente = fields.Field(attribute='tipoCliente', column_name='tipoCliente', widget=ForeignKeyWidget(TipoClienteRecambios, field='codigo'))
    formaDePago = fields.Field(attribute='formaDePago', column_name='formaDePago', widget=ForeignKeyWidget(FormaDePago, field='codigo'))
    dtomo = fields.Field(attribute='dtomo', column_name='dtomo', widget=ForeignKeyWidget(DescuentoMO, field='codigo'))
    fechaUltimaFactura = fields.Field(attribute='fechaUltimaFactura', column_name='fechaUltimaFactura', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaUltimoMovimiento = fields.Field(attribute='fechaUltimoMovimiento', column_name='fechaUltimoMovimiento', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaNacimiento = fields.Field(attribute='fechaNacimiento', column_name='fechaNacimiento', widget=DateWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    banco = fields.Field(attribute='banco', column_name='banco', widget=ForeignkeyBancoWidget(Banco, 'id'))

    class Meta:
        model = Cliente
        fields = (
            'id',
            'codigo',
            'razonSocial',
            'tipoCliente',
            'direccion',
            'codpostal',
            'poblacion',
            'provincia',
            'cif',
            'telefono',
            'fax',
            'tlfmovil',
            'banco',
            'cuenta',
            'formaDePago',
            'diaPagoDesde',
            'diaPagoHasta',
            'dtopieza',
            'dtomo',
            'dtoEpecial',
            'fechaUltimaFactura',
            'creditoDisponible',
            'creditoDispuesto',
            'bloquearCredito',
            'importeRecambiosMes',
            'importeRecambiosAno',
            'importeRecambiosAnoAnterior',
            'costeRecambiosMes',
            'costeRecambiosAno',
            'costeRecambiosAnoAnterior',
            'importeTallerMes',
            'importeTallerAno',
            'importeTallerAnoAnterior',
            'costeTallerMes',
            'costeTallerAno',
            'costeTallerAnoAnterior',
            'fechaUltimoMovimiento',
            'comprasMes',
            'comprasAno',
            'comprasAnoAnterior',
            'emitirRecibos',
            'aplicarIva',
            'importeRecambiosTallerMes',
            'importeRecambiosTallerAno',
            'importeRecambiosTallerAnoAnterior',
            'costeRecambiosTallerMes',
            'costeRecambiosTallerAno',
            'costeRecambiosTallerAnoAnterior',
            'listarnetodto',
            'exentoMail',
            'pasaporte',
            'notas',
            'precioMo',
            'fechaNacimiento',
            'ivaEpecial',
            'email',
            'enviarSms',
            'ocultarCuenta',
            'iban',
            'dc',
            'nombre',
            'apellido1',
            'apellido2',
            'lopd',
            'lopd1',
            'lopd2',
            'lopd3',
            'lopdfirma',
        )

        clean_model_instances = True

