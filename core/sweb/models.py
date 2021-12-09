from django.db import models


class Banco(models.Model):
    codigo = models.CharField(max_length=4, verbose_name='código banco', db_column='ban_codcsp', null=False)
    sucursal = models.CharField(max_length=4, verbose_name='sucursal', db_column='ban_sucursal', null=False)
    cuenta = models.CharField(max_length=15, verbose_name='número cuenta', db_column='ban_cuenta',null=True)
    dgc = models.CharField(max_length=1, verbose_name='dígito control', db_column='ban_dgc', null=True)
    dgc2 = models.CharField(max_length=1, verbose_name='dígito control 2', db_column='ban_dgc2', null=True)
    codbcoe = models.CharField(max_length=8, db_column='ban_codbcoe', null=True)
    razonsocial = models.CharField(max_length=100, db_column='ban_rsocial', verbose_name='razón social', null=True)
    tipovia = models.CharField(max_length=2, verbose_name='tipo vía', db_column='ban_tipovia', null=True)
    nomvia = models.CharField(max_length=100, verbose_name='nombre vía', db_column='ban_nomvia', null=True)
    numvia = models.CharField(max_length=3, verbose_name='número vía', db_column='ban_numvia', null=True)
    codpostal = models.CharField(max_length=5, verbose_name='código postal', db_column='ban_cpostal', null=True)
    municipio = models.CharField(max_length=100, verbose_name='municipio', db_column='ban_mncipio', null=True)
    provincia = models.CharField(max_length=100, verbose_name='provincia', db_column='ban_provin', null=True)
    telex = models.CharField(max_length=25, verbose_name='telex', db_column='ban_telex',null=True)
    prefijo = models.IntegerField(db_column='ban_preftel', verbose_name='prefijo teléfono', null=True)
    telefono = models.IntegerField(db_column='ban_telef', verbose_name='teléfono', null=True)
    telperso = models.IntegerField(db_column='ban_telper', verbose_name='teléfono personal', null=True)
    extension = models.IntegerField(db_column='ban_extelf', verbose_name='extensión', null=True)
    contacto = models.CharField(max_length=100, verbose_name='contacto', db_column='ban_contac', null=True)

    def __str__(self):
        return self.codigo + self.sucursal

    class Meta:
        db_table = 'sirtbban'
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        # constraint para que la combinación de código y sucursal no pueda repetirse
        unique_together = ['codigo', 'sucursal']


class DescuentoMO(models.Model):
    codigo = models.CharField(max_length=1, verbose_name='código MO', db_column='dmo_codigo', unique=True,
                              null=False, blank=False)
    descripcion = models.CharField(max_length=100, verbose_name='descripción', db_column='dmo_descrip',
                                   null=False, blank=False)
    descuento = models.DecimalField(verbose_name='descuento MO', max_digits=5, decimal_places=2, null=False)

    def __str__(self):
        return f'{self.codigo} {self.descripcion}'

    class Meta:
        db_table = 'sirtbdmo'
        verbose_name = 'Descuento MO'
        verbose_name_plural = 'Descuentos MO'


class FormaDePago(models.Model):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='fpg_codigo', unique=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='fpg_descrip',
                                   null=False, blank=False)
    recibos = models.IntegerField(verbose_name='Recibos', db_column='fpg_recibos', default=0, null=True)
    diasvto = models.IntegerField(verbose_name='Días vencimiento factura', db_column='fpg_diasvto', default=0, null=True)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    class Meta:
        db_table = 'sirtbfpg'
        verbose_name = 'Forma de Pago'
        verbose_name_plural = 'Formas de Pago'
        ordering = ['codigo']

    def clean(self):
        super(FormaDePago, self).clean()
        self.codigo = self.codigo.upper()


class TipoClienteRecambios(models.Model):
    codigo = models.CharField(max_length=2, verbose_name='Código', db_column='tcr_codigo', unique=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='tcr_descrip',
                                   null=False, blank=False)
    datocontable = models.CharField(max_length=1, verbose_name='Dato contable', db_column='tcr_datocon', null=True)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

    class Meta:
        db_table = 'sirtbtcr'
        verbose_name = 'Tipo de Cliente Recambios'
        verbose_name_plural = 'Tipos de Cliente Recambios'
        ordering = ['codigo']

    def clean(self):
        super(TipoClienteRecambios, self).clean()
        self.codigo = self.codigo.upper()
