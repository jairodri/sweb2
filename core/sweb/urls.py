from django.urls import path
from core.sweb.views import vistaprueba

app_name = 'sweb'

urlpatterns = [
    path('prueba1/', vistaprueba, name='vistap1'),
]