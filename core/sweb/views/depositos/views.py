from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import CapacidadDepositoForm
from core.sweb.models import CapacidadDeposito
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class CapacidadDepositoListView(BasicListView, ListView):
    folder = 'depositos'
    model = CapacidadDeposito
    template_name = f'{folder}/list.html'


class CapacidadDepositoCreateView(BasicCreateView, CreateView):
    folder = 'depositos'
    model = CapacidadDeposito
    form_class = CapacidadDepositoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class CapacidadDepositoUpdateView(BasicUpdateView, UpdateView):
    folder = 'depositos'
    model = CapacidadDeposito
    form_class = CapacidadDepositoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class CapacidadDepositoDeleteView(BasicDeleteView, DeleteView):
    folder = 'depositos'
    model = CapacidadDeposito
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'







