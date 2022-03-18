from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import FamiliaMarketingForm
from core.sweb.models import FamiliaMarketing
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class FamiliaMarketingListView(BasicListView, ListView):
    folder = 'fmarketing'
    model = FamiliaMarketing
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'descripcion']


class FamiliaMarketingCreateView(BasicCreateView, CreateView):
    folder = 'fmarketing'
    model = FamiliaMarketing
    form_class = FamiliaMarketingForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class FamiliaMarketingUpdateView(BasicUpdateView, UpdateView):
    folder = 'fmarketing'
    model = FamiliaMarketing
    form_class = FamiliaMarketingForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class FamiliaMarketingDeleteView(BasicDeleteView, DeleteView):
    folder = 'fmarketing'
    model = FamiliaMarketing
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'


