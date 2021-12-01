from django.urls import path
from core.sweb.views.formasdepago.views import formasdepago_list

app_name = 'sweb'

urlpatterns = [
    path('formasdepago/list/', formasdepago_list, name='formasdepago_list'),
]