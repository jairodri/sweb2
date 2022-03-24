from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import ModeloVehPiezaForm
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView
from core.sweb.models import ModeloVehPieza


class ModeloVehPiezaListView(BasicListView, ListView):
    folder = 'modvehpieza'
    model = ModeloVehPieza
    template_name = f'{folder}/list.html'


class ModeloVehPiezaCreateView(BasicCreateView, CreateView):
    folder = 'modvehpieza'
    model = ModeloVehPieza
    form_class = ModeloVehPiezaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class ModeloVehPiezaUpdateView(BasicUpdateView, UpdateView):
    folder = 'modvehpieza'
    model = ModeloVehPieza
    form_class = ModeloVehPiezaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class ModeloVehPiezaDeleteView(BasicDeleteView, DeleteView):
    folder = 'modvehpieza'
    model = ModeloVehPieza
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'



