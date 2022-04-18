from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import TasaCodigoForm
from core.sweb.models import TasaCodigo
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class TasaCodigoListView(BasicListView, ListView):
    folder = 'codigotasa'
    model = TasaCodigo
    template_name = f'{folder}/list.html'


class TasaCodigoCreateView(BasicCreateView, CreateView):
    folder = 'codigotasa'
    model = TasaCodigo
    form_class = TasaCodigoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class TasaCodigoUpdateView(BasicUpdateView, UpdateView):
    folder = 'codigotasa'
    model = TasaCodigo
    form_class = TasaCodigoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class TasaCodigoDeleteView(BasicDeleteView, DeleteView):
    folder = 'codigotasa'
    model = TasaCodigo
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'







