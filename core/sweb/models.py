from django.db import models
from core.sweb.utils import digitos_control, validar_porcentaje
from core.models import BaseModel
from core.sweb.mixins import ModelMixin
from django.db.models import Q


class Banco(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=4, verbose_name='código banco', db_column='ban_codcsp', null=False,
                              blank=False)
    sucursal = models.CharField(max_length=4, verbose_name='sucursal', db_column='ban_sucursal', null=False,
                                blank=False)
    cuenta = models.CharField(max_length=15, verbose_name='número cuenta', db_column='ban_cuenta', null=True)
    dgc = models.CharField(max_length=1, verbose_name='dígito control', db_column='ban_dgc', null=True)
    dgc2 = models.CharField(max_length=1, verbose_name='dígito control 2', db_column='ban_dgc2', null=True)
    codbcoe = models.CharField(max_length=8, db_column='ban_codbcoe', null=True)
    razonsocial = models.CharField(max_length=100, db_column='ban_rsocial', verbose_name='razón social', null=False,
                                   blank=False)
    tipovia = models.CharField(max_length=2, verbose_name='tipo vía', db_column='ban_tipovia', null=False, blank=False)
    nomvia = models.CharField(max_length=100, verbose_name='nombre vía', db_column='ban_nomvia', null=False,
                              blank=False)
    numvia = models.CharField(max_length=3, verbose_name='número vía', db_column='ban_numvia', null=False, blank=False)
    codpostal = models.CharField(max_length=5, verbose_name='código postal', db_column='ban_cpostal', null=False,
                                 blank=False)
    municipio = models.CharField(max_length=100, verbose_name='municipio', db_column='ban_mncipio', null=False,
                                 blank=False)
    provincia = models.CharField(max_length=100, verbose_name='provincia', db_column='ban_provin', null=False,
                                 blank=False)
    telex = models.CharField(max_length=25, verbose_name='telex', db_column='ban_telex', null=True, blank=True)
    prefijo = models.IntegerField(db_column='ban_preftel', verbose_name='prefijo teléfono', null=True, blank=True)
    telefono = models.IntegerField(db_column='ban_telef', verbose_name='teléfono', null=True, blank=True)
    telperso = models.IntegerField(db_column='ban_telper', verbose_name='teléfono personal', null=True, blank=True)
    extension = models.IntegerField(db_column='ban_extelf', verbose_name='extensión', null=True, blank=True)
    contacto = models.CharField(max_length=100, verbose_name='contacto', db_column='ban_contac', null=True, blank=True)

    def __str__(self):
        # return self.codigo + self.sucursal
        return f'| {self.codigo} | {self.sucursal} | {self.razonsocial}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'sucursal': self.sucursal,
            'razonsocial': self.razonsocial,
            'telefono': self.telefono,
        }
        return item

    # para la paginación por servidor utilizamos este método para los filtros
    def to_search(self, value):
        return self.objects.filter(Q(codigo__icontains=value) |
                                   Q(sucursal__icontains=value) |
                                   Q(razonsocial__icontains=value) |
                                   Q(telefono__icontains=value)
                                   )

    class Meta:
        db_table = 'sirtbban'
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        # constraint para que la combinación de código y sucursal no pueda repetirse
        unique_together = ['codigo', 'sucursal']
        ordering = ['codigo', 'sucursal']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.pk:
            # Inicializamos campos
            self.cuenta = '000000000000000'
            self.dgc = digitos_control('00' + self.codigo + self.sucursal)
            self.dgc2 = '0'
        super(Banco, self).save()


class DescuentoMO(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=1, verbose_name='Código', db_column='dmo_codigo', unique=True,
                              null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='dmo_descrip',
                                   null=False, blank=False)
    descuento = models.DecimalField(verbose_name='Descuento', db_column='dmo_descuento', default=0.0, max_digits=5,
                                    decimal_places=2, null=False, blank=False, validators=[validar_porcentaje])

    def __str__(self):
        return f'{self.codigo} - {self.descripcion} - {self.descuento}%'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'descuento': self.descuento,
        }
        return item

    class Meta:
        db_table = 'sirtbdmo'
        verbose_name = 'Descuento MO'
        verbose_name_plural = 'Descuentos MO'
        ordering = ['codigo']


class FormaDePago(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='fpg_codigo', unique=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='fpg_descrip',
                                   null=False, blank=False)
    recibos = models.IntegerField(verbose_name='Recibos', db_column='fpg_recibos', default=0, null=False, blank=False)
    diasvto = models.IntegerField(verbose_name='Días vencimiento factura', db_column='fpg_diasvto', default=0,
                                  null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'recibos': self.recibos,
            'diasvto': self.diasvto,
        }
        return item

    class Meta:
        db_table = 'sirtbfpg'
        verbose_name = 'Forma de Pago'
        verbose_name_plural = 'Formas de Pago'
        ordering = ['codigo']


class TipoClienteRecambios(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='tcr_codigo', unique=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='tcr_descrip',
                                   null=False, blank=False)
    datocontable = models.CharField(max_length=1, verbose_name='Dato contable', db_column='tcr_datocon',
                                    null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'datocontable': self.datocontable,
        }
        return item

    class Meta:
        db_table = 'sirtbtcr'
        verbose_name = 'Tipo de Cliente Recambios'
        verbose_name_plural = 'Tipos de Cliente Recambios'
        ordering = ['codigo']


