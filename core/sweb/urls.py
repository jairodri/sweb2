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

app_name = 'sweb'
folder_cpz = 'codapropza'
folder_tcr = 'tiposclienterec'
folder_dmo = 'descuentosmo'
folder_fpg = 'formasdepago'
folder_ban = 'bancos'
folder_cli = 'clientes'
folder_nau = 'numeracionauto'
folder_uni = 'unidadesmedida'
folder_iva = 'codigosiva'
folder_fpz = 'familiapieza'
folder_mca = 'marcas'
folder_ctb = 'codigocontable'
folder_mov = 'modvehpieza'
folder_fmk = 'fmarketing'

urlpath_dtr = 'descuentosrec'
urlpath_dtr_t0 = 'dtoventas'
urlpath_dtr_t1 = 'dtopedapro'
urlpath_dtr_t2 = 'dtopedurgte'
urlpath_dtr_t3 = 'dtopedcamp'
urlpath_dtr_t4 = 'dtovtacamp'
urlpath_dtr_t5 = 'dtopzagar'


urlpatterns = [
    # Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', DashboardView.as_view(), name='index'),

    # Formas de Pago
    path(f'{folder_fpg}/list/', FormaDePagoListView.as_view(), name=f'{folder_fpg}_list'),
    path(f'{folder_fpg}/add/', FormaDePagoCreateView.as_view(), name=f'{folder_fpg}_add'),
    path(f'{folder_fpg}/edit/<int:pk>/', FormaDePagoUpdateView.as_view(), name=f'{folder_fpg}_edit'),
    path(f'{folder_fpg}/delete/<int:pk>/', FormaDePagoDeleteView.as_view(), name=f'{folder_fpg}_delete'),

    # Tipos de Cliente de Recambios
    path(f'{folder_tcr}/list/', TipoClienteRecambiosListView.as_view(), name=f'{folder_tcr}_list'),
    path(f'{folder_tcr}/add/', TipoClienteRecambiosCreateView.as_view(), name=f'{folder_tcr}_add'),
    path(f'{folder_tcr}/edit/<int:pk>/', TipoClienteRecambiosUpdateView.as_view(), name=f'{folder_tcr}_edit'),
    path(f'{folder_tcr}/delete/<int:pk>/', TipoClienteRecambiosDeleteView.as_view(), name=f'{folder_tcr}_delete'),

    # Descuentos MO
    path(f'{folder_dmo}/list/', DescuentoMOListView.as_view(), name=f'{folder_dmo}_list'),
    path(f'{folder_dmo}/add/', DescuentoMOCreateView.as_view(), name=f'{folder_dmo}_add'),
    path(f'{folder_dmo}/edit/<int:pk>/', DescuentoMOUpdateView.as_view(), name=f'{folder_dmo}_edit'),
    path(f'{folder_dmo}/delete/<int:pk>/', DescuentoMODeleteView.as_view(), name=f'{folder_dmo}_delete'),

    # Bancos
    path(f'{folder_ban}/list/', BancoListView.as_view(), name=f'{folder_ban}_list'),
    path(f'{folder_ban}/add/', BancoCreateView.as_view(), name=f'{folder_ban}_add'),
    path(f'{folder_ban}/edit/<int:pk>/', BancoUpdateView.as_view(), name=f'{folder_ban}_edit'),
    path(f'{folder_ban}/delete/<int:pk>/', BancoDeleteView.as_view(), name=f'{folder_ban}_delete'),
    path(f'{folder_ban}/detail/<int:pk>/', BancoDetailView.as_view(), name=f'{folder_ban}_detail'),

    # Clientes
    path(f'{folder_cli}/list/', ClienteListView.as_view(), name=f'{folder_cli}_list'),
    path(f'{folder_cli}/add/', ClienteCreateView.as_view(), name=f'{folder_cli}_add'),
    path(f'{folder_cli}/edit/<int:pk>/', ClienteUpdateView.as_view(), name=f'{folder_cli}_edit'),
    path(f'{folder_cli}/delete/<int:pk>/', ClienteDeleteView.as_view(), name=f'{folder_cli}_delete'),
    path(f'{folder_cli}/detail/<int:pk>/', ClienteDetailView.as_view(), name=f'{folder_cli}_detail'),

    # Importar
    # path('administrador/importar/', ImportarView.as_view(), name='administrador_importar'),

    # Numeración Automática
    path(f'{folder_nau}/list/', NumeracionAutomaticaListView.as_view(), name=f'{folder_nau}_list'),
    path(f'{folder_nau}/add/', NumeracionAutomaticaCreateView.as_view(), name=f'{folder_nau}_add'),
    path(f'{folder_nau}/edit/<int:pk>/', NumeracionAutomaticaUpdateView.as_view(), name=f'{folder_nau}_edit'),
    path(f'{folder_nau}/delete/<int:pk>/', NumeracionAutomaticaDeleteView.as_view(), name=f'{folder_nau}_delete'),

    # Unidades de Medida
    path(f'{folder_uni}/list/', UnidadMedidaListView.as_view(), name=f'{folder_uni}_list'),
    path(f'{folder_uni}/add/', UnidadMedidaCreateView.as_view(), name=f'{folder_uni}_add'),
    path(f'{folder_uni}/edit/<int:pk>/', UnidadMedidaUpdateView.as_view(), name=f'{folder_uni}_edit'),
    path(f'{folder_uni}/delete/<int:pk>/', UnidadMedidaDeleteView.as_view(), name=f'{folder_uni}_delete'),

    # Códigos Aprovisioanmiento Piezas
    path(f'{folder_cpz}/list/', CodigoAproPiezaListView.as_view(), name=f'{folder_cpz}_list'),
    path(f'{folder_cpz}/add/', CodigoAproPiezaCreateView.as_view(), name=f'{folder_cpz}_add'),
    path(f'{folder_cpz}/edit/<int:pk>/', CodigoAproPiezaUpdateView.as_view(), name=f'{folder_cpz}_edit'),
    path(f'{folder_cpz}/delete/<int:pk>/', CodigoAproPiezaDeleteView.as_view(), name=f'{folder_cpz}_delete'),

    # Códigos IVA
    path(f'{folder_iva}/list/', CodigoIvaListView.as_view(), name=f'{folder_iva}_list'),
    path(f'{folder_iva}/add/', CodigoIvaCreateView.as_view(), name=f'{folder_iva}_add'),
    path(f'{folder_iva}/edit/<int:pk>/', CodigoIvaUpdateView.as_view(), name=f'{folder_iva}_edit'),
    path(f'{folder_iva}/delete/<int:pk>/', CodigoIvaDeleteView.as_view(), name=f'{folder_iva}_delete'),

    # Familias Piezas
    path(f'{folder_fpz}/list/', FamiliaPiezaListView.as_view(), name=f'{folder_fpz}_list'),
    path(f'{folder_fpz}/add/', FamiliaPiezaCreateView.as_view(), name=f'{folder_fpz}_add'),
    path(f'{folder_fpz}/edit/<int:pk>/', FamiliaPiezaUpdateView.as_view(), name=f'{folder_fpz}_edit'),
    path(f'{folder_fpz}/delete/<int:pk>/', FamiliaPiezaDeleteView.as_view(), name=f'{folder_fpz}_delete'),

    # Marcas
    path(f'{folder_mca}/list/', MarcaListView.as_view(), name=f'{folder_mca}_list'),
    path(f'{folder_mca}/add/', MarcaCreateView.as_view(), name=f'{folder_mca}_add'),
    path(f'{folder_mca}/edit/<int:pk>/', MarcaUpdateView.as_view(), name=f'{folder_mca}_edit'),
    path(f'{folder_mca}/delete/<int:pk>/', MarcaDeleteView.as_view(), name=f'{folder_mca}_delete'),

    # Códigos Contables
    path(f'{folder_ctb}/list/', CodigoContableListView.as_view(), name=f'{folder_ctb}_list'),
    path(f'{folder_ctb}/add/', CodigoContableCreateView.as_view(), name=f'{folder_ctb}_add'),
    path(f'{folder_ctb}/edit/<int:pk>/', CodigoContableUpdateView.as_view(), name=f'{folder_ctb}_edit'),
    path(f'{folder_ctb}/delete/<int:pk>/', CodigoContableDeleteView.as_view(), name=f'{folder_ctb}_delete'),

    # Modelos Vehículos Piezas
    path(f'{folder_mov}/list/', ModeloVehPiezaListView.as_view(), name=f'{folder_mov}_list'),
    path(f'{folder_mov}/add/', ModeloVehPiezaCreateView.as_view(), name=f'{folder_mov}_add'),
    path(f'{folder_mov}/edit/<int:pk>/', ModeloVehPiezaUpdateView.as_view(), name=f'{folder_mov}_edit'),
    path(f'{folder_mov}/delete/<int:pk>/', ModeloVehPiezaDeleteView.as_view(), name=f'{folder_mov}_delete'),

    # Familias Marketing
    path(f'{folder_fmk}/list/', FamiliaMarketingListView.as_view(), name=f'{folder_fmk}_list'),
    path(f'{folder_fmk}/add/', FamiliaMarketingCreateView.as_view(), name=f'{folder_fmk}_add'),
    path(f'{folder_fmk}/edit/<int:pk>/', FamiliaMarketingUpdateView.as_view(), name=f'{folder_fmk}_edit'),
    path(f'{folder_fmk}/delete/<int:pk>/', FamiliaMarketingDeleteView.as_view(), name=f'{folder_fmk}_delete'),

    # Descuentos Pedidos Aprovisionamiento
    path(f'{urlpath_dtr}/{urlpath_dtr_t1}/list/', DescuentoRecambiosPedidosAproListView.as_view(), name=f'{urlpath_dtr_t1}_list'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t1}/add/', DescuentoRecambiosPedidosAproCreateView.as_view(), name=f'{urlpath_dtr_t1}_add'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t1}/edit/<int:pk>/', DescuentoRecambiosPedidosAproUpdateView.as_view(), name=f'{urlpath_dtr_t1}_edit'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t1}/delete/<int:pk>/', DescuentoRecambiosPedidosAproDeleteView.as_view(), name=f'{urlpath_dtr_t1}_delete'),

    # Descuentos Ventas
    path(f'{urlpath_dtr}/{urlpath_dtr_t0}/list/', DescuentoRecambiosVentasListView.as_view(), name=f'{urlpath_dtr_t0}_list'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t0}/add/', DescuentoRecambiosVentasCreateView.as_view(), name=f'{urlpath_dtr_t0}_add'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t0}/edit/<int:pk>/', DescuentoRecambiosVentasUpdateView.as_view(), name=f'{urlpath_dtr_t0}_edit'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t0}/delete/<int:pk>/', DescuentoRecambiosVentasDeleteView.as_view(), name=f'{urlpath_dtr_t0}_delete'),

    # Descuentos Pedidos Urgentes
    path(f'{urlpath_dtr}/{urlpath_dtr_t2}/list/', DescuentoRecambiosPedidosUrgtesListView.as_view(), name=f'{urlpath_dtr_t2}_list'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t2}/add/', DescuentoRecambiosPedidosUrgtesCreateView.as_view(), name=f'{urlpath_dtr_t2}_add'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t2}/edit/<int:pk>/', DescuentoRecambiosPedidosUrgtesUpdateView.as_view(), name=f'{urlpath_dtr_t2}_edit'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t2}/delete/<int:pk>/', DescuentoRecambiosPedidosUrgtesDeleteView.as_view(), name=f'{urlpath_dtr_t2}_delete'),

    # Descuentos Pedidos Campaña
    path(f'{urlpath_dtr}/{urlpath_dtr_t3}/list/', DescuentoRecambiosPedidosCampnaListView.as_view(), name=f'{urlpath_dtr_t3}_list'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t3}/add/', DescuentoRecambiosPedidosCampnaCreateView.as_view(), name=f'{urlpath_dtr_t3}_add'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t3}/edit/<int:pk>/', DescuentoRecambiosPedidosCampnaUpdateView.as_view(), name=f'{urlpath_dtr_t3}_edit'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t3}/delete/<int:pk>/', DescuentoRecambiosPedidosCampnaDeleteView.as_view(), name=f'{urlpath_dtr_t3}_delete'),

    # Descuentos Ventas Campaña
    path(f'{urlpath_dtr}/{urlpath_dtr_t4}/list/', DescuentoRecambiosVentasCampnaListView.as_view(), name=f'{urlpath_dtr_t4}_list'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t4}/add/', DescuentoRecambiosVentasCampnaCreateView.as_view(), name=f'{urlpath_dtr_t4}_add'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t4}/edit/<int:pk>/', DescuentoRecambiosVentasCampnaUpdateView.as_view(), name=f'{urlpath_dtr_t4}_edit'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t4}/delete/<int:pk>/', DescuentoRecambiosVentasCampnaDeleteView.as_view(), name=f'{urlpath_dtr_t4}_delete'),

    # Descuentos Piezas Garantías
    path(f'{urlpath_dtr}/{urlpath_dtr_t5}/list/', DescuentoRecambiosPiezasGarantiaListView.as_view(), name=f'{urlpath_dtr_t5}_list'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t5}/add/', DescuentoRecambiosPiezasGarantiaCreateView.as_view(), name=f'{urlpath_dtr_t5}_add'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t5}/edit/<int:pk>/', DescuentoRecambiosPiezasGarantiaUpdateView.as_view(), name=f'{urlpath_dtr_t5}_edit'),
    path(f'{urlpath_dtr}/{urlpath_dtr_t5}/delete/<int:pk>/', DescuentoRecambiosPiezasGarantiaDeleteView.as_view(), name=f'{urlpath_dtr_t5}_delete'),
]
