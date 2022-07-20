from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget, DateTimeWidget, DateWidget
from core.sweb.models import *
from datetime import datetime


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


class NumeracionAutomaticaResource(resources.ModelResource):

    class Meta:
        model = NumeracionAutomatica
        fields = (
            'id',
            'codigo',
            'tabla',
            'serie',
            'contador',
            'activo',
        )


class UnidadMedidaResource(resources.ModelResource):

    class Meta:
        model = UnidadMedida
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class CodigoAproPiezaResource(resources.ModelResource):

    class Meta:
        model = CodigoAproPieza
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class CodigoIvaResource(resources.ModelResource):

    class Meta:
        model = CodigoIva
        fields = (
            'id',
            'codigo',
            'descripcion',
            'porcentaje',
        )


class FamiliaPiezaResource(resources.ModelResource):

    class Meta:
        model = FamiliaPieza
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class MarcaResource(resources.ModelResource):

    class Meta:
        model = Marca
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class CodigoContableResource(resources.ModelResource):

    class Meta:
        model = CodigoContable
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class ModeloVehPiezaResource(resources.ModelResource):

    class Meta:
        model = ModeloVehPieza
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class FamiliaMarketingResource(resources.ModelResource):

    class Meta:
        model = FamiliaMarketing
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class DescuentoRecambiosResource(resources.ModelResource):

    class Meta:
        model = DescuentoRecambios
        fields = (
            'id',
            'tipo',
            'codigo',
            'codpieza',
            'descuento',
        )


class ForeignkeyDescuentoRecambiosWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return super().clean(value)

        # separamos componentes, tipo, codigo y codigo pieza
        valores = value.split('|')
        # print(valores)
        tipo = valores[0]
        codigo = valores[1]
        codpieza = valores[2].rstrip()
        # print(f'{tipo}-{codigo}-{codpieza}')
        # obtenemos el id correspondiente
        # qdtorec = DescuentoRecambios.objects.get(tipo=valores[0], codigo=valores[1], codpieza=valores[2])
        try:
            q = DescuentoRecambios.objects.get(tipo=tipo, codigo=codigo, codpieza=codpieza)
        except Exception as e:
            # En el caso de que el descuento de recambios no exista, lo creamos
            # print(f'Descuento Recanbuis inexistente: {tipo}-{codigo}-{codpieza}')
            # print(e)
            dtr = DescuentoRecambios()
            dtr.tipo = tipo
            dtr.codigo = codigo
            dtr.codpieza = codpieza
            dtr.descuento = 0
            dtr.save()
            q = DescuentoRecambios.objects.get(tipo=tipo, codigo=codigo, codpieza=codpieza)
        return super().clean(q.id)


class ForeignkeyFamiliaPiezaWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if value is None:
            return super().clean(value)

        try:
            q = FamiliaPieza.objects.get(codigo=value)
        except Exception as e:
            # En el caso de que no exista, lo creamos
            familia = FamiliaPieza()
            familia.codigo = value
            familia.descripcion = '...'
            familia.save()
            q = FamiliaPieza.objects.get(codigo=value)
        return super().clean(q.id)


class ForeignkeyFamiliaMarketingWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if value is None:
            return super().clean(value)

        try:
            q = FamiliaMarketing.objects.get(codigo=value)
        except Exception as e:
            # En el caso de que no exista, lo creamos
            familiamk = FamiliaMarketing()
            familiamk.codigo = value
            familiamk.descripcion = '...'
            familiamk.save()
            q = FamiliaMarketing.objects.get(codigo=value)
        return super().clean(q.id)


class PrecioTarifaResource(resources.ModelResource):

    codigoDescuento = fields.Field(attribute='codigoDescuento', column_name='codigoDescuento', widget=ForeignkeyDescuentoRecambiosWidget(DescuentoRecambios, 'id'))
    codUrgencia = fields.Field(attribute='codUrgencia', column_name='codUrgencia', widget=ForeignkeyDescuentoRecambiosWidget(DescuentoRecambios, 'id'))
    familia = fields.Field(attribute='familia', column_name='familia', widget=ForeignkeyFamiliaPiezaWidget(FamiliaPieza, 'id'))
    familiaMarketing = fields.Field(attribute='familiaMarketing', column_name='familiaMarketing', widget=ForeignkeyFamiliaMarketingWidget(FamiliaMarketing, 'id'))

    class Meta:
        model = PrecioTarifa
        fields = (
            'id',
            'referencia',
            'denominacion',
            'variacion',
            'pvp',
            'f1',
            'f2',
            'f3',
            'f4',
            'f5',
            'f6',
            'f8',
            'f9',
            'codigoDescuento',
            'multiplo',
            'modeloVehiculo',
            'penetracion',
            'nuevaReferencia',
            'nuevaRefer2',
            'pvp1',
            'familiaMarketing',
            'funcion',
            'familia',
            'panier',
            'codUrgencia',
        )