class Cliente(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=6, verbose_name='código cliente', db_column='cli_codigo', unique=True,
                              null=False, blank=False)
    razonSocial = models.CharField(max_length=100, verbose_name='razón social', db_column='cli_rsocial', null=True, blank=True)
    nombre = models.CharField(max_length=100, verbose_name='nombre', db_column='cli_nombre', null=True, blank=True)
    apellido1 = models.CharField(max_length=100, verbose_name='apellido 1', db_column='cli_ape1', null=True, blank=True)
    apellido2 = models.CharField(max_length=100, verbose_name='apellido 2', db_column='cli_ape2', null=True, blank=True)
    tipoCliente = models.ForeignKey(TipoClienteRecambios, on_delete=models.PROTECT, null=False, blank=False,
                                    db_column='cli_tipcli', verbose_name='tipo cliente')
    direccion = models.CharField(max_length=100, verbose_name='direccion', db_column='cli_direccion', null=True,
                                 blank=True)
    codpostal = models.CharField(max_length=5, verbose_name='código postal', db_column='cli_cpostal', null=True,
                                 blank=True)
    poblacion = models.CharField(max_length=100, verbose_name='poblacion', db_column='cli_poblacion', null=True,
                                 blank=True)
    provincia = models.CharField(max_length=100, verbose_name='provincia', db_column='cli_provincia', null=True,
                                 blank=True)
    cif = models.CharField(max_length=15, verbose_name='CIF', db_column='cli_cif', null=True, blank=True)
    telefono = models.CharField(max_length=15, verbose_name='telefono', db_column='cli_telefono', null=True, blank=True)
    fax = models.CharField(max_length=15, verbose_name='fax', db_column='cli_fax', null=True, blank=True)
    tlfmovil = models.CharField(max_length=15, verbose_name='teléfono móvil', db_column='cli_tlfmovil', null=True, blank=True)
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT, null=True, blank=True, db_column='cli_banco',
                              verbose_name='banco')
    cuenta = models.CharField(max_length=15, verbose_name='cuenta', db_column='cli_cuenta', null=True, blank=True)
    formaDePago = models.ForeignKey(FormaDePago, on_delete=models.PROTECT, null=False, blank=False,
                                    db_column='cli_fpago', verbose_name='forma de pago')
    diaPagoDesde = models.IntegerField(verbose_name='día pago desde', db_column='cli_diapagod', null=True, blank=True)
    diaPagoHasta = models.IntegerField(verbose_name='día pago hasta', db_column='cli_diapagoh', null=True, blank=True)
    dtopieza = models.CharField(max_length=1, verbose_name='descuento pieza', db_column='cli_dtopieza', null=True,
                                blank=True)
    dtomo = models.ForeignKey(DescuentoMO, on_delete=models.PROTECT, null=False, blank=False, db_column='cli_dtomo',
                              verbose_name='descuento MO')
    dtoEpecial = models.DecimalField(verbose_name='descuento especial', db_column='cli_dtoesp', max_digits=5,
                                     decimal_places=2, null=True, blank=True, validators=[validar_porcentaje])
    fechaUltimaFactura = models.DateTimeField(verbose_name='fecha última factura', db_column='cli_fultfac', null=True,
                                              blank=True)
    creditoDisponible = models.DecimalField(verbose_name='crédito disponible', db_column='cli_credispo', max_digits=9,
                                            decimal_places=2, null=True, blank=True)
    creditoDispuesto = models.DecimalField(verbose_name='crédito dispuesto', db_column='cli_credispu', max_digits=9,
                                           decimal_places=2, null=True, blank=True)
    bloquearCredito = models.BooleanField(verbose_name='bloquear crédito', db_column='cli_bloqcred', default=False,
                                          null=False, blank=False)
    importeRecambiosMes = models.DecimalField(verbose_name='importe recambios mes', db_column='cli_imprecmes',
                                              max_digits=9, decimal_places=2, null=True, blank=True)
    importeRecambiosAno = models.DecimalField(verbose_name='importe recambios año', db_column='cli_imprecano',
                                              max_digits=9, decimal_places=2, null=True, blank=True)
    importeRecambiosAnoAnterior = models.DecimalField(verbose_name='importe recambios año anterior', max_digits=9,
                                                      decimal_places=2, db_column='cli_imprecanoant', null=True,
                                                      blank=True)
    costeRecambiosMes = models.DecimalField(verbose_name='coste recambios mes', db_column='cli_cosrecmes', max_digits=9,
                                            decimal_places=2, null=True, blank=True)
    costeRecambiosAno = models.DecimalField(verbose_name='coste recambios año', db_column='cli_cosrecano', max_digits=9,
                                            decimal_places=2, null=True, blank=True)
    costeRecambiosAnoAnterior = models.DecimalField(verbose_name='coste recambios año anterior', max_digits=9,
                                                    decimal_places=2, db_column='cli_cosrecanoant', null=True,
                                                    blank=True)
    importeTallerMes = models.DecimalField(verbose_name='importe taller mes', db_column='cli_imptalmes', max_digits=9,
                                           decimal_places=2, null=True, blank=True)
    importeTallerAno = models.DecimalField(verbose_name='importe taller año', db_column='cli_imptalano', max_digits=9,
                                           decimal_places=2, null=True, blank=True)
    importeTallerAnoAnterior = models.DecimalField(verbose_name='importe taller año anterior', max_digits=9,
                                                   decimal_places=2, db_column='cli_imptalanoant', null=True,
                                                   blank=True)
    costeTallerMes = models.DecimalField(verbose_name='coste taller mes', db_column='cli_costalmes', max_digits=9,
                                         decimal_places=2, null=True, blank=True)
    costeTallerAno = models.DecimalField(verbose_name='coste taller año', db_column='cli_costalano', max_digits=9,
                                         decimal_places=2, null=True, blank=True)
    costeTallerAnoAnterior = models.DecimalField(verbose_name='coste taller año anterior', max_digits=9,
                                                 decimal_places=2, db_column='cli_costalanoant', null=True, blank=True)
    fechaUltimoMovimiento = models.DateTimeField(verbose_name='fecha último movimiento', db_column='cli_fultmov',
                                                 null=True, blank=True)
    comprasMes = models.DecimalField(verbose_name='compras mes', db_column='cli_comprasmes', max_digits=9,
                                     decimal_places=2, null=True, blank=True)
    comprasAno = models.DecimalField(verbose_name='compras año', db_column='cli_comprasano', max_digits=9,
                                     decimal_places=2, null=True, blank=True)
    comprasAnoAnterior = models.DecimalField(verbose_name='compras año anterior', max_digits=9, decimal_places=2,
                                             db_column='cli_comprasanoant', null=True, blank=True)
    emitirRecibos = models.BooleanField(verbose_name='emitir recibos', db_column='cli_emirec', default=False,
                                        null=False, blank=False)
    aplicarIva = models.BooleanField(verbose_name='aplicar IVA', db_column='cli_apliva', default=False, null=False,
                                     blank=False)
    importeRecambiosTallerMes = models.DecimalField(verbose_name='importe recambios taller mes', max_digits=9,
                                                    decimal_places=2, db_column='cli_imprectalmes', null=True,
                                                    blank=True)
    importeRecambiosTallerAno = models.DecimalField(verbose_name='importe recambios taller año', max_digits=9,
                                                    decimal_places=2, db_column='cli_imprectalano', null=True,
                                                    blank=True)
    importeRecambiosTallerAnoAnterior = models.DecimalField(verbose_name='importe recambios taller año anterior',
                                                            max_digits=9, decimal_places=2,
                                                            db_column='cli_imprectalanoant', null=True, blank=True)
    costeRecambiosTallerMes = models.DecimalField(verbose_name='coste recambios taller mes', max_digits=9,
                                                  decimal_places=2, db_column='cli_cosrectalmes', null=True, blank=True)
    costeRecambiosTallerAno = models.DecimalField(verbose_name='coste recambios taller año', max_digits=9,
                                                  decimal_places=2, db_column='cli_cosrectalano', null=True, blank=True)
    costeRecambiosTallerAnoAnterior = models.DecimalField(verbose_name='coste recambios taller año anterior',
                                                          max_digits=9, decimal_places=2,
                                                          db_column='cli_cosrectalanoant', null=True, blank=True)
    listarnetodto = models.BooleanField(verbose_name='listar neto descuento', db_column='cli_lstnetdto', default=False, null=False, blank=False)
    exentoMail = models.BooleanField(verbose_name='exento mail', db_column='cli_exentomail', default=False, null=False,
                                     blank=False)
    pasaporte = models.CharField(max_length=15, verbose_name='pasaporte', db_column='cli_pasaporte', null=True,
                                 blank=True)
    notas = models.TextField(verbose_name='notas', db_column='cli_notas', null=True, blank=True)
    precioMo = models.DecimalField(verbose_name='precio MO', db_column='cli_preciomo', max_digits=9, decimal_places=2,
                                   null=True, blank=True)
    fechaNacimiento = models.DateField(verbose_name='fecha nacimiento', db_column='cli_fenaci', null=True, blank=True)
    ivaEpecial = models.DecimalField(verbose_name='iva especial', db_column='cli_ivaesp', max_digits=5,
                                     decimal_places=2, null=True, blank=True, validators=[validar_porcentaje])
    email = models.CharField(max_length=100, verbose_name='email', db_column='cli_email', null=True, blank=True)
    SMS_CHOICES = [
        ('0', 'No Envío'),
        ('1', 'Envío Cerrar OR'),
        ('2', 'Envío Satisfacción'),
        ('3', 'Envío Ambos'),
        ('4', 'Envío Sin Importe'),
    ]
    enviarSms = models.CharField(max_length=1, choices=SMS_CHOICES, default='0', verbose_name='enviar sms',
                                 db_column='cli_envsms', null=False, blank=False)
    ocultarCuenta = models.BooleanField(verbose_name='ocultar cuenta', db_column='cli_ocucta', default=False,
                                        null=False, blank=False)
    iban = models.CharField(max_length=4, verbose_name='iban', db_column='cli_iban', null=True, blank=True)
    dc = models.CharField(max_length=2, verbose_name='dígito control', db_column='cli_dc', null=True, blank=True)
    lopd = models.BooleanField(verbose_name='LOPD', db_column='cli_lopd', default=False, null=False, blank=False)
    lopd1 = models.BooleanField(verbose_name='LOPD 1', db_column='cli_lopd1', default=False, null=False, blank=False)
    lopd2 = models.BooleanField(verbose_name='LOPD 2', db_column='cli_lopd2', default=False, null=False, blank=False)
    lopd3 = models.BooleanField(verbose_name='LOPD 3', db_column='cli_lopd3', default=False, null=False, blank=False)
    lopdfirma = models.BooleanField(verbose_name='LOPD firma', db_column='cli_lopdf', default=False, null=False, blank=False)

    def __str__(self):
        # if self.nombre is not None:
        #     return f'{self.codigo} - {self.nombre} - {self.apellido1} - {self.apellido2}'
        # else:
            return f'{self.codigo} - {self.razonSocial}'

    # para la paginación por servidor utilizamos este método para los filtros
    def to_search(self, value):
        return self.objects.filter(Q(codigo__icontains=value) |
                                   Q(razonSocial__icontains=value) |
                                   Q(cif__icontains=value) |
                                   Q(telefono__icontains=value) |
                                   Q(tlfmovil__icontains=value) |
                                   Q(poblacion__icontains=value) |
                                   Q(provincia__icontains=value)
                                   )

    # para la paginación por select2
    def to_search_select(self, value):
        return self.objects.filter(Q(codigo__icontains=value) |
                                   Q(razonSocial__icontains=value)
                                   )

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'razonSocial': self.razonSocial,
            'cif': self.cif,
            'telefono': self.telefono,
            'tlfmovil': self.tlfmovil,
            'poblacion': self.poblacion,
            'provincia': self.provincia,
        }
        return item

    def to_list_select(self):
        item = {
            'id': self.id,
            'text': f'{self.codigo} - {self.razonSocial}',
        }
        return item

    def to_list_select_veh(self):
        stelefono = ''
        if self.telefono is not None:
            stelefono = ' - Teléfono: ' + self.telefono

        item = {
            'id': self.id,
            'text': f'{self.codigo} - {self.razonSocial}{stelefono}',
        }
        return item

    class Meta:
        db_table = 'sirtbcli'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['codigo']


