from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from core.sweb.forms import TipoClienteRecambiosForm
from core.sweb.models import TipoClienteRecambios
from django.utils.decorators import method_decorator
from django.contrib import messages


class TipoClienteRecambiosListView(ListView):
    model = TipoClienteRecambios
    template_name = 'tiposclienterec/list.html'

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
                for i in TipoClienteRecambios.objects.all().values('id', 'codigo', 'descripcion', 'datocontable'):
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de Cliente de Recambios'
        context['add_url'] = reverse_lazy('sweb:tiposclienterec_add')
        context['list_url'] = reverse_lazy('sweb:tiposclienterec_list')
        context['entity'] = 'Tipos de Cliente'
        return context


class TipoClienteRecambiosCreateView(CreateView):
    model = TipoClienteRecambios
    form_class = TipoClienteRecambiosForm
    template_name = 'tiposclienterec/create.html'
    success_url = reverse_lazy('sweb:tiposclienterec_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Tipo de Cliente de Recambios'
        context['entity'] = 'Tipos de Cliente'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('sweb:tiposclienterec_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tipo de Cliente añadido')
        return super().form_valid(form)


class TipoClienteRecambiosUpdateView(UpdateView):
    model = TipoClienteRecambios
    form_class = TipoClienteRecambiosForm
    template_name = 'tiposclienterec/create.html'
    success_url = reverse_lazy('sweb:tiposclienterec_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo de Cliente de Recambios'
        context['entity'] = 'Tipos de Cliente'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('sweb:tiposclienterec_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tipo de Cliente modificado')
        return super().form_valid(form)


class TipoClienteRecambiosDeleteView(DeleteView):
    model = TipoClienteRecambios
    template_name = 'tiposclienterec/delete.html'
    success_url = reverse_lazy('sweb:tiposclienterec_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Tipo de Cliente de Recambios'
        context['entity'] = 'Tipos de Cliente'
        context['list_url'] = reverse_lazy('sweb:tiposclienterec_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tipo de Cliente eliminado')
        return super().form_valid(form)

    # def delete(self, request, *args, **kwargs):
    #     messages.add_message(self.request, messages.SUCCESS, 'Tipo de Cliente eliminado')
    #     return super(TipoClienteRecambiosDeleteView, self).delete(request, *args, **kwargs)

