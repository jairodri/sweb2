from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import CategoriaOperarioForm
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView
from core.sweb.models import CategoriaOperario


class CategoriaOperarioListView(BasicListView, ListView):
    folder = 'catoper'
    model = CategoriaOperario
    template_name = f'{folder}/list.html'


class CategoriaOperarioCreateView(BasicCreateView, CreateView):
    folder = 'catoper'
    model = CategoriaOperario
    form_class = CategoriaOperarioForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class CategoriaOperarioUpdateView(BasicUpdateView, UpdateView):
    folder = 'catoper'
    model = CategoriaOperario
    form_class = CategoriaOperarioForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class CategoriaOperarioDeleteView(BasicDeleteView, DeleteView):
    folder = 'catoper'
    model = CategoriaOperario
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'



