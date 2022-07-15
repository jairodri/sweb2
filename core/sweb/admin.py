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


class FamiliaPiezaAdmin(ImportExportModelAdmin):
    resource_class = FamiliaPiezaResource


class MarcaAdmin(ImportExportModelAdmin):
    resource_class = MarcaResource


class CodigoContableAdmin(ImportExportModelAdmin):
    resource_class = CodigoContableResource


class ModeloVehPiezaAdmin(ImportExportModelAdmin):
    resource_class = ModeloVehPiezaResource


class FamiliaMarketingAdmin(ImportExportModelAdmin):
    resource_class = FamiliaMarketingResource


class DescuentoRecambiosAdmin(ImportExportModelAdmin):
    resource_class = DescuentoRecambiosResource


class PrecioTarifaAdmin(ImportExportModelAdmin):
    resource_class = PrecioTarifaResource


class ArticuloAdmin(ImportExportModelAdmin):
    resource_class = ArticuloResource


class TasaAdmin(ImportExportModelAdmin):
    resource_class = TasaResource


class TasaNeumaticoAdmin(ImportExportModelAdmin):
    resource_class = TasaNeumaticoResource


class GamaAdmin(ImportExportModelAdmin):
    resource_class = GamaResource


class ModeloAdmin(ImportExportModelAdmin):
    resource_class = ModeloResource


class ConcesionarioAdmin(ImportExportModelAdmin):
    resource_class = ConcesionarioResource


class VehiculoAdmin(ImportExportModelAdmin):
    resource_class = VehiculoResource


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
admin.site.register(FamiliaPieza, FamiliaPiezaAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(CodigoContable, CodigoContableAdmin)
admin.site.register(ModeloVehPieza, ModeloVehPiezaAdmin)
admin.site.register(FamiliaMarketing, FamiliaMarketingAdmin)
admin.site.register(DescuentoRecambios, DescuentoRecambiosAdmin)
admin.site.register(PrecioTarifa, PrecioTarifaAdmin)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Tasa, TasaAdmin)
admin.site.register(TasaCodigo)
admin.site.register(TasaNeumatico, TasaNeumaticoAdmin)
admin.site.register(Gama, GamaAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Concesionario, ConcesionarioAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)





