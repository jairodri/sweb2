from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import SeccionInternaForm
from core.sweb.models import SeccionInterna
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class SeccionInternaListView(BasicListView, ListView):
    folder = 'seccionint'
    model = SeccionInterna
    template_name = f'{folder}/list.html'


class SeccionInternaCreateView(BasicCreateView, CreateView):
    folder = 'seccionint'
    model = SeccionInterna
    form_class = SeccionInternaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class SeccionInternaUpdateView(BasicUpdateView, UpdateView):
    folder = 'seccionint'
    model = SeccionInterna
    form_class = SeccionInternaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class SeccionInternaDeleteView(BasicDeleteView, DeleteView):
    folder = 'seccionint'
    model = SeccionInterna
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'







