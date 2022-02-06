from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from core.sweb.forms import FormaDePagoForm
from core.sweb.models import FormaDePago
from django.utils.decorators import method_decorator
from django.contrib import messages


class FormaDePagoListView(ListView):
    model = FormaDePago
    template_name = 'formasdepago/list.html'

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    # @method_decorator(csrf_exempt)  # para el POST que se hace al cargar la datatable con ajax
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
                for i in FormaDePago.objects.all().values('id', 'codigo', 'descripcion', 'recibos', 'diasvto'):
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formas de Pago'
        context['add_url'] = reverse_lazy('sweb:formasdepago_add')
        context['list_url'] = reverse_lazy('sweb:formasdepago_list')
        context['entity'] = 'Formas de Pago'
        return context


class FormaDePagoCreateView(CreateView):
    model = FormaDePago
    form_class = FormaDePagoForm
    template_name = 'formasdepago/create.html'
    success_url = reverse_lazy('sweb:formasdepago_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Forma de Pago'
        context['entity'] = 'Formas de Pago'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('sweb:formasdepago_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Forma de Pago añadida')
        return super().form_valid(form)


class FormaDePagoUpdateView(UpdateView):
    model = FormaDePago
    form_class = FormaDePagoForm
    template_name = 'formasdepago/create.html'
    success_url = reverse_lazy('sweb:formasdepago_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Forma de Pago'
        context['entity'] = 'Formas de Pago'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('sweb:formasdepago_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Forma de Pago modificada')
        return super().form_valid(form)


class FormaDePagoDeleteView(DeleteView):
    model = FormaDePago
    # form_class = FormaDePagoForm # No he conseguido que funcione con el form_class
    template_name = 'formasdepago/delete.html'
    success_url = reverse_lazy('sweb:formasdepago_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Forma de Pago'
        context['entity'] = 'Formas de Pago'
        context['list_url'] = reverse_lazy('sweb:formasdepago_list')
        context['action'] = 'delete'
        return context

    # override get_initial para rellenar el form con los datos del registro
    # serializamos en un diccionario los campos del objeto
    # def get_initial(self):
    #     # return {
    #     #     'codigo': self.object.codigo,
    #     #     'descripcion': self.object.descripcion,
    #     #     'recibos': self.object.recibos,
    #     #     'diasvto': self.object.diasvto
    #     # }
    #     return model_to_dict(self.object)

    # No funciona el envío de mensajes de este modo con DeleteView
    # con la versión 4 de Django ya funciona
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Forma de Pago eliminada')
        return super().form_valid(form)

    # def delete(self, request, *args, **kwargs):
    #     messages.add_message(self.request, messages.SUCCESS, 'Forma de Pago eliminada')
    #     return super(FormaDePagoDeleteView, self).delete(request, *args, **kwargs)

