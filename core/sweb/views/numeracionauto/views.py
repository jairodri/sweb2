from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from core.sweb.forms import NumeracionAutomaticaForm
from core.sweb.models import NumeracionAutomatica
from django.utils.decorators import method_decorator
from django.contrib import messages


class NumeracionAutomaticaListView(ListView):
    model = NumeracionAutomatica
    template_name = 'numeracionauto/list.html'

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
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
                for i in NumeracionAutomatica.objects.all().values('id', 'codigo', 'tabla', 'serie', 'contador', 'activo'):
                    data.append(i)
            else:
                data = {
                    'error': 'Ha ocurrido un error'
                }
        except Exception as e:
            data = {
                'error': str(e)
            }
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Numeración Automática'
        context['add_url'] = reverse_lazy('sweb:mumeracionauto_add')
        context['list_url'] = reverse_lazy('sweb:mumeracionauto_list')
        context['entity'] = 'Numeración Automática'
        return context


class NumeracionAutomaticaCreateView(CreateView):
    model = NumeracionAutomatica
    form_class = NumeracionAutomaticaForm
    template_name = 'numeracionauto/create.html'
    success_url = reverse_lazy('sweb:mumeracionauto_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Numeración Automática'
        context['entity'] = 'Numeración Automática'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('sweb:mumeracionauto_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Numeración Automática añadida')
        return super().form_valid(form)


class NumeracionAutomaticaUpdateView(UpdateView):
    model = NumeracionAutomatica
    form_class = NumeracionAutomaticaForm
    template_name = 'numeracionauto/create.html'
    success_url = reverse_lazy('sweb:mumeracionauto_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Numeración Automática'
        context['entity'] = 'Numeración Automática'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('sweb:mumeracionauto_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Numeración Automática modificada')
        return super().form_valid(form)


class NumeracionAutomaticaDeleteView(DeleteView):
    model = NumeracionAutomatica
    template_name = 'numeracionauto/delete.html'
    success_url = reverse_lazy('sweb:mumeracionauto_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Numeración Automática'
        context['entity'] = 'Numeración Automática'
        context['list_url'] = reverse_lazy('sweb:mumeracionauto_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Numeración Automática eliminada')
        return super().form_valid(form)
