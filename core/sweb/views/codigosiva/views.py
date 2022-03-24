from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import CodigoIvaForm
from core.sweb.models import CodigoIva
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class CodigoIvaListView(BasicListView, ListView):
    folder = 'codigosiva'
    model = CodigoIva
    template_name = f'{folder}/list.html'


class CodigoIvaCreateView(BasicCreateView, CreateView):
    folder = 'codigosiva'
    model = CodigoIva
    form_class = CodigoIvaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class CodigoIvaUpdateView(BasicUpdateView, UpdateView):
    folder = 'codigosiva'
    model = CodigoIva
    form_class = CodigoIvaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class CodigoIvaDeleteView(BasicDeleteView, DeleteView):
    folder = 'codigosiva'
    model = CodigoIva
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'








