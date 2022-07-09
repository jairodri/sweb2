from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import ModeloForm
from core.sweb.models import Modelo
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class ModeloListView(BasicListView, ListView):
    folder = 'modelos'
    model = Modelo
    template_name = f'{folder}/list.html'


class ModeloCreateView(BasicCreateView, CreateView):
    folder = 'modelos'
    model = Modelo
    form_class = ModeloForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class ModeloUpdateView(BasicUpdateView, UpdateView):
    folder = 'modelos'
    model = Modelo
    form_class = ModeloForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class ModeloDeleteView(BasicDeleteView, DeleteView):
    folder = 'modelos'
    model = Modelo
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'







