from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from core.sweb.models import Cliente
from django.views.generic import ListView


class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/list.html'

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        # context['add_url'] = reverse_lazy('sweb:bancos_add')
        context['list_url'] = reverse_lazy('sweb:clientes_list')
        context['entity'] = 'Clientes'
        return context
