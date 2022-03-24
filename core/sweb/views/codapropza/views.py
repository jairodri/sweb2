from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import CodigoAproPiezaForm
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView
from core.sweb.models import CodigoAproPieza


class CodigoAproPiezaListView(BasicListView, ListView):
    folder = 'codapropza'
    model = CodigoAproPieza
    template_name = f'{folder}/list.html'


class CodigoAproPiezaCreateView(BasicCreateView, CreateView):
    folder = 'codapropza'
    model = CodigoAproPieza
    form_class = CodigoAproPiezaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class CodigoAproPiezaUpdateView(BasicUpdateView, UpdateView):
    folder = 'codapropza'
    model = CodigoAproPieza
    form_class = CodigoAproPiezaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class CodigoAproPiezaDeleteView(BasicDeleteView, DeleteView):
    folder = 'codapropza'
    model = CodigoAproPieza
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'



