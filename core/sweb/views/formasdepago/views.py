from django.views.generic import ListView
from core.sweb.models import FormaDePago


class FormaDePagoListView(ListView):
    model = FormaDePago
    template_name = 'formasdepago/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formas de Pago'
        return context