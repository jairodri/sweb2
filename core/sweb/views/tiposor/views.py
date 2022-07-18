from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import TipoOrdenReparacionForm
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView
from core.sweb.models import TipoOrdenReparacion


class TipoOrdenReparacionListView(BasicListView, ListView):
    folder = 'tiposor'
    model = TipoOrdenReparacion
    template_name = f'{folder}/list.html'


class TipoOrdenReparacionCreateView(BasicCreateView, CreateView):
    folder = 'tiposor'
    model = TipoOrdenReparacion
    form_class = TipoOrdenReparacionForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class TipoOrdenReparacionUpdateView(BasicUpdateView, UpdateView):
    folder = 'tiposor'
    model = TipoOrdenReparacion
    form_class = TipoOrdenReparacionForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class TipoOrdenReparacionDeleteView(BasicDeleteView, DeleteView):
    folder = 'tiposor'
    model = TipoOrdenReparacion
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'



