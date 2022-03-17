from django.urls import path
from core.sweb.views.formasdepago.views import *
from core.sweb.views.dashboard.views import *
from core.sweb.views.tiposclienterec.views import *
from core.sweb.views.descuentosmo.views import *
from core.sweb.views.bancos.views import *
from core.sweb.views.clientes.views import *
from core.sweb.views.administrador.views import *
from core.sweb.views.numeracionauto.views import *
from core.sweb.views.unidadesmedida.views import *
from core.sweb.views.codapropza.views import *
from core.sweb.views.codigosiva.views import *

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
]
