from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import CodigoContableForm
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView
from core.sweb.models import CodigoContable


class CodigoContableListView(BasicListView, ListView):
    folder = 'codigocontable'
    model = CodigoContable
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'descripcion']


class CodigoContableCreateView(BasicCreateView, CreateView):
    folder = 'codigocontable'
    model = CodigoContable
    form_class = CodigoContableForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class CodigoContableUpdateView(BasicUpdateView, UpdateView):
    folder = 'codigocontable'
    model = CodigoContable
    form_class = CodigoContableForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class CodigoContableDeleteView(BasicDeleteView, DeleteView):
    folder = 'codigocontable'
    model = CodigoContable
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'