class NumeracionAutomatica(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='nau_codigo', unique=True,
                              null=False, blank=False)
    tabla = models.CharField(max_length=100, verbose_name='Tabla', db_column='nau_tabla', null=False, blank=False)
    serie = models.CharField(max_length=2, verbose_name='Serie', db_column='nau_serie', null=True, blank=True)
    contador = models.IntegerField(verbose_name='Contador', db_column='nau_cuenta', null=False, blank=False, default=0)
    activo = models.BooleanField(verbose_name='Activo', db_column='nau_activo', default=False, null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.tabla}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'tabla': self.tabla,
            'serie': self.serie,
            'contador': self.contador,
            'activo': self.activo,
        }
        return item

    class Meta:
        db_table = 'sirtbnau'
        verbose_name = 'Numeración Automática'
        verbose_name_plural = 'Numeraciones Automáticas'
        ordering = ['codigo']


class UnidadMedida(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=1, verbose_name='Código', db_column='uni_codigo', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='uni_descrip', null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
        }
        return item

    class Meta:
        db_table = 'sirtbuni'
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['codigo']


class CodigoAproPieza(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=1, verbose_name='Código', db_column='cpz_codigo', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='cpz_descrip', null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
        }
        return item

    class Meta:
        db_table = 'sirtbcpz'
        verbose_name = 'Código Aprovisionamiento Pieza'
        verbose_name_plural = 'Códigos Aprovisionamiento Piezas'
        ordering = ['codigo']


class CodigoIva(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='iva_codigo', unique=True,
                              null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='iva_descrip',
                                   null=False, blank=False)
    porcentaje = models.DecimalField(verbose_name='Porcentaje', db_column='iva_porcent', default=0.0, max_digits=5,
                                    decimal_places=2, null=False, blank=False, validators=[validar_porcentaje])

    def __str__(self):
        return f'{self.codigo} - {self.descripcion} - {self.porcentaje}%'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'porcentaje': self.porcentaje,
        }
        return item

    class Meta:
        db_table = 'sirtbiva'
        verbose_name = 'Código IVA'
        verbose_name_plural = 'Códigos IVA'
        ordering = ['codigo']


class FamiliaPieza(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=3, verbose_name='Código', db_column='fpz_codigo', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='fpz_descrip', null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        # item = {}
        # if self.id is not None:
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
        }
        return item

    class Meta:
        db_table = 'sirtbfpz'
        verbose_name = 'Familia Pieza'
        verbose_name_plural = 'Familia Piezas'
        ordering = ['codigo']


class Marca(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='mca_codigo', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='mca_descrip', null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
        }
        return item

    class Meta:
        db_table = 'sirtbmca'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['codigo']


class CodigoContable(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='mca_codigo', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='mca_descrip', null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
        }
        return item

    class Meta:
        db_table = 'sirtbctb'
        verbose_name = 'Código Contable'
        verbose_name_plural = 'Códigos Contables'
        ordering = ['codigo']


class ModeloVehPieza(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='mca_codigo', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='mca_descrip', null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
        }
        return item

    class Meta:
        db_table = 'sirtbmov'
        verbose_name = 'Modelo Vehículo (Piezas)'
        verbose_name_plural = 'Modelos Vehículos (Piezas)'
        ordering = ['codigo']


class FamiliaMarketing(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=4, verbose_name='Código', db_column='mca_codigo', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='mca_descrip', null=True, blank=True)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    # para la paginación por select2
    def to_search_select(self, value):
        return self.objects.filter(Q(codigo__icontains=value) |
                                   Q(descripcion__icontains=value)
                                   )

    def to_list(self):
        # item = {}
        # if self.id is not None:
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
        }
        return item

    def to_list_select(self):
        item = {
            'id': self.id,
            'text': f'{self.codigo} - {self.descripcion}',
        }
        return item

    class Meta:
        db_table = 'sirtbfmk'
        verbose_name = 'Familia Marketing'
        verbose_name_plural = 'Familias Marketing'
        ordering = ['codigo']


class DescuentoRecambios(ModelMixin, BaseModel):
    tipo = models.CharField(max_length=1, verbose_name='Tipo', db_column='dtr_tipo', null=False, blank=False)
    codigo = models.CharField(max_length=1, verbose_name='Código', db_column='dtr_codigo', null=False, blank=False)
    codpieza = models.CharField(max_length=2, verbose_name='Cod pieza', db_column='dtr_codpza', null=False, blank=False)
    descuento = models.DecimalField(verbose_name='Porcentaje', db_column='dtr_descto', default=0.0, max_digits=5,
                                    decimal_places=2, null=False, blank=False, validators=[validar_porcentaje])

    def __str__(self):
        return f'{self.codigo} - {self.codpieza} - {self.descuento}%'

    def to_list(self):
        # item = {}
        # if self.id is not None:
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'codpieza': self.codpieza,
            'descuento': self.descuento,
        }
        return item

    class Meta:
        db_table = 'sirtbdtr'
        verbose_name = 'Descuento Recambios'
        verbose_name_plural = 'Descuentos Recambios'
        # constraint para que la combinación de código y sucursal no pueda repetirse
        unique_together = ['tipo', 'codigo', 'codpieza']
        ordering = ['tipo', 'codigo', 'codpieza']


