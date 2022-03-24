from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import NumeracionAutomaticaForm
from core.sweb.models import NumeracionAutomatica
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class NumeracionAutomaticaListView(BasicListView, ListView):
    folder = 'numeracionauto'
    model = NumeracionAutomatica
    template_name = f'{folder}/list.html'


class NumeracionAutomaticaCreateView(BasicCreateView, CreateView):
    folder = 'numeracionauto'
    model = NumeracionAutomatica
    form_class = NumeracionAutomaticaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class NumeracionAutomaticaUpdateView(BasicUpdateView, UpdateView):
    folder = 'numeracionauto'
    model = NumeracionAutomatica
    form_class = NumeracionAutomaticaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class NumeracionAutomaticaDeleteView(BasicDeleteView, DeleteView):
    folder = 'numeracionauto'
    model = NumeracionAutomatica
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'

