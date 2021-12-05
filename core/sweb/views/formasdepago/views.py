from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import FormaDePagoForm
from core.sweb.models import FormaDePago
from django.utils.decorators import method_decorator


class FormaDePagoListView(ListView):
    model = FormaDePago
    template_name = 'formasdepago/list.html'

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Forma de Pago'
        context['entity'] = 'Formas de Pago'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('sweb:formasdepago_list')
        return context


class FormaDePagoUpdateView(UpdateView):
    model = FormaDePago
    form_class = FormaDePagoForm
    template_name = 'formasdepago/create.html'
    success_url = reverse_lazy('sweb:formasdepago_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Forma de Pago'
        context['entity'] = 'Formas de Pago'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('sweb:formasdepago_list')
        return context


class FormaDePagoDeleteView(DeleteView):
    model = FormaDePago
    template_name = 'formasdepago/delete.html'
    success_url = reverse_lazy('sweb:formasdepago_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Forma de Pago'
        context['entity'] = 'Formas de Pago'
        context['list_url'] = reverse_lazy('sweb:formasdepago_list')
        return context

