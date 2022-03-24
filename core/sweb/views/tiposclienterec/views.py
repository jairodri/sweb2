from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import TipoClienteRecambiosForm
from core.sweb.models import TipoClienteRecambios
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class TipoClienteRecambiosListView(BasicListView, ListView):
    folder = 'tiposclienterec'
    model = TipoClienteRecambios
    template_name = f'{folder}/list.html'


class TipoClienteRecambiosCreateView(BasicCreateView, CreateView):
    folder = 'tiposclienterec'
    model = TipoClienteRecambios
    form_class = TipoClienteRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class TipoClienteRecambiosUpdateView(BasicUpdateView, UpdateView):
    folder = 'tiposclienterec'
    model = TipoClienteRecambios
    form_class = TipoClienteRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class TipoClienteRecambiosDeleteView(BasicDeleteView, DeleteView):
    folder = 'tiposclienterec'
    model = TipoClienteRecambios
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'



