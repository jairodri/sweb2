from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import ConcesionarioForm
from core.sweb.models import Concesionario
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class ConcesionarioListView(BasicListView, ListView):
    folder = 'concesionarios'
    model = Concesionario
    template_name = f'{folder}/list.html'


class ConcesionarioCreateView(BasicCreateView, CreateView):
    folder = 'concesionarios'
    model = Concesionario
    form_class = ConcesionarioForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class ConcesionarioUpdateView(BasicUpdateView, UpdateView):
    folder = 'concesionarios'
    model = Concesionario
    form_class = ConcesionarioForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class ConcesionarioDeleteView(BasicDeleteView, DeleteView):
    folder = 'concesionarios'
    model = Concesionario
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'







