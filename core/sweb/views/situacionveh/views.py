from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import SituacionVehiculoForm
from core.sweb.models import SituacionVehiculo
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class SituacionVehiculoListView(BasicListView, ListView):
    folder = 'situacionveh'
    model = SituacionVehiculo
    template_name = f'{folder}/list.html'


class SituacionVehiculoCreateView(BasicCreateView, CreateView):
    folder = 'situacionveh'
    model = SituacionVehiculo
    form_class = SituacionVehiculoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class SituacionVehiculoUpdateView(BasicUpdateView, UpdateView):
    folder = 'situacionveh'
    model = SituacionVehiculo
    form_class = SituacionVehiculoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class SituacionVehiculoDeleteView(BasicDeleteView, DeleteView):
    folder = 'situacionveh'
    model = SituacionVehiculo
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'







