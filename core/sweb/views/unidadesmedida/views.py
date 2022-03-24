from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import UnidadMedidaForm
from core.sweb.models import UnidadMedida
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class UnidadMedidaListView(BasicListView, ListView):
    folder = 'unidadesmedida'
    model = UnidadMedida
    template_name = f'{folder}/list.html'


class UnidadMedidaCreateView(BasicCreateView, CreateView):
    folder = 'unidadesmedida'
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class UnidadMedidaUpdateView(BasicUpdateView, UpdateView):
    folder = 'unidadesmedida'
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class UnidadMedidaDeleteView(BasicDeleteView, DeleteView):
    folder = 'unidadesmedida'
    model = UnidadMedida
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'


