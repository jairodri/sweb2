from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import AmpliacionGarantiaForm
from core.sweb.models import AmpliacionGarantia
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView


class AmpliacionGarantiaListView(BasicListView, ListView):
    folder = 'ampaga'
    model = AmpliacionGarantia
    template_name = f'{folder}/list.html'


class AmpliacionGarantiaCreateView(BasicCreateView, CreateView):
    folder = 'ampaga'
    model = AmpliacionGarantia
    form_class = AmpliacionGarantiaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class AmpliacionGarantiaUpdateView(BasicUpdateView, UpdateView):
    folder = 'ampaga'
    model = AmpliacionGarantia
    form_class = AmpliacionGarantiaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'


class AmpliacionGarantiaDeleteView(BasicDeleteView, DeleteView):
    folder = 'ampaga'
    model = AmpliacionGarantia
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'







