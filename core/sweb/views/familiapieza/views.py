from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import FamiliaPiezaForm
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView
from core.sweb.models import FamiliaPieza


class FamiliaPiezaListView(BasicListView, ListView):
    folder = 'familiapieza'
    model = FamiliaPieza
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'descripcion']


class FamiliaPiezaCreateView(BasicCreateView, CreateView):
    folder = 'familiapieza'
    model = FamiliaPieza
    form_class = FamiliaPiezaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class FamiliaPiezaUpdateView(BasicUpdateView, UpdateView):
    folder = 'familiapieza'
    model = FamiliaPieza
    form_class = FamiliaPiezaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class FamiliaPiezaDeleteView(BasicDeleteView, DeleteView):
    folder = 'familiapieza'
    model = FamiliaPieza
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'