class PrecioTarifa(ModelMixin, BaseModel):
    referencia = models.CharField(max_length=15, verbose_name='Referencia', db_column='ptr_refer', unique=True, null=False, blank=False)
    denominacion = models.CharField(max_length=100, verbose_name='Denominación', db_column='ptr_denom', null=True, blank=True)
    variacion = models.CharField(max_length=1, verbose_name='Variación', db_column='ptr_varia', null=True, blank=True)
    pvp = models.DecimalField(verbose_name='pvp', db_column='ptr_pvp', max_digits=9, decimal_places=2, null=True, blank=True)
    INDICE_CHOICES = [
        ('', ''),
        ('0001', 'Carrocería'),
        ('0002', 'Mantenimiento'),
        ('0003', 'Mecánica'),
        ('0004', 'Accesorios'),
        ('0005', 'Neumáticos'),
        ('0006', 'Publicidad'),
        ('0007', 'Otras marcas'),
        ('0008', 'Desgaste'),
    ]
    f1 = models.CharField(max_length=5, verbose_name='f1', choices=INDICE_CHOICES, default='', db_column='ptr_f1', null=True, blank=True)
    f2 = models.CharField(max_length=5, verbose_name='f2', db_column='ptr_f2', null=True, blank=True)
    f3 = models.CharField(max_length=7, verbose_name='f3', db_column='ptr_f3', null=True, blank=True)
    f4 = models.CharField(max_length=6, verbose_name='f4', db_column='ptr_f4', null=True, blank=True)
    f5 = models.CharField(max_length=1, verbose_name='f5', db_column='ptr_f5', null=True, blank=True)
    f6 = models.CharField(max_length=2, verbose_name='f6', db_column='ptr_f6', null=True, blank=True)
    f8 = models.CharField(max_length=1, verbose_name='f8', db_column='ptr_f8', null=True, blank=True)
    C_CHOICES = [
        ('', ''),
        ('1', 'Reemplazada por'),
        ('2', 'Reemplaza a'),
        ('3', 'Trascodificada a'),
        ('4', 'Trascodificada por'),
        ('5', 'No se sirve más'),
    ]
    f9 = models.CharField(max_length=1, verbose_name='f9', choices=C_CHOICES, default='', db_column='ptr_f9', null=True, blank=True)
    codigoDescuento = models.ForeignKey(DescuentoRecambios, on_delete=models.PROTECT, null=True, blank=True,
                                        db_column='ptr_codito', verbose_name='Código Descuento',
                                        limit_choices_to={'tipo': 1}, related_name='codapro')
    multiplo = models.IntegerField(verbose_name='Múltiplo', db_column='ptr_multiplo', null=True, blank=True)
    modeloVehiculo = models.CharField(max_length=2, verbose_name='Modelo Vehículo', db_column='ptr_modveh', null=True, blank=True)
    penetracion = models.CharField(max_length=1, verbose_name='Penetración', db_column='ptr_penet', null=True, blank=True)
    nuevaReferencia = models.CharField(max_length=15, verbose_name='Nueva Referencia', db_column='ptr_newrefer', null=True, blank=True)
    nuevaRefer2 = models.CharField(max_length=15, verbose_name='Nueva Referencia 2', db_column='ptr_newrefer2', null=True, blank=True)
    pvp1 = models.DecimalField(verbose_name='pvp1', db_column='ptr_pvp1', max_digits=9, decimal_places=2, null=True, blank=True)
    familiaMarketing = models.ForeignKey(FamiliaMarketing, on_delete=models.PROTECT, null=True, blank=True, db_column='ptr_fmark', verbose_name='Familia marketing')
    funcion = models.CharField(max_length=5, verbose_name='Función', db_column='ptr_funcion', null=True, blank=True)
    familia = models.ForeignKey(FamiliaPieza, on_delete=models.PROTECT, null=True, blank=True, db_column='ptr_familia', verbose_name='Familia')
    panier = models.CharField(max_length=1, verbose_name='Panier', db_column='ptr_panier', null=True, blank=True)
    codUrgencia = models.ForeignKey(DescuentoRecambios, on_delete=models.PROTECT, null=True, blank=True,
                                    db_column='ptr_codurg', verbose_name='Código Urgencia', limit_choices_to={'tipo': 2}, related_name='codurgte')

    def __str__(self):
        return f'{self.referencia} - {self.denominacion}'

    # recuperamos solo los campos necesarios para la paginación
    def to_list(self):
        if self.codigoDescuento is None:
            codigoDescuento = None
        else:
            codigoDescuento = self.codigoDescuento.codpieza
        if self.familiaMarketing is None:
            familiaMarketing = None
        else:
            familiaMarketing = self.familiaMarketing.codigo
        item = {
            'id': self.id,
            'referencia': self.referencia,
            'denominacion': self.denominacion,
            'nuevaReferencia': self.nuevaReferencia,
            'pvp': self.pvp,
            'multiplo': self.multiplo,
            'codigoDescuento': codigoDescuento,
            'penetracion': self.penetracion,
            'familiaMarketing': familiaMarketing,
            'f1': self.f1,
            'f9': self.f9,
            'f2': self.f2,
        }
        if self.f9 is None or self.f9.strip() == '':
            item['f9'] = ''
        else:
            item['f9'] = f'{self.f9}-{self.get_f9_display()}'
        if self.f1 is None or self.f1.strip() == '':
            item['f1'] = ''
        elif self.f1 == self.get_f1_display():
            item['f1'] = self.f1
        else:
            item['f1'] = f'{self.f1}-{self.get_f1_display()}'
        if self.f2 is None or self.f2.strip() == '':
            item['f2'] = ''
        else:
            item['f2'] = f' (Seg. {self.f2})'
        return item

    # recuperamos solo los campos necesarios para la paginación modal
    def to_list_modal(self):
        if self.codigoDescuento is None:
            codigoDescuento = {}
        else:
            codigoDescuento = self.codigoDescuento.to_list()
        if self.codUrgencia is None:
            codUrgencia = {}
        else:
            codUrgencia = self.codUrgencia.to_list()
        if self.familia is None:
            familia = {}
        else:
            familia = self.familia.to_list()
        if self.familiaMarketing is None:
            familiaMarketing = {}
        else:
            familiaMarketing = self.familiaMarketing.to_list()

        codAproPieza = CodigoAproPieza.objects.get(codigo='E').to_list()
        item = {
            'id': self.id,
            'referencia': self.referencia,
            'denominacion': self.denominacion,
            'pvp': self.pvp,
            'multiplo': self.multiplo,
            'codigoDescuento': codigoDescuento,
            'codUrgencia': codUrgencia,
            'familia': familia,
            'familiaMarketing': familiaMarketing,
            'panier': self.panier,
            'funcion': self.funcion,
            'codAproPieza': codAproPieza,
        }
        return item

    # para la paginación por servidor utilizamos este método para los filtros
    def to_search(self, value):
        return self.objects.filter(Q(referencia__icontains=value) |
                                   Q(denominacion__icontains=value) |
                                   Q(nuevaReferencia__icontains=value) |
                                   Q(penetracion__icontains=value) |
                                   Q(f1__icontains=value) |
                                   Q(f9__icontains=value)
                                   )

    def to_search_modal(self, value):
        return self.objects.filter(Q(referencia__icontains=value) |
                                   Q(denominacion__icontains=value)
                                   )

    class Meta:
        db_table = 'sirtbptr'
        verbose_name = 'Precio'
        verbose_name_plural = 'Lista de Precios'
        ordering = ['referencia']


