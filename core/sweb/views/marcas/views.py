from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import MarcaForm
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView
from core.sweb.models import Marca


class MarcaListView(BasicListView, ListView):
    folder = 'marcas'
    model = Marca
    template_name = f'{folder}/list.html'


class MarcaCreateView(BasicCreateView, CreateView):
    folder = 'marcas'
    model = Marca
    form_class = MarcaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class MarcaUpdateView(BasicUpdateView, UpdateView):
    folder = 'marcas'
    model = Marca
    form_class = MarcaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class MarcaDeleteView(BasicDeleteView, DeleteView):
    folder = 'marcas'
    model = Marca
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'



