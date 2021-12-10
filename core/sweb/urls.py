from django.urls import path
from core.sweb.views.formasdepago.views import *
from core.sweb.views.dashboard.views import *
from core.sweb.views.tiposclienterec.views import *

app_name = 'sweb'

urlpatterns = [
    # Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Formas de Pago
    path('formasdepago/list/', FormaDePagoListView.as_view(), name='formasdepago_list'),
    path('formasdepago/add/', FormaDePagoCreateView.as_view(), name='formasdepago_add'),
    path('formasdepago/edit/<int:pk>/', FormaDePagoUpdateView.as_view(), name='formasdepago_edit'),
    path('formasdepago/delete/<int:pk>/', FormaDePagoDeleteView.as_view(), name='formasdepago_delete'),

    # Tipos de Cliente de Recambios
    path('tiposclienterec/list/', TipoClienteRecambiosListView.as_view(), name='tiposclienterec_list'),
    path('tiposclienterec/add/', TipoClienteRecambiosCreateView.as_view(), name='tiposclienterec_add'),
    path('tiposclienterec/edit/<int:pk>/', TipoClienteRecambiosUpdateView.as_view(), name='tiposclienterec_edit'),
    path('tiposclienterec/delete/<int:pk>/', TipoClienteRecambiosDeleteView.as_view(), name='tiposclienterec_delete'),
]