class Articulo(ModelMixin, BaseModel):
    referencia = models.CharField(max_length=15, verbose_name='Referencia', db_column='ref_refer', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='ref_descrip', null=False, blank=False)
    tarifa = models.DecimalField(verbose_name='Precio tarifa', db_column='ref_tarifa', max_digits=9, default=0, decimal_places=2, null=False, blank=False)
    existencias = models.IntegerField(verbose_name='Existencias', db_column='ref_exist', default=0, null=True, blank=True)
    nuevaReferencia = models.CharField(max_length=15, verbose_name='Nueva Referencia', db_column='ref_newrefer', null=True, blank=True)
    precioCosteMedio = models.DecimalField(verbose_name='Precio coste medio', db_column='ref_pcostmed', max_digits=9, default=0, decimal_places=2, null=False, blank=False)
    precioInicial = models.DecimalField(verbose_name='Precio inicial', db_column='ref_pinicial', max_digits=9, default=0, decimal_places=2, null=False, blank=False)
    precioCoste = models.DecimalField(verbose_name='Precio coste', db_column='ref_pcoste', max_digits=9, default=0, decimal_places=2, null=False, blank=False)
    proveedor = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=False, blank=False, db_column='ref_proved', verbose_name='Proveedor')
    codigoPromo = models.ForeignKey(DescuentoRecambios, on_delete=models.PROTECT, null=True, blank=True,
                                    db_column='ref_cpromo', verbose_name='Descuento promo', limit_choices_to={'tipo': '3'}, related_name='pedcamp')
    codigoApro = models.ForeignKey(DescuentoRecambios, on_delete=models.PROTECT, null=False, blank=False,
                                   db_column='ref_capro', verbose_name='Descuento apro', limit_choices_to={'tipo': '1'}, related_name='pedapro')
    codigoUrgte = models.ForeignKey(DescuentoRecambios, on_delete=models.PROTECT, null=True, blank=True,
                                    db_column='ref_curgte', verbose_name='Descuento urgente', limit_choices_to={'tipo': '2'}, related_name='pedurgte')
    precioPromo = models.DecimalField(verbose_name='Precio promoción', db_column='ref_ppromo', max_digits=9, default=0, decimal_places=2, null=False, blank=False)
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, null=True, blank=True, db_column='ref_unimed', verbose_name='Unidad Medida')
    unidadCompra = models.IntegerField(verbose_name='Unidad de compra', db_column='ref_unicomp', default=1, null=True, blank=True)
    unidadVenta = models.IntegerField(verbose_name='Unidad de venta', db_column='ref_univta', default=1, null=True, blank=True)
    unidadStock = models.IntegerField(verbose_name='Unidad de stock', db_column='ref_unistk', default=1, null=True, blank=True)
    multiplo = models.IntegerField(verbose_name='Múltiplo', db_column='ref_multi', default=1, null=True, blank=True)
    ubicacion = models.CharField(max_length=15, verbose_name='Ubicación', db_column='ref_ubica', null=True, blank=True)
    codAproPieza = models.ForeignKey(CodigoAproPieza, on_delete=models.PROTECT, null=False, blank=False, db_column='ref_capropza', verbose_name='Código Aprovisionamiento')
    pedidosPendientes = models.IntegerField(verbose_name='Pedidos pendientes', db_column='ref_pedpte', default=0, null=True, blank=True)
    entradasMes = models.IntegerField(verbose_name='Entradas mes', db_column='ref_entmes', default=0, null=True, blank=True)
    salidasMes = models.IntegerField(verbose_name='Salidas mes', db_column='ref_salmes', default=0, null=True, blank=True)
    entradasAcumuladas = models.IntegerField(verbose_name='Entradas acumuladas', db_column='ref_entacum', default=0, null=True, blank=True)
    salidasAcumuladas = models.IntegerField(verbose_name='Salidas acumuladas', db_column='ref_salacum', default=0, null=True, blank=True)
    fechaUltMovimiento = models.DateTimeField(verbose_name='Fecha último movimiento', db_column='ref_fultmov', null=True, blank=True)
    fechaUltimaVenta = models.DateTimeField(verbose_name='Fecha última venta', db_column='ref_fultvta', null=True, blank=True)
    fechaUltimaCompra = models.DateTimeField(verbose_name='Fecha última compra', db_column='ref_fultcomp', null=True, blank=True)
    observaciones = models.TextField(verbose_name='Observaciones', db_column='ref_obser', null=True, blank=True)
    ivaPieza = models.ForeignKey(CodigoIva, on_delete=models.PROTECT, null=False, blank=False, db_column='ref_iva', verbose_name='IVA pieza')
    consumoMedio = models.IntegerField(verbose_name='Consumo medio', db_column='ref_consumedio', null=True, blank=True)
    stockSeguridad = models.IntegerField(verbose_name='Stock de seguridad', db_column='ref_stkmax', default=0, null=True, blank=True)
    puntoPedido = models.IntegerField(verbose_name='Punto pedido', db_column='ref_ptoped', default=0, null=True, blank=True)
    stockMinimo = models.IntegerField(verbose_name='Stock mínimo', db_column='ref_stkmin', default=0, null=True, blank=True)
    codigoAbc = models.CharField(max_length=2, verbose_name='Código ABC', db_column='ref_codabc', null=True, blank=True)
    codigoObsoleto = models.CharField(max_length=1, verbose_name='Código obsoleto', db_column='ref_codobs', default='0', null=True, blank=True)
    codigoFuncion = models.CharField(max_length=5, verbose_name='Código función', db_column='ref_codfunc', null=True, blank=True)
    panier = models.CharField(max_length=1, verbose_name='Panier', db_column='ref_panier', null=True, blank=True)
    familia = models.ForeignKey(FamiliaPieza, on_delete=models.PROTECT, null=True, blank=True, db_column='ref_familia', verbose_name='Familia pieza')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, null=True, blank=True, db_column='ref_marca', verbose_name='Marca')
    codigoContable = models.ForeignKey(CodigoContable, on_delete=models.PROTECT, null=True, blank=True,
                                       db_column='ref_cconta', verbose_name='Código Contable')
    COD_COMPETENCIA_CHOICES = [
        ('00', 'Competitiva'),
        ('01', 'No Competitiva'),
    ]
    codigoCompetencia = models.CharField(max_length=2, verbose_name='Código Competencia',
                                         choices=COD_COMPETENCIA_CHOICES, db_column='ref_ccompet', null=True,
                                         blank=True)
    codigoModelo = models.ForeignKey(ModeloVehPieza, on_delete=models.PROTECT, null=True, blank=True, db_column='ref_modelo', verbose_name='Modelo')
    familiaMarketing = models.ForeignKey(FamiliaMarketing, on_delete=models.PROTECT, null=True, blank=True, db_column='ref_fmark', verbose_name='Familia marketing')
    difinventario = models.IntegerField(verbose_name='Diferencia inventario', db_column='ref_difinv', null=True, blank=True)
    fechaUltimoInventario = models.DateTimeField(verbose_name='Fecha último inventario', db_column='ref_fultinv', null=True, blank=True)
    unidadesVendidasMes = models.IntegerField(verbose_name='Unidades vendidas mes', db_column='ref_uvenmes', null=True, blank=True)
    unidadesVendidasAno = models.IntegerField(verbose_name='Unidades vendidas año', db_column='ref_uvenano', null=True, blank=True)
    unidadesVendidasAnoAnt = models.IntegerField(verbose_name='Unidades vendidas año anterior', db_column='ref_uvenanoant', null=True, blank=True)
    bloqueoPieza = models.CharField(max_length=1, verbose_name='Bloqueo pieza', db_column='ref_blqpieza', null=True, blank=True)
    fechaBloqueo = models.DateTimeField(verbose_name='Fecha bloqueo', db_column='ref_fblqpieza', null=True, blank=True)
    unidadesVendidas12m = models.IntegerField(verbose_name='Unidades vendidas 12 meses', db_column='ref_uven12m', null=True, blank=True)
    stockinicialano = models.IntegerField(verbose_name='Stock inicial año', db_column='ref_stkiniano', null=True, blank=True)
    unidadesVendidasm1 = models.IntegerField(verbose_name='Unidades vendidas mes 1', db_column='ref_uvenm1', null=True, blank=True)
    unidadesVendidasm2 = models.IntegerField(verbose_name='Unidades vendidas mes 2', db_column='ref_uvenm2', null=True, blank=True)
    unidadesVendidasm3 = models.IntegerField(verbose_name='Unidades vendidas mes 3', db_column='ref_uvenm3', null=True, blank=True)
    unidadesVendidasm4 = models.IntegerField(verbose_name='Unidades vendidas mes 4', db_column='ref_uvenm4', null=True, blank=True)
    unidadesVendidasm5 = models.IntegerField(verbose_name='Unidades vendidas mes 5', db_column='ref_uvenm5', null=True, blank=True)
    unidadesVendidasm6 = models.IntegerField(verbose_name='Unidades vendidas mes 6', db_column='ref_uvenm6', null=True, blank=True)
    unidadesVendidasm7 = models.IntegerField(verbose_name='Unidades vendidas mes 7', db_column='ref_uvenm7', null=True, blank=True)
    unidadesVendidasm8 = models.IntegerField(verbose_name='Unidades vendidas mes 8', db_column='ref_uvenm8', null=True, blank=True)
    unidadesVendidasm9 = models.IntegerField(verbose_name='Unidades vendidas mes 9', db_column='ref_uvenm9', null=True, blank=True)
    unidadesVendidasm10 = models.IntegerField(verbose_name='Unidades vendidas mes 10', db_column='ref_uvenm10', null=True, blank=True)
    unidadesVendidasm11 = models.IntegerField(verbose_name='Unidades vendidas mes 11', db_column='ref_uvenm11', null=True, blank=True)
    unidadesVendidasm12 = models.IntegerField(verbose_name='Unidades vendidas mes 12', db_column='ref_uvenm12', null=True, blank=True)
    demandaNoServidaDia = models.IntegerField(verbose_name='Demanda no servida día', db_column='ref_demnoserd', null=True, blank=True)
    demandaNoServidaMes = models.IntegerField(verbose_name='Demanda no servida mes', db_column='ref_demmpserm', null=True, blank=True)
    demandaNoServidaAno = models.IntegerField(verbose_name='Demanda no servida año', db_column='ref_demmosera', null=True, blank=True)
    reserva = models.IntegerField(verbose_name='Reserva', db_column='ref_reserva', null=True, blank=True)
    unidadesCompradasMes = models.IntegerField(verbose_name='Unidades compradas mes', db_column='ref_unicompm', null=True, blank=True)
    unidadesCompradasAno = models.IntegerField(verbose_name='Unidades compradas año', db_column='ref_unicompa', null=True, blank=True)
    unidadesCompradasAnoAnt = models.IntegerField(verbose_name='Unidades compradas año anterior', db_column='ref_unicompant', null=True, blank=True)
    unidadesSalTallerMes = models.IntegerField(verbose_name='Unidades salida taller mes', db_column='ref_unisaltames', null=True, blank=True)
    unidadesSalTallerAno = models.IntegerField(verbose_name='Unidades salida taller año', db_column='ref_unisaltaano', null=True, blank=True)
    otrasEntradasMes = models.IntegerField(verbose_name='Otras entradas mes', db_column='ref_otrentmes', null=True, blank=True)
    otrasEntradasAno = models.IntegerField(verbose_name='Otras entradas año', db_column='ref_otrentano', null=True, blank=True)
    otrasSalidasMes = models.IntegerField(verbose_name='Otras salidas mes', db_column='ref_otrsalmes', null=True, blank=True)
    otrasSalidasAno = models.IntegerField(verbose_name='Otras salidas año', db_column='ref_otrsalano', null=True, blank=True)
    importeVtasMesPvp = models.DecimalField(verbose_name='Importe ventas mes pvp', db_column='ref_ivtamespvp', max_digits=9, decimal_places=2, null=True, blank=True)
    importeVtasMesCoste = models.DecimalField(verbose_name='Importe ventas mes coste', db_column='ref_ivtamescos', max_digits=9, decimal_places=2, null=True, blank=True)
    importeVtasAnoPvp = models.DecimalField(verbose_name='Importe ventas año pvp', db_column='ref_ivtaanopvp', max_digits=9, decimal_places=2, null=True, blank=True)
    importeVtasAnoCoste = models.DecimalField(verbose_name='Importe ventas año coste', db_column='ref_ivtaanocos', max_digits=9, decimal_places=2, null=True, blank=True)
    importeVtasAnoAntPvp = models.DecimalField(verbose_name='Importe ventas año anterior pvp', db_column='ref_ivtaanoantpvp', max_digits=9, decimal_places=2, null=True, blank=True)
    importeVtasAnoAntCoste = models.DecimalField(verbose_name='Importe ventas año anterior coste', db_column='ref_ivtaanoantcos', max_digits=9, decimal_places=2, null=True, blank=True)
    importeDtoMes = models.DecimalField(verbose_name='Importe descuentos mes', db_column='ref_idtomes', max_digits=9, decimal_places=2, null=True, blank=True)
    importeDtoAno = models.DecimalField(verbose_name='Importe descuentos año', db_column='ref_idtoano', max_digits=9, decimal_places=2, null=True, blank=True)
    importeComprasMes = models.DecimalField(verbose_name='Importe compras mes', db_column='ref_icommes', max_digits=9, decimal_places=2, null=True, blank=True)
    importeComprasAno = models.DecimalField(verbose_name='Importe compras año', db_column='ref_icomano', max_digits=9, decimal_places=2, null=True, blank=True)
    importeComprasAnoAnt = models.DecimalField(verbose_name='Importe compras año anterior', db_column='ref_icomanoant', max_digits=9, decimal_places=2, null=True, blank=True)
    importeSalTallerMes = models.DecimalField(verbose_name='Importe salidas taller mes', db_column='ref_isaltames', max_digits=9, decimal_places=2, null=True, blank=True)
    importeSalTallerAno = models.DecimalField(verbose_name='Importe salidas taller año', db_column='ref_isaltaano', max_digits=9, decimal_places=2, null=True, blank=True)
    importeOtrasSalmes = models.DecimalField(verbose_name='Importe otras salidas mes', db_column='ref_iotrsalmes', max_digits=9, decimal_places=2, null=True, blank=True)
    importeOtrasSalano = models.DecimalField(verbose_name='Importe otras salidas año', db_column='ref_iotrsalano', max_digits=9, decimal_places=2, null=True, blank=True)
    importeOtrasEntmes = models.DecimalField(verbose_name='Importe otras entradas mes', db_column='ref_iotrentmes', max_digits=9, decimal_places=2, null=True, blank=True)
    importeOtrasEntano = models.DecimalField(verbose_name='Importe otras entradas año', db_column='ref_iotrentano', max_digits=9, decimal_places=2, null=True, blank=True)
    bloqueo = models.BooleanField(verbose_name='Bloqueo', db_column='ref_bloqueo', default=False, null=True, blank=True)
    ns = models.BooleanField(verbose_name='Ns', db_column='ref_ns', default=False, null=True, blank=True)
    negativo = models.BooleanField(verbose_name='Negativo', db_column='ref_negativo', default=False, null=True, blank=True)
    imprimir = models.BooleanField(verbose_name='Imprimir', db_column='ref_imprimir', default=False, null=True, blank=True)
    unidadesUltimaCompra = models.IntegerField(verbose_name='Unidades última compra', db_column='ref_uniultcom', null=True, blank=True)
    unidadesUltimaVenta = models.IntegerField(verbose_name='Unidades última venta', db_column='ref_uniultvta', null=True, blank=True)
    codAlerta = models.CharField(max_length=1, verbose_name='Código alerta', db_column='ref_codalert', null=True, blank=True)
    unidadesDq = models.IntegerField(verbose_name='Unidades dq', db_column='ref_unidq', null=True, blank=True)
    unidadesDq1 = models.IntegerField(verbose_name='Unidades dq1', db_column='ref_unidq1', null=True, blank=True)
    unidadesDq2 = models.IntegerField(verbose_name='Unidades dq2', db_column='ref_unidq2', null=True, blank=True)
    unidadesDq3 = models.IntegerField(verbose_name='Unidades dq3', db_column='ref_unidq3', null=True, blank=True)
    unidadesDq4 = models.IntegerField(verbose_name='Unidades dq4', db_column='ref_unidq4', null=True, blank=True)
    unidadesDq5 = models.IntegerField(verbose_name='Unidades dq5', db_column='ref_unidq5', null=True, blank=True)
    unidadesDq6 = models.IntegerField(verbose_name='Unidades dq6', db_column='ref_unidq6', null=True, blank=True)
    unidadesDq7 = models.IntegerField(verbose_name='Unidades dq7', db_column='ref_unidq7', null=True, blank=True)
    unidadesDq8 = models.IntegerField(verbose_name='Unidades dq8', db_column='ref_unidq8', null=True, blank=True)
    unidadesDq9 = models.IntegerField(verbose_name='Unidades dq9', db_column='ref_unidq9', null=True, blank=True)
    unidadesDq10 = models.IntegerField(verbose_name='Unidades dq10', db_column='ref_unidq10', null=True, blank=True)
    unidadesDq11 = models.IntegerField(verbose_name='Unidades dq11', db_column='ref_unidq11', null=True, blank=True)
    unidadesDq12 = models.IntegerField(verbose_name='Unidades dq12', db_column='ref_unidq12', null=True, blank=True)
    unidadesDqx = models.IntegerField(verbose_name='Unidades dqx', db_column='ref_unidqx', null=True, blank=True)
    unidadesDq1x = models.IntegerField(verbose_name='Unidades dq1x', db_column='ref_unidq1x', null=True, blank=True)
    unidadesDq2x = models.IntegerField(verbose_name='Unidades dq2x', db_column='ref_unidq2x', null=True, blank=True)
    unidadesDq3x = models.IntegerField(verbose_name='Unidades dq3x', db_column='ref_unidq3x', null=True, blank=True)
    unidadesDq4x = models.IntegerField(verbose_name='Unidades dq4x', db_column='ref_unidq4x', null=True, blank=True)
    unidadesDq5x = models.IntegerField(verbose_name='Unidades dq5x', db_column='ref_unidq5x', null=True, blank=True)
    unidadesDq6x = models.IntegerField(verbose_name='Unidades dq6x', db_column='ref_unidq6x', null=True, blank=True)
    unidadesDq7x = models.IntegerField(verbose_name='Unidades dq7x', db_column='ref_unidq7x', null=True, blank=True)
    unidadesDq8x = models.IntegerField(verbose_name='Unidades dq8x', db_column='ref_unidq8x', null=True, blank=True)
    stockMinimoP = models.IntegerField(verbose_name='Stock mínimo p', db_column='ref_stkminp', null=True, blank=True)
    stockSeguridadP = models.IntegerField(verbose_name='Stock seguridad p', db_column='ref_stksegp', null=True, blank=True)
    puntoPedidoP = models.IntegerField(verbose_name='Punto pedido p', db_column='ref_ptopedp', null=True, blank=True)
    consumoP = models.IntegerField(verbose_name='Consumo p', db_column='ref_cosumop', null=True, blank=True)
    fechaAlta = models.DateTimeField(verbose_name='Fecha alta', db_column='ref_falta', null=False, blank=False)

    def __str__(self):
        return f'{self.referencia} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'referencia': self.referencia,
            'descripcion': self.descripcion,
            'existencias': self.existencias,
            'tarifa': self.tarifa,
        }
        return item

    # para la paginación por servidor utilizamos este método para los filtros
    def to_search(self, value):
        return self.objects.filter(Q(referencia__icontains=value) |
                                   Q(descripcion__icontains=value)
                                   )

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     print(f'save en models.py')
    #     # # Datos calculados
    #     # self.precioCoste = self.tarifa - (self.tarifa * self.codigoApro.descuento / 100)
    #     # if self.codigoPromo is None:
    #     #     self.precioPromo = 0
    #     # else:
    #     #     self.precioPromo = self.tarifa - (self.tarifa * self.codigoPromo.descuento / 100)
    #
    #     # if not self.pk:
    #     #     # Inicializamos campos en altas
    #     #     self.precioCosteMedio = self.precioCoste
    #
    #     super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    class Meta:
        db_table = 'sirtbref'
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        ordering = ['referencia']


