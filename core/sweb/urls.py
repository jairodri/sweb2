from django.urls import path
from core.sweb.views.formasdepago.views import *
from core.sweb.views.dashboard.views import *
from core.sweb.views.tiposclienterec.views import *
from core.sweb.views.descuentosmo.views import *
from core.sweb.views.bancos.views import *
from core.sweb.views.clientes.views import *
from core.sweb.views.numeracionauto.views import *
from core.sweb.views.unidadesmedida.views import *
from core.sweb.views.codapropza.views import *
from core.sweb.views.codigosiva.views import *
from core.sweb.views.familiapieza.views import *
from core.sweb.views.marcas.views import *
from core.sweb.views.codigocontable.views import *
from core.sweb.views.modvehpieza.views import *
from core.sweb.views.fmarketing.views import *
from core.sweb.views.descuentosrec.views import *
from core.sweb.views.precios.views import *
from core.sweb.views.articulos.views import *
from core.sweb.views.codigotasa.views import *
from core.sweb.views.tasaneum.views import *
from core.sweb.views.gamas.views import *
from core.sweb.views.modelos.views import *
from core.sweb.views.concesionarios.views import *
from core.sweb.views.vehiculos.views import *
from core.sweb.views.tiposor.views import *
from core.sweb.views.catoper.views import *
from core.sweb.views.opetaller.views import *
from core.sweb.views.seccionint.views import *
from core.sweb.views.depositos.views import *
from core.sweb.views.ampaga.views import *
from core.sweb.views.secciontra.views import *
from core.sweb.views.situacionveh.views import *
from core.sweb.views.baremo.views import *
from core.sweb.views.linbaremo.views import *

app_name = 'sweb'