class ArticuloResource(resources.ModelResource):

    proveedor = fields.Field(attribute='proveedor', column_name='proveedor', widget=ForeignKeyWidget(Cliente, field='codigo'))
    unidadMedida = fields.Field(attribute='unidadMedida', column_name='unidadMedida', widget=ForeignKeyWidget(UnidadMedida, field='codigo'))
    codAproPieza = fields.Field(attribute='codAproPieza', column_name='codAproPieza', widget=ForeignKeyWidget(CodigoAproPieza, field='codigo'))
    ivaPieza = fields.Field(attribute='ivaPieza', column_name='ivaPieza', widget=ForeignKeyWidget(CodigoIva, field='codigo'))
    familia = fields.Field(attribute='familia', column_name='familia', widget=ForeignKeyWidget(FamiliaPieza, field='codigo'))
    marca = fields.Field(attribute='marca', column_name='marca', widget=ForeignKeyWidget(Marca, field='codigo'))
    codigoContable = fields.Field(attribute='codigoContable', column_name='codigoContable', widget=ForeignKeyWidget(CodigoContable, field='codigo'))
    codigoModelo = fields.Field(attribute='codigoModelo', column_name='codigoModelo', widget=ForeignKeyWidget(ModeloVehPieza, field='codigo'))
    familiaMarketing = fields.Field(attribute='familiaMarketing', column_name='familiaMarketing', widget=ForeignkeyFamiliaMarketingWidget(FamiliaMarketing, 'id'))
    codigoPromo = fields.Field(attribute='codigoPromo', column_name='codigoPromo', widget=ForeignkeyDescuentoRecambiosWidget(DescuentoRecambios, 'id'))
    codigoApro = fields.Field(attribute='codigoApro', column_name='codigoApro', widget=ForeignkeyDescuentoRecambiosWidget(DescuentoRecambios, 'id'))
    codigoUrgte = fields.Field(attribute='codigoUrgte', column_name='codigoUrgte', widget=ForeignkeyDescuentoRecambiosWidget(DescuentoRecambios, 'id'))

    fechaAlta = fields.Field(attribute='fechaAlta', column_name='fechaAlta', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaUltMovimiento = fields.Field(attribute='fechaUltMovimiento', column_name='fechaUltMovimiento', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaUltimoInventario = fields.Field(attribute='fechaUltimoInventario', column_name='fechaUltimoInventario', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaUltimaVenta = fields.Field(attribute='fechaUltimaVenta', column_name='fechaUltimaVenta', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaUltimaCompra = fields.Field(attribute='fechaUltimaCompra', column_name='fechaUltimaCompra', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaBloqueo = fields.Field(attribute='fechaBloqueo', column_name='fechaBloqueo', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))

    class Meta:
        model = Articulo
        fields = (
            'id',
            'referencia',
            'descripcion',
            'tarifa',
            'precioCosteMedio',
            'precioInicial',
            'precioCoste',
            'codigoPromo',
            'precioPromo',
            'existencias',
            'codigoApro',
            'peidosPendientes',
            'reserva',
            'unidadCompra',
            'unidadVenta',
            'multiplo',
            'unidadMedida',
            'unidadStock',
            'fechaAlta',
            'codigoObsoleto',
            'nuevaReferencia',
            'entradasMes',
            'salidasMes',
            'fechaUltMovimiento',
            'ubicacion',
            'ivaPieza',
            'codAlerta',
            'stockSeguridad',
            'stockMinimo',
            'puntoPedido',
            'consumoMedio',
            'codigoContable',
            'codAproPieza',
            'codigoAbc',
            'marca',
            'codigoCompetencia',
            'funcion',
            'difinventario',
            'fechaUltimoInventario',
            'fechaUltimaVenta',
            'entradasAcumuladas',
            'salidasAcumuladas',
            'codigoModelo',
            'proveedor',
            'unidadesVendidasMes',
            'unidadesVendidasm1',
            'unidadesVendidasm2',
            'unidadesVendidasm3',
            'unidadesVendidasm4',
            'unidadesVendidasm5',
            'unidadesVendidasm6',
            'unidadesVendidasAno',
            'unidadesVendidasAnoAnt',
            'importeVtasMesPvp',
            'importeVtasMesCoste',
            'importeDtoMes',
            'importeVtasAnoPvp',
            'importeVtasAnoCoste',
            'importeDtoAno',
            'importeVtasAnoAntPvp',
            'importeVtasAnoAntCoste',
            'unidadesCompradasMes',
            'unidadesCompradasAno',
            'unidadesCompradasAnoAnt',
            'importeComprasMes',
            'importeComprasAno',
            'importeComprasAnoAnt',
            'unidadesSalTallerMes',
            'unidadesSalTallerAno',
            'importeSalTallerMes',
            'importeSalTallerAno',
            'otrasSalidasMes',
            'otrasSalidasAno',
            'otrasEntradasMes',
            'otrasEntradasAno',
            'importeOtrasSalmes',
            'importeOtrasSalano',
            'importeOtrasEntmes',
            'importeOtrasEntano',
            'stockinicialano',
            'demandaNoServidaMes',
            'demandaNoServidaAno',
            'demandaNoServidaDia',
            'ns',
            'negativo',
            'imprimir',
            'bloqueo',
            'unidadesVendidasm7',
            'unidadesVendidasm8',
            'unidadesVendidasm9',
            'unidadesVendidasm10',
            'unidadesVendidasm11',
            'unidadesVendidasm12',
            'unidadesVendidas12m',
            'unidadesDq',
            'unidadesDq1',
            'unidadesDq2',
            'unidadesDq3',
            'unidadesDq4',
            'unidadesDq5',
            'unidadesDq6',
            'unidadesDq7',
            'unidadesDq8',
            'unidadesDq9',
            'unidadesDq10',
            'unidadesDq11',
            'unidadesDq12',
            'stockMinimoP',
            'stockSeguridadP',
            'puntoPedidoP',
            'consumoP',
            'familia',
            'fechaUltimaCompra',
            'unidadesUltimaCompra',
            'unidadesUltimaVenta',
            'bloqueoPieza',
            'fechaBloqueo',
            'unidadesDqx',
            'unidadesDq1x',
            'unidadesDq2x',
            'unidadesDq3x',
            'unidadesDq4x',
            'unidadesDq5x',
            'unidadesDq6x',
            'unidadesDq7x',
            'unidadesDq8x',
            'observaciones',
            'panier',
            'familiaMarketing',
            'codigoUrgte',
        )


# class TasaChoicesWidget(widgets.Widget):
#
#     def clean(self, value, row=None, *args, **kwargs):
#         if value is None:
#             return super().clean(value)
#         print(value)
#         if value.startswith('APORTA'):
#             codigo = '00'
#         elif value.startswith('A.A.'):
#             codigo = '01'
#         else:
#             codigo = None
#         return super().clean(codigo)


class TasaResource(resources.ModelResource):

    referencia = fields.Field(attribute='referencia', column_name='referencia', widget=ForeignKeyWidget(Articulo, field='referencia'))

    class Meta:
        model = Tasa
        fields = (
            'id',
            'referencia',
            'denominacion',
            'precio',
            'descuento',
        )


class TasaNeumaticoResource(resources.ModelResource):

    class Meta:
        model = TasaNeumatico
        fields = (
            'id',
            'codigo',
            'descripcion',
            'precio',
        )


class GamaResource(resources.ModelResource):

    class Meta:
        model = Gama
        fields = (
            'id',
            'codigo',
            'descripcion',
            'objetivo',
        )


class ModeloResource(resources.ModelResource):

    class Meta:
        model = Modelo
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class ConcesionarioResource(resources.ModelResource):

    class Meta:
        model = Concesionario
        fields = (
            'id',
            'codigo',
            'descripcion',
            'compostaje',
        )


class ForeignkeyModeloWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        defecto = '000000'
        if value is None:
            return super().clean(value)

        try:
            q = Modelo.objects.get(codigo=value)
        except Exception as e:
            # En el caso de que no exista, utilizamos valor por defecto
            q = Modelo.objects.get(codigo=defecto)
        return super().clean(q.id)


class ForeignkeyGamaWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if value is None:
            return super().clean(value)

        try:
            q = Gama.objects.get(codigo=value)
        except Exception as e:
            # En el caso de que no exista, lo creamos
            gama = Gama()
            gama.codigo = value
            gama.descripcion = '...'
            gama.save()
            q = Gama.objects.get(codigo=value)
        return super().clean(q.id)


class ForeignkeyMarcaWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if value is None:
            return super().clean(value)

        try:
            q = Marca.objects.get(codigo=value)
        except Exception as e:
            # En el caso de que no exista, lo creamos
            marca = Marca()
            marca.codigo = value
            marca.descripcion = '...'
            marca.save()
            q = Marca.objects.get(codigo=value)
        return super().clean(q.id)


class VehiculoResource(resources.ModelResource):
    cliente = fields.Field(attribute='cliente', column_name='cliente', widget=ForeignKeyWidget(Cliente, field='codigo'))
    marca = fields.Field(attribute='marca', column_name='marca', widget=ForeignkeyMarcaWidget(Marca, 'id'))
    gama = fields.Field(attribute='gama', column_name='gama', widget=ForeignkeyGamaWidget(Gama, 'id'))
    modelo = fields.Field(attribute='modelo', column_name='modelo', widget=ForeignkeyModeloWidget(Modelo, 'id'))
    concesionario = fields.Field(attribute='concesionario', column_name='concesionario', widget=ForeignKeyWidget(Concesionario, field='codigo'))
    fechaVenta = fields.Field(attribute='fechaVenta', column_name='fechaVenta', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaFinGarantia = fields.Field(attribute='fechaFinGarantia', column_name='fechaFinGarantia', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaItv = fields.Field(attribute='fechaItv', column_name='fechaItv', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))
    fechaNeumatico = fields.Field(attribute='fechaNeumatico', column_name='fechaNeumatico', widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%SZ'))

    class Meta:
        model = Vehiculo
        fields = (
            'id',
            'matricula',
            'vin',
            'cliente',
            'marca',
            'gama',
            'modelo',
            'concesionario',
            'kilometros',
            'fechaVenta',
            'fechaFinGarantia',
            'notas',
            'norgpr',
            'aorgpr',
            'arranque',
            'llave',
            'mando',
            'radio',
            'fechaItv',
            'neumatico',
            'fechaNeumatico',
            'opPreventiva',
        )


class TipoOrdenReparacionResource(resources.ModelResource):

    class Meta:
        model = TipoOrdenReparacion
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class CategoriaOperarioResource(resources.ModelResource):

    class Meta:
        model = CategoriaOperario
        fields = (
            'id',
            'codigo',
            'descripcion',
        )


class OperarioResource(resources.ModelResource):

    categoria = fields.Field(attribute='categoria', column_name='categoria', widget=ForeignKeyWidget(CategoriaOperario, field='codigo'))

    class Meta:
        model = Operario
        fields = (
            'id',
            'codigo',
            'nombre',
            'categoria',
            'actividad',
            'costeHora',
            'costeHoraExtra',
            'potencialDia',
            'potencialMes',
            'potencialAno',
            'efectivoMarca',
            'absentismoDia',
            'absentismoMes',
            'absentismoAno',
            'absentismoSocialDia',
            'absentismoSocialMes',
            'absentismoSocialAno',
            'bonoDia',
            'bonoMes',
            'bonoAno',
            'horasExtraDia',
            'horasExtraMes',
            'horasExtraAno',
            'hExtCurInvertidoMes',
            'hExtCurInvertidoAno',
            'hExtFacInvertidoMes',
            'hExtFacBaremoMes',
            'hExtFacInvertidoDia',
            'hExtFacBaremoDia',
            'hExtFacInvertidoAno',
            'hExtFacBaremoAno',
            'hIntCurInvertidoMes',
            'hIntCurInvertidoAno',
            'hIntFacInvertidoMes',
            'hIntFacBaremoMes',
            'hIntFacInvertidoDia',
            'hIntFacBaremoDia',
            'hIntFacInvertidoAno',
            'hGarCurInvertidoMes',
            'hGarCurInvertidoAno',
            'hGarFacInvertidoMes',
            'hGarFacBaremoMes',
            'hGarFacInvertidoDia',
            'hGarFacBaremoDia',
            'hGarFacInvertidoAno',
            'hGarFacBaremoAno',
            'hImpCurInvertidoMes',
            'hImpFacInvertidoMes',
            'hImpFacInvertidoAno',
            'horaEntrada1',
            'horaSalida1',
            'horaEntrada2',
            'horaSalida2',
            'horaEntradaEspecial',
            'horaSalidaEspecial',
            'trabajoEnCurso'
        )
