from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import FormaDePagoForm
from core.sweb.models import FormaDePago
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class FormaDePagoListView(BasicListView, ListView):
    folder = 'formasdepago'
    model = FormaDePago
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'descripcion', 'recibos', 'diasvto']


class FormaDePagoCreateView(BasicCreateView, CreateView):
    folder = 'formasdepago'
    model = FormaDePago
    form_class = FormaDePagoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class FormaDePagoUpdateView(BasicUpdateView, UpdateView):
    folder = 'formasdepago'
    model = FormaDePago
    form_class = FormaDePagoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class FormaDePagoDeleteView(BasicDeleteView, DeleteView):
    folder = 'formasdepago'
    model = FormaDePago
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'



