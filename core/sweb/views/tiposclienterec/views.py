from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
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
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['title'] = 'Tipos de Cliente de Recambios'
        context['entity'] = 'Tipos de Cliente'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('sweb:tiposclienterec_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tipo de Cliente añadido')
        return super().form_valid(form)


# class FormaDePagoUpdateView(UpdateView):
#     model = FormaDePago
#     form_class = FormaDePagoForm
#     template_name = 'formasdepago/create.html'
#     success_url = reverse_lazy('sweb:formasdepago_list')
#
#     # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     # sobreescribimos el método get_context_data para añadir info al contexto
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Editar Forma de Pago'
#         context['entity'] = 'Formas de Pago'
#         context['action'] = 'edit'
#         context['list_url'] = reverse_lazy('sweb:formasdepago_list')
#         return context
#
#     def form_valid(self, form):
#         messages.add_message(self.request, messages.SUCCESS, 'Forma de Pago modificada')
#         return super().form_valid(form)
#
#
# class FormaDePagoDeleteView(DeleteView):
#     model = FormaDePago
#     template_name = 'formasdepago/delete.html'
#     success_url = reverse_lazy('sweb:formasdepago_list')
#
#     # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     # sobreescribimos el método get_context_data para añadir info al contexto
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Borrar Forma de Pago'
#         context['entity'] = 'Formas de Pago'
#         context['list_url'] = reverse_lazy('sweb:formasdepago_list')
#         return context
#
#     # No funciona el envío de mensajes de este modo con DeleteView
#     # def form_valid(self, form):
#     #     messages.add_message(self.request, messages.SUCCESS, 'Forma de Pago eliminada')
#     #     return super().form_valid(form)
#
#     def delete(self, request, *args, **kwargs):
#         messages.add_message(self.request, messages.SUCCESS, 'Forma de Pago eliminada')
#         return super(FormaDePagoDeleteView, self).delete(request, *args, **kwargs)

