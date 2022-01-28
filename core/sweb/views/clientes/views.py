from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sweb.models import Cliente
from django.views.generic import ListView


class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/list.html'

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)  # para el POST que se hace al cargar la datatable con ajax
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # recuperamos solo los campos necesarios para la paginación
                for i in Cliente.objects.all().values('id', 'codigo', 'razonSocial', 'cif', 'telefono', 'poblacion'):
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        # context['add_url'] = reverse_lazy('sweb:bancos_add')
        context['list_url'] = reverse_lazy('sweb:clientes_list')
        context['entity'] = 'Clientes'
        return context
