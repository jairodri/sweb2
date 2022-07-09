from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import GamaForm
from core.sweb.models import Gama
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class GamaListView(BasicListView, ListView):
    folder = 'gamas'
    model = Gama
    template_name = f'{folder}/list.html'


class GamaCreateView(BasicCreateView, CreateView):
    folder = 'gamas'
    model = Gama
    form_class = GamaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class GamaUpdateView(BasicUpdateView, UpdateView):
    folder = 'gamas'
    model = Gama
    form_class = GamaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class GamaDeleteView(BasicDeleteView, DeleteView):
    folder = 'gamas'
    model = Gama
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'







