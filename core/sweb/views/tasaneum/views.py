from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import TasaNeumaticoForm
from core.sweb.models import TasaNeumatico
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class TasaNeumaticoListView(BasicListView, ListView):
    folder = 'tasaneum'
    model = TasaNeumatico
    template_name = f'{folder}/list.html'


class TasaNeumaticoCreateView(BasicCreateView, CreateView):
    folder = 'tasaneum'
    model = TasaNeumatico
    form_class = TasaNeumaticoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class TasaNeumaticoUpdateView(BasicUpdateView, UpdateView):
    folder = 'tasaneum'
    model = TasaNeumatico
    form_class = TasaNeumaticoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class TasaNeumaticoDeleteView(BasicDeleteView, DeleteView):
    folder = 'tasaneum'
    model = TasaNeumatico
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'







