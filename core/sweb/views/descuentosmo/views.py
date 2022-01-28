from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from core.sweb.forms import DescuentoMOForm
from core.sweb.models import DescuentoMO
from django.utils.decorators import method_decorator
from django.contrib import messages


class DescuentoMOListView(ListView):
    model = DescuentoMO
    template_name = 'descuentosmo/list.html'

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
                for i in DescuentoMO.objects.all().values('id', 'codigo', 'descripcion', 'descuento'):
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Descuentos Mano de Obra'
        context['add_url'] = reverse_lazy('sweb:descuentosmo_add')
        context['list_url'] = reverse_lazy('sweb:descuentosmo_list')
        context['entity'] = 'Descuentos MO'
        return context


class DescuentoMOCreateView(CreateView):
    model = DescuentoMO
    form_class = DescuentoMOForm
    template_name = 'descuentosmo/create.html'
    success_url = reverse_lazy('sweb:descuentosmo_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Descuento Mano de Obra'
        context['entity'] = 'Descuentos MO'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('sweb:descuentosmo_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Descuento MO añadido')
        return super().form_valid(form)


class DescuentoMOUpdateView(UpdateView):
    model = DescuentoMO
    form_class = DescuentoMOForm
    template_name = 'descuentosmo/create.html'
    success_url = reverse_lazy('sweb:descuentosmo_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Descuento Mano de Obra'
        context['entity'] = 'Descuentos MO'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('sweb:descuentosmo_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Descuento MO modificado')
        return super().form_valid(form)


class DescuentoMODeleteView(DeleteView):
    model = DescuentoMO
    template_name = 'descuentosmo/delete.html'
    success_url = reverse_lazy('sweb:descuentosmo_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Descuento Mano de Obra'
        context['entity'] = 'Descuentos MO'
        context['list_url'] = reverse_lazy('sweb:descuentosmo_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Descuento MO eliminado')
        return super().form_valid(form)

    # def delete(self, request, *args, **kwargs):
    #     messages.add_message(self.request, messages.SUCCESS, 'Descuento MO eliminado')
    #     return super(DescuentoMODeleteView, self).delete(request, *args, **kwargs)

