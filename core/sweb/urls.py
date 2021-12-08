from django.urls import path
from core.sweb.views.formasdepago.views import *
from core.sweb.views.dashboard.views import *

app_name = 'sweb'

urlpatterns = [
    # Formas de Pago
    path('formasdepago/list/', FormaDePagoListView.as_view(), name='formasdepago_list'),
    path('formasdepago/add/', FormaDePagoCreateView.as_view(), name='formasdepago_add'),
    path('formasdepago/edit/<int:pk>/', FormaDePagoUpdateView.as_view(), name='formasdepago_edit'),
    path('formasdepago/delete/<int:pk>/', FormaDePagoDeleteView.as_view(), name='formasdepago_delete'),
    # Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]