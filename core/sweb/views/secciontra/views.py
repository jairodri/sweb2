from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import SeccionTrabajoForm
from core.sweb.models import SeccionTrabajo
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class SeccionTrabajoListView(BasicListView, ListView):
    folder = 'secciontra'
    model = SeccionTrabajo
    template_name = f'{folder}/list.html'


class SeccionTrabajoCreateView(BasicCreateView, CreateView):
    folder = 'secciontra'
    model = SeccionTrabajo
    form_class = SeccionTrabajoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class SeccionTrabajoUpdateView(BasicUpdateView, UpdateView):
    folder = 'secciontra'
    model = SeccionTrabajo
    form_class = SeccionTrabajoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class SeccionTrabajoDeleteView(BasicDeleteView, DeleteView):
    folder = 'secciontra'
    model = SeccionTrabajo
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'







