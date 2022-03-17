from django.contrib import admin
from core.sweb.models import *
from import_export.admin import ImportExportModelAdmin
from core.sweb.resources import *


class DescuentoMOAdmin(ImportExportModelAdmin):
    resource_class = DescuentoMOResource


class BancoAdmin(ImportExportModelAdmin):
    resource_class = BancoResource


class FormaDePagoAdmin(ImportExportModelAdmin):
    resource_class = FormaDePagoResource


class TipoClienteRecambiosAdmin(ImportExportModelAdmin):
    resource_class = TipoClienteRecambiosResource


class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource


class NumeracionAutomaticaAdmin(ImportExportModelAdmin):
    resource_class = NumeracionAutomaticaResource


class UnidadMedidaAdmin(ImportExportModelAdmin):
    resource_class = UnidadMedidaResource


class CodigoAproPiezaAdmin(ImportExportModelAdmin):
    resource_class = CodigoAproPiezaResource


class CodigoIvaAdmin(ImportExportModelAdmin):
    resource_class = CodigoIvaResource


# Register your models here.
# Para que se muestren en el panel administrador del servidor
admin.site.register(Banco, BancoAdmin)
admin.site.register(DescuentoMO, DescuentoMOAdmin)
admin.site.register(FormaDePago, FormaDePagoAdmin)
admin.site.register(TipoClienteRecambios, TipoClienteRecambiosAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(NumeracionAutomatica, NumeracionAutomaticaAdmin)
admin.site.register(UnidadMedida, UnidadMedidaAdmin)
admin.site.register(CodigoAproPieza, CodigoAproPiezaAdmin)
admin.site.register(CodigoIva, CodigoIvaAdmin)





