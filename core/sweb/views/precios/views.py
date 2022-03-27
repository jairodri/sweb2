from django.views.generic import ListView
from core.sweb.models import PrecioTarifa
from core.sweb.mixins import BasicListView


class PrecioTarifaListView(BasicListView, ListView):
    folder = 'precios'
    model = PrecioTarifa
    template_name = f'{folder}/list.html'




