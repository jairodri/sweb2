from django.db import models
from core.sweb.utils import digitos_control, validar_porcentaje
from core.models import BaseModel
from core.sweb.mixins import ModelMixin


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
        if self.nombre:
            return f'{self.codigo} - {self.nombre} - {self.apellido1} - {self.apellido2}'
        else:
            return f'{self.codigo} - {self.razonSocial}'

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

    class Meta:
        db_table = 'sirtbfmk'
        verbose_name = 'Familia Marketing'
        verbose_name_plural = 'Familias Marketing'
        ordering = ['codigo']
