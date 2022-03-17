from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.forms import BancoForm
from core.sweb.models import Banco
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView


class BancoListView(BasicListView, ListView):
    folder = 'bancos'
    model = Banco
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'sucursal', 'razonsocial', 'telefono']


class BancoCreateView(BasicCreateView, CreateView):
    folder = 'bancos'
    model = Banco
    form_class = BancoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class BancoUpdateView(BasicUpdateView, UpdateView):
    folder = 'bancos'
    model = Banco
    form_class = BancoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class BancoDeleteView(BasicDeleteView, DeleteView):
    folder = 'bancos'
    model = Banco
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class BancoDetailView(BasicDetailView, DetailView):
    folder = 'bancos'
    model = Banco
    template_name = f'{folder}/detail.html'