class Tasa(ModelMixin, BaseModel):
    referencia = models.OneToOneField(Articulo, on_delete=models.CASCADE, unique=True, null=False, blank=False, db_column='tas_refer', verbose_name='Referencia')
    denominacion = models.CharField(max_length=100, verbose_name='Denominación tasa', db_column='tas_denom', null=True, blank=True)
    precio = models.DecimalField(verbose_name='Precio', db_column='tas_precio', max_digits=9, default=0,
                                 decimal_places=2, null=False, blank=False)
    descuento = models.DecimalField(verbose_name='Descuento', db_column='tas_descuento', max_digits=5,
                                    decimal_places=2, null=True, blank=True, validators=[validar_porcentaje])

    def __str__(self):
        return f'{self.referencia.referencia} - {self.denominacion} - {self.precio} - {self.descuento}%'

    def to_list(self):
        item = {
            'id': self.id,
            'referencia': self.referencia.referencia,
            'denominacion': self.denominacion,
            'precio': self.precio,
            'descuento': self.descuento,
        }
        return item

    class Meta:
        db_table = 'sirtbtas'
        verbose_name = 'Tasa'
        verbose_name_plural = 'Tasas'


class TasaCodigo(ModelMixin, BaseModel):
    codcontable = models.ForeignKey(CodigoContable, on_delete=models.CASCADE, null=False, blank=False, db_column='tsc_codigo', verbose_name='Código contable')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='tsc_descrip', null=False, blank=False)
    precio = models.DecimalField(verbose_name='Precio', db_column='tsc_precio', max_digits=9, decimal_places=2, null=False, blank=False)
    descuento = models.DecimalField(verbose_name='Descuento', db_column='tsc_descuento', max_digits=5,
                                    decimal_places=2, null=True, blank=True, validators=[validar_porcentaje])

    def __str__(self):
        if self.descuento is None:
            dto = ''
        else:
            dto = str(self.descuento)
        return f'{self.descripcion} - PVP: {self.precio} - Dto: {dto}'

    def to_list(self):
        item = {
            'id': self.id,
            'codcontable': f'{self.codcontable.codigo} - {self.codcontable.descripcion}',
            'descripcion': self.descripcion,
            'precio': self.precio,
            'descuento': self.descuento,
        }
        return item

    class Meta:
        db_table = 'sirtbtsc'
        verbose_name = 'Código Tasa'
        verbose_name_plural = 'Códigos Tasas'


