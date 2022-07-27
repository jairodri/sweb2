from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import OperarioRecambiosForm
from core.sweb.models import OperarioRecambios
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class OperarioRecambiosListView(BasicListView, ListView):
    folder = 'operecam'
    model = OperarioRecambios
    template_name = f'{folder}/list.html'


class OperarioRecambiosCreateView(BasicCreateView, CreateView):
    folder = 'operecam'
    model = OperarioRecambios
    form_class = OperarioRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class OperarioRecambiosUpdateView(BasicUpdateView, UpdateView):
    folder = 'operecam'
    model = OperarioRecambios
    form_class = OperarioRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class OperarioRecambiosDeleteView(BasicDeleteView, DeleteView):
    folder = 'operecam'
    model = OperarioRecambios
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'








