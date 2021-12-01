from django.urls import path
from core.sweb.views.formasdepago.views import *

app_name = 'sweb'

urlpatterns = [
    path('formasdepago/list/', FormaDePagoListView.as_view(), name='formasdepago_list'),
]