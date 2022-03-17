from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import DescuentoMOForm
from core.sweb.models import DescuentoMO
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class DescuentoMOListView(BasicListView, ListView):
    folder = 'descuentosmo'
    model = DescuentoMO
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'descripcion', 'descuento']


class DescuentoMOCreateView(BasicCreateView, CreateView):
    folder = 'descuentosmo'
    model = DescuentoMO
    form_class = DescuentoMOForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class DescuentoMOUpdateView(BasicUpdateView, UpdateView):
    folder = 'descuentosmo'
    model = DescuentoMO
    form_class = DescuentoMOForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class DescuentoMODeleteView(BasicDeleteView, DeleteView):
    folder = 'descuentosmo'
    model = DescuentoMO
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'