class TasaNeumatico(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='tsn_codigo', unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='tsn_descrip', null=False, blank=False)
    precio = models.DecimalField(verbose_name='Precio', db_column='tsn_precio', max_digits=9, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion} - PVP: {self.precio}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'precio': self.precio,
        }
        return item

    class Meta:
        db_table = 'sirtbtsn'
        verbose_name = 'Tasa Neumático'
        verbose_name_plural = 'Tasas Neumáticos'


class Gama(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='gam_codigo', unique=True,
                              null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='gam_descrip',
                                   null=False, blank=False)
    objetivo = models.IntegerField(verbose_name='Objetivo', db_column='gam_objetivo', null=False, blank=False, default=0)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'objetivo': self.objetivo,
        }
        return item

    class Meta:
        db_table = 'sirtbgam'
        verbose_name = 'Gama Vehículo'
        verbose_name_plural = 'Gamas Vehículos'
        ordering = ['codigo']


class Modelo(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=6, verbose_name='Código', db_column='mod_codigo', unique=True,
                              null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='mod_descrip',
                                   null=False, blank=False)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
        }
        return item

    def to_list_select(self):
        item = {
            'id': self.id,
            'text': f'{self.codigo} - {self.descripcion}',
        }
        return item

    # para la paginación por select2
    def to_search_select(self, value):
        return self.objects.filter(Q(codigo__icontains=value) |
                                   Q(descripcion__icontains=value)
                                   )

    class Meta:
        db_table = 'sirtbmod'
        verbose_name = 'Modelo Vehículo'
        verbose_name_plural = 'Modelos Vehículos'
        ordering = ['codigo']