urlpatterns = [
    # Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', DashboardView.as_view(), name='index'),

    # Formas de Pago
    path(f'{FormaDePagoListView.folder}/list/', FormaDePagoListView.as_view(), name=f'{FormaDePagoListView.folder}_list'),
    path(f'{FormaDePagoCreateView.folder}/add/', FormaDePagoCreateView.as_view(), name=f'{FormaDePagoCreateView.folder}_add'),
    path(f'{FormaDePagoUpdateView.folder}/edit/<int:pk>/', FormaDePagoUpdateView.as_view(), name=f'{FormaDePagoUpdateView.folder}_edit'),
    path(f'{FormaDePagoDeleteView.folder}/delete/<int:pk>/', FormaDePagoDeleteView.as_view(), name=f'{FormaDePagoDeleteView.folder}_delete'),

    # Tipos de Cliente de Recambios
    path(f'{TipoClienteRecambiosListView.folder}/list/', TipoClienteRecambiosListView.as_view(), name=f'{TipoClienteRecambiosListView.folder}_list'),
    path(f'{TipoClienteRecambiosCreateView.folder}/add/', TipoClienteRecambiosCreateView.as_view(), name=f'{TipoClienteRecambiosCreateView.folder}_add'),
    path(f'{TipoClienteRecambiosUpdateView.folder}/edit/<int:pk>/', TipoClienteRecambiosUpdateView.as_view(), name=f'{TipoClienteRecambiosUpdateView.folder}_edit'),
    path(f'{TipoClienteRecambiosDeleteView.folder}/delete/<int:pk>/', TipoClienteRecambiosDeleteView.as_view(), name=f'{TipoClienteRecambiosDeleteView.folder}_delete'),

    # Descuentos MO
    path(f'{DescuentoMOListView.folder}/list/', DescuentoMOListView.as_view(), name=f'{DescuentoMOListView.folder}_list'),
    path(f'{DescuentoMOCreateView.folder}/add/', DescuentoMOCreateView.as_view(), name=f'{DescuentoMOCreateView.folder}_add'),
    path(f'{DescuentoMOUpdateView.folder}/edit/<int:pk>/', DescuentoMOUpdateView.as_view(), name=f'{DescuentoMOUpdateView.folder}_edit'),
    path(f'{DescuentoMODeleteView.folder}/delete/<int:pk>/', DescuentoMODeleteView.as_view(), name=f'{DescuentoMODeleteView.folder}_delete'),

    # Bancos
    path(f'{BancoListView.folder}/list/', BancoListView.as_view(), name=f'{BancoListView.folder}_list'),
    path(f'{BancoCreateView.folder}/add/', BancoCreateView.as_view(), name=f'{BancoCreateView.folder}_add'),
    path(f'{BancoUpdateView.folder}/edit/<int:pk>/', BancoUpdateView.as_view(), name=f'{BancoUpdateView.folder}_edit'),
    path(f'{BancoDeleteView.folder}/delete/<int:pk>/', BancoDeleteView.as_view(), name=f'{BancoDeleteView.folder}_delete'),
    path(f'{BancoDetailView.folder}/detail/<int:pk>/', BancoDetailView.as_view(), name=f'{BancoDetailView.folder}_detail'),

    # Clientes
    path(f'{ClienteListView.folder}/list/', ClienteListView.as_view(), name=f'{ClienteListView.folder}_list'),
    path(f'{ClienteCreateView.folder}/add/', ClienteCreateView.as_view(), name=f'{ClienteCreateView.folder}_add'),
    path(f'{ClienteUpdateView.folder}/edit/<int:pk>/', ClienteUpdateView.as_view(), name=f'{ClienteUpdateView.folder}_edit'),
    path(f'{ClienteDeleteView.folder}/delete/<int:pk>/', ClienteDeleteView.as_view(), name=f'{ClienteDeleteView.folder}_delete'),
    path(f'{ClienteDetailView.folder}/detail/<int:pk>/', ClienteDetailView.as_view(), name=f'{ClienteDetailView.folder}_detail'),

    # Importar
    # path('administrador/importar/', ImportarView.as_view(), name='administrador_importar'),

    # Numeración Automática
    path(f'{NumeracionAutomaticaListView.folder}/list/', NumeracionAutomaticaListView.as_view(), name=f'{NumeracionAutomaticaListView.folder}_list'),
    path(f'{NumeracionAutomaticaCreateView.folder}/add/', NumeracionAutomaticaCreateView.as_view(), name=f'{NumeracionAutomaticaCreateView.folder}_add'),
    path(f'{NumeracionAutomaticaUpdateView.folder}/edit/<int:pk>/', NumeracionAutomaticaUpdateView.as_view(), name=f'{NumeracionAutomaticaUpdateView.folder}_edit'),
    path(f'{NumeracionAutomaticaDeleteView.folder}/delete/<int:pk>/', NumeracionAutomaticaDeleteView.as_view(), name=f'{NumeracionAutomaticaDeleteView.folder}_delete'),

    # Unidades de Medida
    path(f'{UnidadMedidaListView.folder}/list/', UnidadMedidaListView.as_view(), name=f'{UnidadMedidaListView.folder}_list'),
    path(f'{UnidadMedidaCreateView.folder}/add/', UnidadMedidaCreateView.as_view(), name=f'{UnidadMedidaCreateView.folder}_add'),
    path(f'{UnidadMedidaUpdateView.folder}/edit/<int:pk>/', UnidadMedidaUpdateView.as_view(), name=f'{UnidadMedidaUpdateView.folder}_edit'),
    path(f'{UnidadMedidaDeleteView.folder}/delete/<int:pk>/', UnidadMedidaDeleteView.as_view(), name=f'{UnidadMedidaDeleteView.folder}_delete'),

    # Códigos Aprovisioanmiento Piezas
    path(f'{CodigoAproPiezaListView.folder}/list/', CodigoAproPiezaListView.as_view(), name=f'{CodigoAproPiezaListView.folder}_list'),
    path(f'{CodigoAproPiezaCreateView.folder}/add/', CodigoAproPiezaCreateView.as_view(), name=f'{CodigoAproPiezaCreateView.folder}_add'),
    path(f'{CodigoAproPiezaUpdateView.folder}/edit/<int:pk>/', CodigoAproPiezaUpdateView.as_view(), name=f'{CodigoAproPiezaUpdateView.folder}_edit'),
    path(f'{CodigoAproPiezaDeleteView.folder}/delete/<int:pk>/', CodigoAproPiezaDeleteView.as_view(), name=f'{CodigoAproPiezaDeleteView.folder}_delete'),

    # Códigos IVA
    path(f'{CodigoIvaListView.folder}/list/', CodigoIvaListView.as_view(), name=f'{CodigoIvaListView.folder}_list'),
    path(f'{CodigoIvaCreateView.folder}/add/', CodigoIvaCreateView.as_view(), name=f'{CodigoIvaCreateView.folder}_add'),
    path(f'{CodigoIvaUpdateView.folder}/edit/<int:pk>/', CodigoIvaUpdateView.as_view(), name=f'{CodigoIvaUpdateView.folder}_edit'),
    path(f'{CodigoIvaDeleteView.folder}/delete/<int:pk>/', CodigoIvaDeleteView.as_view(), name=f'{CodigoIvaDeleteView.folder}_delete'),

    # Familias Piezas
    path(f'{FamiliaPiezaListView.folder}/list/', FamiliaPiezaListView.as_view(), name=f'{FamiliaPiezaListView.folder}_list'),
    path(f'{FamiliaPiezaCreateView.folder}/add/', FamiliaPiezaCreateView.as_view(), name=f'{FamiliaPiezaCreateView.folder}_add'),
    path(f'{FamiliaPiezaUpdateView.folder}/edit/<int:pk>/', FamiliaPiezaUpdateView.as_view(), name=f'{FamiliaPiezaUpdateView.folder}_edit'),
    path(f'{FamiliaPiezaDeleteView.folder}/delete/<int:pk>/', FamiliaPiezaDeleteView.as_view(), name=f'{FamiliaPiezaDeleteView.folder}_delete'),

    # Marcas
    path(f'{MarcaListView.folder}/list/', MarcaListView.as_view(), name=f'{MarcaListView.folder}_list'),
    path(f'{MarcaCreateView.folder}/add/', MarcaCreateView.as_view(), name=f'{MarcaCreateView.folder}_add'),
    path(f'{MarcaUpdateView.folder}/edit/<int:pk>/', MarcaUpdateView.as_view(), name=f'{MarcaUpdateView.folder}_edit'),
    path(f'{MarcaDeleteView.folder}/delete/<int:pk>/', MarcaDeleteView.as_view(), name=f'{MarcaDeleteView.folder}_delete'),

    # Códigos Contables
    path(f'{CodigoContableListView.folder}/list/', CodigoContableListView.as_view(), name=f'{CodigoContableListView.folder}_list'),
    path(f'{CodigoContableCreateView.folder}/add/', CodigoContableCreateView.as_view(), name=f'{CodigoContableCreateView.folder}_add'),
    path(f'{CodigoContableUpdateView.folder}/edit/<int:pk>/', CodigoContableUpdateView.as_view(), name=f'{CodigoContableUpdateView.folder}_edit'),
    path(f'{CodigoContableDeleteView.folder}/delete/<int:pk>/', CodigoContableDeleteView.as_view(), name=f'{CodigoContableDeleteView.folder}_delete'),

    # Modelos Vehículos Piezas
    path(f'{ModeloVehPiezaListView.folder}/list/', ModeloVehPiezaListView.as_view(), name=f'{ModeloVehPiezaListView.folder}_list'),
    path(f'{ModeloVehPiezaCreateView.folder}/add/', ModeloVehPiezaCreateView.as_view(), name=f'{ModeloVehPiezaCreateView.folder}_add'),
    path(f'{ModeloVehPiezaUpdateView.folder}/edit/<int:pk>/', ModeloVehPiezaUpdateView.as_view(), name=f'{ModeloVehPiezaUpdateView.folder}_edit'),
    path(f'{ModeloVehPiezaDeleteView.folder}/delete/<int:pk>/', ModeloVehPiezaDeleteView.as_view(), name=f'{ModeloVehPiezaDeleteView.folder}_delete'),

    # Familias Marketing
    path(f'{FamiliaMarketingListView.folder}/list/', FamiliaMarketingListView.as_view(), name=f'{FamiliaMarketingListView.folder}_list'),
    path(f'{FamiliaMarketingCreateView.folder}/add/', FamiliaMarketingCreateView.as_view(), name=f'{FamiliaMarketingCreateView.folder}_add'),
    path(f'{FamiliaMarketingUpdateView.folder}/edit/<int:pk>/', FamiliaMarketingUpdateView.as_view(), name=f'{FamiliaMarketingUpdateView.folder}_edit'),
    path(f'{FamiliaMarketingDeleteView.folder}/delete/<int:pk>/', FamiliaMarketingDeleteView.as_view(), name=f'{FamiliaMarketingDeleteView.folder}_delete'),

    # Descuentos Pedidos Aprovisionamiento
    path(f'{DescuentoRecambiosPedidosAproListView.folder}/{DescuentoRecambiosPedidosAproListView.subfolder}/list/',
         DescuentoRecambiosPedidosAproListView.as_view(),
         name=f'{DescuentoRecambiosPedidosAproListView.subfolder}_list'),
    path(f'{DescuentoRecambiosPedidosAproCreateView.folder}/{DescuentoRecambiosPedidosAproCreateView.subfolder}/add/',
         DescuentoRecambiosPedidosAproCreateView.as_view(),
         name=f'{DescuentoRecambiosPedidosAproCreateView.subfolder}_add'),
    path(
        f'{DescuentoRecambiosPedidosAproUpdateView.folder}/{DescuentoRecambiosPedidosAproUpdateView.subfolder}/edit/<int:pk>/',
        DescuentoRecambiosPedidosAproUpdateView.as_view(),
        name=f'{DescuentoRecambiosPedidosAproUpdateView.subfolder}_edit'),
    path(
        f'{DescuentoRecambiosPedidosAproDeleteView.folder}/{DescuentoRecambiosPedidosAproDeleteView.subfolder}/delete/<int:pk>/',
        DescuentoRecambiosPedidosAproDeleteView.as_view(),
        name=f'{DescuentoRecambiosPedidosAproDeleteView.subfolder}_delete'),

    # Descuentos Ventas
    path(f'{DescuentoRecambiosVentasListView.folder}/{DescuentoRecambiosVentasListView.subfolder}/list/',
         DescuentoRecambiosVentasListView.as_view(), name=f'{DescuentoRecambiosVentasListView.subfolder}_list'),
    path(f'{DescuentoRecambiosVentasCreateView.folder}/{DescuentoRecambiosVentasCreateView.subfolder}/add/',
         DescuentoRecambiosVentasCreateView.as_view(), name=f'{DescuentoRecambiosVentasCreateView.subfolder}_add'),
    path(f'{DescuentoRecambiosVentasUpdateView.folder}/{DescuentoRecambiosVentasUpdateView.subfolder}/edit/<int:pk>/',
         DescuentoRecambiosVentasUpdateView.as_view(), name=f'{DescuentoRecambiosVentasUpdateView.subfolder}_edit'),
    path(f'{DescuentoRecambiosVentasDeleteView.folder}/{DescuentoRecambiosVentasDeleteView.subfolder}/delete/<int:pk>/',
         DescuentoRecambiosVentasDeleteView.as_view(), name=f'{DescuentoRecambiosVentasDeleteView.subfolder}_delete'),

    # Descuentos Pedidos Urgentes
    path(f'{DescuentoRecambiosPedidosUrgtesListView.folder}/{DescuentoRecambiosPedidosUrgtesListView.subfolder}/list/',
         DescuentoRecambiosPedidosUrgtesListView.as_view(),
         name=f'{DescuentoRecambiosPedidosUrgtesListView.subfolder}_list'),
    path(
        f'{DescuentoRecambiosPedidosUrgtesCreateView.folder}/{DescuentoRecambiosPedidosUrgtesCreateView.subfolder}/add/',
        DescuentoRecambiosPedidosUrgtesCreateView.as_view(),
        name=f'{DescuentoRecambiosPedidosUrgtesCreateView.subfolder}_add'),
    path(
        f'{DescuentoRecambiosPedidosUrgtesUpdateView.folder}/{DescuentoRecambiosPedidosUrgtesUpdateView.subfolder}/edit/<int:pk>/',
        DescuentoRecambiosPedidosUrgtesUpdateView.as_view(),
        name=f'{DescuentoRecambiosPedidosUrgtesUpdateView.subfolder}_edit'),
    path(
        f'{DescuentoRecambiosPedidosUrgtesDeleteView.folder}/{DescuentoRecambiosPedidosUrgtesDeleteView.subfolder}/delete/<int:pk>/',
        DescuentoRecambiosPedidosUrgtesDeleteView.as_view(),
        name=f'{DescuentoRecambiosPedidosUrgtesDeleteView.subfolder}_delete'),

    # Descuentos Pedidos Campaña
    path(f'{DescuentoRecambiosPedidosCampnaListView.folder}/{DescuentoRecambiosPedidosCampnaListView.subfolder}/list/',
         DescuentoRecambiosPedidosCampnaListView.as_view(),
         name=f'{DescuentoRecambiosPedidosCampnaListView.subfolder}_list'),
    path(
        f'{DescuentoRecambiosPedidosCampnaCreateView.folder}/{DescuentoRecambiosPedidosCampnaCreateView.subfolder}/add/',
        DescuentoRecambiosPedidosCampnaCreateView.as_view(),
        name=f'{DescuentoRecambiosPedidosCampnaCreateView.subfolder}_add'),
    path(
        f'{DescuentoRecambiosPedidosCampnaUpdateView.folder}/{DescuentoRecambiosPedidosCampnaUpdateView.subfolder}/edit/<int:pk>/',
        DescuentoRecambiosPedidosCampnaUpdateView.as_view(),
        name=f'{DescuentoRecambiosPedidosCampnaUpdateView.subfolder}_edit'),
    path(
        f'{DescuentoRecambiosPedidosCampnaDeleteView.folder}/{DescuentoRecambiosPedidosCampnaDeleteView.subfolder}/delete/<int:pk>/',
        DescuentoRecambiosPedidosCampnaDeleteView.as_view(),
        name=f'{DescuentoRecambiosPedidosCampnaDeleteView.subfolder}_delete'),

    # Descuentos Ventas Campaña
    path(f'{DescuentoRecambiosVentasCampnaListView.folder}/{DescuentoRecambiosVentasCampnaListView.subfolder}/list/',
         DescuentoRecambiosVentasCampnaListView.as_view(),
         name=f'{DescuentoRecambiosVentasCampnaListView.subfolder}_list'),
    path(f'{DescuentoRecambiosVentasCampnaCreateView.folder}/{DescuentoRecambiosVentasCampnaCreateView.subfolder}/add/',
         DescuentoRecambiosVentasCampnaCreateView.as_view(),
         name=f'{DescuentoRecambiosVentasCampnaCreateView.subfolder}_add'),
    path(
        f'{DescuentoRecambiosVentasCampnaUpdateView.folder}/{DescuentoRecambiosVentasCampnaUpdateView.subfolder}/edit/<int:pk>/',
        DescuentoRecambiosVentasCampnaUpdateView.as_view(),
        name=f'{DescuentoRecambiosVentasCampnaUpdateView.subfolder}_edit'),
    path(
        f'{DescuentoRecambiosVentasCampnaDeleteView.folder}/{DescuentoRecambiosVentasCampnaDeleteView.subfolder}/delete/<int:pk>/',
        DescuentoRecambiosVentasCampnaDeleteView.as_view(),
        name=f'{DescuentoRecambiosVentasCampnaDeleteView.subfolder}_delete'),

    # Descuentos Piezas Garantías
    path(
        f'{DescuentoRecambiosPiezasGarantiaListView.folder}/{DescuentoRecambiosPiezasGarantiaListView.subfolder}/list/',
        DescuentoRecambiosPiezasGarantiaListView.as_view(),
        name=f'{DescuentoRecambiosPiezasGarantiaListView.subfolder}_list'),
    path(
        f'{DescuentoRecambiosPiezasGarantiaCreateView.folder}/{DescuentoRecambiosPiezasGarantiaCreateView.subfolder}/add/',
        DescuentoRecambiosPiezasGarantiaCreateView.as_view(),
        name=f'{DescuentoRecambiosPiezasGarantiaCreateView.subfolder}_add'),
    path(
        f'{DescuentoRecambiosPiezasGarantiaUpdateView.folder}/{DescuentoRecambiosPiezasGarantiaUpdateView.subfolder}/edit/<int:pk>/',
        DescuentoRecambiosPiezasGarantiaUpdateView.as_view(),
        name=f'{DescuentoRecambiosPiezasGarantiaUpdateView.subfolder}_edit'),
    path(
        f'{DescuentoRecambiosPiezasGarantiaDeleteView.folder}/{DescuentoRecambiosPiezasGarantiaDeleteView.subfolder}/delete/<int:pk>/',
        DescuentoRecambiosPiezasGarantiaDeleteView.as_view(),
        name=f'{DescuentoRecambiosPiezasGarantiaDeleteView.subfolder}_delete'),

    # Lista de Precios
    path(f'{PrecioTarifaListView.folder}/list/', PrecioTarifaListView.as_view(), name=f'{PrecioTarifaListView.folder}_list'),

    # Artículos
    path(f'{ArticuloListView.folder}/list/', ArticuloListView.as_view(), name=f'{ArticuloListView.folder}_list'),
    path(f'{ArticuloCreateView.folder}/add/', ArticuloCreateView.as_view(), name=f'{ArticuloCreateView.folder}_add'),
    path(f'{ArticuloUpdateView.folder}/edit/<int:pk>/', ArticuloUpdateView.as_view(), name=f'{ArticuloUpdateView.folder}_edit'),
    path(f'{ArticuloDeleteView.folder}/delete/<int:pk>/', ArticuloDeleteView.as_view(), name=f'{ArticuloDeleteView.folder}_delete'),
    path(f'{ArticuloDetailView.folder}/detail/<int:pk>/', ArticuloDetailView.as_view(), name=f'{ArticuloDetailView.folder}_detail'),
    path(f'{ArticuloInformeTasasView.folder}/itasas/', ArticuloInformeTasasView.as_view(), name=f'{ArticuloInformeTasasView.folder}_itasas'),

    # Códigos de Tasa
    path(f'{TasaCodigoListView.folder}/list/', TasaCodigoListView.as_view(), name=f'{TasaCodigoListView.folder}_list'),
    path(f'{TasaCodigoCreateView.folder}/add/', TasaCodigoCreateView.as_view(), name=f'{TasaCodigoCreateView.folder}_add'),
    path(f'{TasaCodigoUpdateView.folder}/edit/<int:pk>/', TasaCodigoUpdateView.as_view(), name=f'{TasaCodigoUpdateView.folder}_edit'),
    path(f'{TasaCodigoDeleteView.folder}/delete/<int:pk>/', TasaCodigoDeleteView.as_view(), name=f'{TasaCodigoDeleteView.folder}_delete'),

    # Tasa Neumático
    path(f'{TasaNeumaticoListView.folder}/list/', TasaNeumaticoListView.as_view(), name=f'{TasaNeumaticoListView.folder}_list'),
    path(f'{TasaNeumaticoCreateView.folder}/add/', TasaNeumaticoCreateView.as_view(), name=f'{TasaNeumaticoCreateView.folder}_add'),
    path(f'{TasaNeumaticoUpdateView.folder}/edit/<int:pk>/', TasaNeumaticoUpdateView.as_view(), name=f'{TasaNeumaticoUpdateView.folder}_edit'),
    path(f'{TasaNeumaticoDeleteView.folder}/delete/<int:pk>/', TasaNeumaticoDeleteView.as_view(), name=f'{TasaNeumaticoDeleteView.folder}_delete'),

    # Gamas
    path(f'{GamaListView.folder}/list/', GamaListView.as_view(), name=f'{GamaListView.folder}_list'),
    path(f'{GamaCreateView.folder}/add/', GamaCreateView.as_view(), name=f'{GamaCreateView.folder}_add'),
    path(f'{GamaUpdateView.folder}/edit/<int:pk>/', GamaUpdateView.as_view(), name=f'{GamaUpdateView.folder}_edit'),
    path(f'{GamaDeleteView.folder}/delete/<int:pk>/', GamaDeleteView.as_view(), name=f'{GamaDeleteView.folder}_delete'),

    # Modelos
    path(f'{ModeloListView.folder}/list/', ModeloListView.as_view(), name=f'{ModeloListView.folder}_list'),
    path(f'{ModeloCreateView.folder}/add/', ModeloCreateView.as_view(), name=f'{ModeloCreateView.folder}_add'),
    path(f'{ModeloUpdateView.folder}/edit/<int:pk>/', ModeloUpdateView.as_view(), name=f'{ModeloUpdateView.folder}_edit'),
    path(f'{ModeloDeleteView.folder}/delete/<int:pk>/', ModeloDeleteView.as_view(), name=f'{ModeloDeleteView.folder}_delete'),

    # Concesionarios
    path(f'{ConcesionarioListView.folder}/list/', ConcesionarioListView.as_view(), name=f'{ConcesionarioListView.folder}_list'),
    path(f'{ConcesionarioCreateView.folder}/add/', ConcesionarioCreateView.as_view(), name=f'{ConcesionarioCreateView.folder}_add'),
    path(f'{ConcesionarioUpdateView.folder}/edit/<int:pk>/', ConcesionarioUpdateView.as_view(), name=f'{ConcesionarioUpdateView.folder}_edit'),
    path(f'{ConcesionarioDeleteView.folder}/delete/<int:pk>/', ConcesionarioDeleteView.as_view(), name=f'{ConcesionarioDeleteView.folder}_delete'),

    # Vehículos
    path(f'{VehiculoListView.folder}/list/', VehiculoListView.as_view(), name=f'{VehiculoListView.folder}_list'),
    path(f'{VehiculoCreateView.folder}/add/', VehiculoCreateView.as_view(), name=f'{VehiculoCreateView.folder}_add'),
    path(f'{VehiculoUpdateView.folder}/edit/<int:pk>/', VehiculoUpdateView.as_view(), name=f'{VehiculoUpdateView.folder}_edit'),
    path(f'{VehiculoDeleteView.folder}/delete/<int:pk>/', VehiculoDeleteView.as_view(), name=f'{VehiculoDeleteView.folder}_delete'),
    path(f'{VehiculoDetailView.folder}/detail/<int:pk>/', VehiculoDetailView.as_view(), name=f'{VehiculoDetailView.folder}_detail'),

    # Tipos de Órdenes de Reparación
    path(f'{TipoOrdenReparacionListView.folder}/list/', TipoOrdenReparacionListView.as_view(), name=f'{TipoOrdenReparacionListView.folder}_list'),
    path(f'{TipoOrdenReparacionCreateView.folder}/add/', TipoOrdenReparacionCreateView.as_view(), name=f'{TipoOrdenReparacionCreateView.folder}_add'),
    path(f'{TipoOrdenReparacionUpdateView.folder}/edit/<int:pk>/', TipoOrdenReparacionUpdateView.as_view(), name=f'{TipoOrdenReparacionUpdateView.folder}_edit'),
    path(f'{TipoOrdenReparacionDeleteView.folder}/delete/<int:pk>/', TipoOrdenReparacionDeleteView.as_view(), name=f'{TipoOrdenReparacionDeleteView.folder}_delete'),

    # Categorías de Operarios
    path(f'{CategoriaOperarioListView.folder}/list/', CategoriaOperarioListView.as_view(), name=f'{CategoriaOperarioListView.folder}_list'),
    path(f'{CategoriaOperarioCreateView.folder}/add/', CategoriaOperarioCreateView.as_view(), name=f'{CategoriaOperarioCreateView.folder}_add'),
    path(f'{CategoriaOperarioUpdateView.folder}/edit/<int:pk>/', CategoriaOperarioUpdateView.as_view(), name=f'{CategoriaOperarioUpdateView.folder}_edit'),
    path(f'{CategoriaOperarioDeleteView.folder}/delete/<int:pk>/', CategoriaOperarioDeleteView.as_view(), name=f'{CategoriaOperarioDeleteView.folder}_delete'),

    # Operarios Taller
    path(f'{OperarioListView.folder}/list/', OperarioListView.as_view(), name=f'{OperarioListView.folder}_list'),
    path(f'{OperarioCreateView.folder}/add/', OperarioCreateView.as_view(), name=f'{OperarioCreateView.folder}_add'),
    path(f'{OperarioUpdateView.folder}/edit/<int:pk>/', OperarioUpdateView.as_view(), name=f'{OperarioUpdateView.folder}_edit'),
    path(f'{OperarioDeleteView.folder}/delete/<int:pk>/', OperarioDeleteView.as_view(), name=f'{OperarioDeleteView.folder}_delete'),
    path(f'{OperarioDetailView.folder}/detail/<int:pk>/', OperarioDetailView.as_view(), name=f'{OperarioDetailView.folder}_detail'),

    # Secciones Internas
    path(f'{SeccionInternaListView.folder}/list/', SeccionInternaListView.as_view(), name=f'{SeccionInternaListView.folder}_list'),
    path(f'{SeccionInternaCreateView.folder}/add/', SeccionInternaCreateView.as_view(), name=f'{SeccionInternaCreateView.folder}_add'),
    path(f'{SeccionInternaUpdateView.folder}/edit/<int:pk>/', SeccionInternaUpdateView.as_view(), name=f'{SeccionInternaUpdateView.folder}_edit'),
    path(f'{SeccionInternaDeleteView.folder}/delete/<int:pk>/', SeccionInternaDeleteView.as_view(), name=f'{SeccionInternaDeleteView.folder}_delete'),

    # Capacidad Depósito
    path(f'{CapacidadDepositoListView.folder}/list/', CapacidadDepositoListView.as_view(), name=f'{CapacidadDepositoListView.folder}_list'),
    path(f'{CapacidadDepositoCreateView.folder}/add/', CapacidadDepositoCreateView.as_view(), name=f'{CapacidadDepositoCreateView.folder}_add'),
    path(f'{CapacidadDepositoUpdateView.folder}/edit/<int:pk>/', CapacidadDepositoUpdateView.as_view(), name=f'{CapacidadDepositoUpdateView.folder}_edit'),
    path(f'{CapacidadDepositoDeleteView.folder}/delete/<int:pk>/', CapacidadDepositoDeleteView.as_view(), name=f'{CapacidadDepositoDeleteView.folder}_delete'),

    # Ampliaciones de Garantía
    path(f'{AmpliacionGarantiaListView.folder}/list/', AmpliacionGarantiaListView.as_view(), name=f'{AmpliacionGarantiaListView.folder}_list'),
    path(f'{AmpliacionGarantiaCreateView.folder}/add/', AmpliacionGarantiaCreateView.as_view(), name=f'{AmpliacionGarantiaCreateView.folder}_add'),
    path(f'{AmpliacionGarantiaUpdateView.folder}/edit/<int:pk>/', AmpliacionGarantiaUpdateView.as_view(), name=f'{AmpliacionGarantiaUpdateView.folder}_edit'),
    path(f'{AmpliacionGarantiaDeleteView.folder}/delete/<int:pk>/', AmpliacionGarantiaDeleteView.as_view(), name=f'{AmpliacionGarantiaDeleteView.folder}_delete'),

    # Secciones de Trabajo
    path(f'{SeccionTrabajoListView.folder}/list/', SeccionTrabajoListView.as_view(), name=f'{SeccionTrabajoListView.folder}_list'),
    path(f'{SeccionTrabajoCreateView.folder}/add/', SeccionTrabajoCreateView.as_view(), name=f'{SeccionTrabajoCreateView.folder}_add'),
    path(f'{SeccionTrabajoUpdateView.folder}/edit/<int:pk>/', SeccionTrabajoUpdateView.as_view(), name=f'{SeccionTrabajoUpdateView.folder}_edit'),
    path(f'{SeccionTrabajoDeleteView.folder}/delete/<int:pk>/', SeccionTrabajoDeleteView.as_view(), name=f'{SeccionTrabajoDeleteView.folder}_delete'),

    # Situaciones Vehículo Taller
    path(f'{SituacionVehiculoListView.folder}/list/', SituacionVehiculoListView.as_view(), name=f'{SituacionVehiculoListView.folder}_list'),
    path(f'{SituacionVehiculoCreateView.folder}/add/', SituacionVehiculoCreateView.as_view(), name=f'{SituacionVehiculoCreateView.folder}_add'),
    path(f'{SituacionVehiculoUpdateView.folder}/edit/<int:pk>/', SituacionVehiculoUpdateView.as_view(), name=f'{SituacionVehiculoUpdateView.folder}_edit'),
    path(f'{SituacionVehiculoDeleteView.folder}/delete/<int:pk>/', SituacionVehiculoDeleteView.as_view(), name=f'{SituacionVehiculoDeleteView.folder}_delete'),

    # Baremo
    path(f'{BaremoListView.folder}/list/', BaremoListView.as_view(), name=f'{BaremoListView.folder}_list'),
    path(f'{BaremoCreateView.folder}/add/', BaremoCreateView.as_view(), name=f'{BaremoCreateView.folder}_add'),
    path(f'{BaremoUpdateView.folder}/edit/<int:pk>/', BaremoUpdateView.as_view(), name=f'{BaremoUpdateView.folder}_edit'),
    path(f'{BaremoDeleteView.folder}/delete/<int:pk>/', BaremoDeleteView.as_view(), name=f'{BaremoDeleteView.folder}_delete'),
    path(f'{BaremoDetailView.folder}/detail/<int:pk>/', BaremoDetailView.as_view(), name=f'{BaremoDetailView.folder}_detail'),

    # Líneas Baremo
    path(f'{BaremoUpdateView.folder}/edit/<int:pk>/{LineaBaremoCreateView.folder}/add/', LineaBaremoCreateView.as_view(), name=f'{LineaBaremoCreateView.folder}_add'),
    path(f'{BaremoUpdateView.folder}/edit/<int:pk0>/{LineaBaremoUpdateView.folder}/edit/<int:pk>/', LineaBaremoUpdateView.as_view(), name=f'{LineaBaremoUpdateView.folder}_edit'),
    path(f'{BaremoUpdateView.folder}/edit/<int:pk0>/{LineaBaremoDeleteView.folder}/delete/<int:pk>/', LineaBaremoDeleteView.as_view(), name=f'{LineaBaremoDeleteView.folder}_delete'),
]