class Concesionario(ModelMixin, BaseModel):
    codigo = models.CharField(max_length=6, verbose_name='Código', db_column='cnc_codigo', unique=True,
                              null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='cnc_descrip',
                                   null=False, blank=False)
    compostaje = models.IntegerField(verbose_name='Compostaje', db_column='cbc_compostaje', null=False, blank=False, default=0)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    def to_list(self):
        item = {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'compostaje': self.compostaje,
        }
        return item

    def to_list_select(self):
        item = {
            'id': self.id,
            'text': f'{self.codigo} - {self.descripcion}',
        }
        return item

    # para la paginación por select2
    def to_search_select(self, value):
        return self.objects.filter(Q(codigo__icontains=value) |
                                   Q(descripcion__icontains=value)
                                   )

    class Meta:
        db_table = 'sirtbcnc'
        verbose_name = 'Concesionario Garantías'
        verbose_name_plural = 'Concesionarios Garantías'
        ordering = ['codigo']


class Vehiculo(ModelMixin, BaseModel):
    matricula = models.CharField(max_length=10, verbose_name='matrícula', db_column='veh_matri', null=True, blank=True)
    vin = models.CharField(max_length=17, verbose_name='vin', db_column='veh_vin', null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=False, blank=False, db_column='veh_cliente', verbose_name='cliente')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, null=True, blank=True, db_column='veh_marca', verbose_name='marca')
    gama = models.ForeignKey(Gama, on_delete=models.PROTECT, null=False, blank=False, db_column='veh_gama', verbose_name='gama')
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, null=False, blank=False, db_column='veh_modelo', verbose_name='modelo')
    concesionario = models.ForeignKey(Concesionario, on_delete=models.PROTECT, null=False, blank=False, db_column='veh_conces', verbose_name='concesionario')
    kilometros = models.IntegerField(verbose_name='kilometros', db_column='veh_kmts', null=True, blank=True)
    fechaVenta = models.DateTimeField(verbose_name='Fecha venta', db_column='veh_fventa', null=True, blank=True)
    fechaFinGarantia = models.DateTimeField(verbose_name='Fecha fin garantía', db_column='veh_ffingar', null=True, blank=True)
    notas = models.TextField(verbose_name='notas', db_column='veh_notas', null=True, blank=True)
    norgpr = models.CharField(max_length=5, verbose_name='norgpr', db_column='veh_norgpr', null=True, blank=True)
    aorgpr = models.CharField(max_length=2, verbose_name='aorgpr', db_column='veh_aorgpr', null=True, blank=True)
    arranque = models.CharField(max_length=8, verbose_name='arranque', db_column='veh_arranq', null=True, blank=True)
    llave = models.CharField(max_length=10, verbose_name='llave', db_column='veh_llave', null=True, blank=True)
    mando = models.CharField(max_length=8, verbose_name='mando', db_column='veh_mando', null=True, blank=True)
    radio = models.CharField(max_length=8, verbose_name='radio', db_column='veh_radio', null=True, blank=True)
    fechaItv = models.DateTimeField(verbose_name='Fecha ITV', db_column='veh_fecitv', null=True, blank=True)
    neumatico = models.CharField(max_length=15, verbose_name='neumatico', db_column='veh_neumat', null=True, blank=True)
    fechaNeumatico = models.DateTimeField(verbose_name='Fecha Neumático', db_column='veh_fneuma', null=True, blank=True)
    opPreventiva = models.BooleanField(verbose_name='operación preventiva', db_column='veh_opprev', default=False, null=False, blank=False)

    def __str__(self):
        return f'| {self.matricula} | {self.vin}'

    def to_list(self):
        # print(f'id: {self.id}')
        # si el vehículo tiene un código marca con nulo no se puede extraer la descipción y peta el datatable
        # al intentar ordenar por algún campo que en la primera página obtenga ese nulo
        if self.marca is None:
            marca_d = ''
        else:
            marca_d = self.marca.descripcion
        # Para los nombres de los campos que son foreing key (Cliente, Marca, Modelo)
        # definimos también el campo por el que queremos ordenar el datatable
        item = {
            'id': self.id,
            'matricula': self.matricula,
            'vin': self.vin,
            'cliente__codigo': self.cliente.codigo,
            # 'marca': self.marca.descripcion,
            'marca__descripcion': marca_d,
            'modelo__descripcion': self.modelo.descripcion,
        }
        # print(f'item: {item}')
        return item

    # para la paginación por servidor utilizamos este método para los filtros
    def to_search(self, value):
        return self.objects.filter(Q(matricula__icontains=value) |
                                   Q(vin__icontains=value) |
                                   Q(cliente__codigo__icontains=value) |
                                   Q(marca__descripcion__icontains=value) |
                                   Q(modelo__descripcion__icontains=value)
                                   )

    class Meta:
        db_table = 'sirtbveh'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        # constraint para que la combinación de matrícula y vin no pueda repetirse
        unique_together = ['matricula', 'vin']
        ordering = ['matricula', 'vin']

