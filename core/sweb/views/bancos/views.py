from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.forms import BancoForm
from core.sweb.models import Banco
from django.utils.decorators import method_decorator
from django.contrib import messages


class BancoListView(ListView):
    model = Banco
    template_name = 'bancos/list.html'

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bancos'
        context['add_url'] = reverse_lazy('sweb:bancos_add')
        context['list_url'] = reverse_lazy('sweb:bancos_list')
        context['entity'] = 'Bancos'
        return context


class BancoCreateView(CreateView):
    model = Banco
    form_class = BancoForm
    template_name = 'bancos/create.html'
    success_url = reverse_lazy('sweb:bancos_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Banco'
        context['entity'] = 'Bancos'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('sweb:bancos_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Banco añadido')
        return super().form_valid(form)


class BancoUpdateView(UpdateView):
    model = Banco
    form_class = BancoForm
    template_name = 'bancos/create.html'
    success_url = reverse_lazy('sweb:bancos_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Banco'
        context['entity'] = 'Bancos'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('sweb:bancos_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Banco modificado')
        return super().form_valid(form)


class BancoDeleteView(DeleteView):
    model = Banco
    template_name = 'bancos/delete.html'
    success_url = reverse_lazy('sweb:bancos_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Banco'
        context['entity'] = 'Bancos'
        context['list_url'] = reverse_lazy('sweb:bancos_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Banco eliminado')
        return super().form_valid(form)


class BancoDetailView(DetailView):
    model = Banco
    template_name = 'bancos/detail.html'
    # success_url = reverse_lazy('sweb:bancos_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle Banco'
        context['entity'] = 'Bancos'
        context['list_url'] = reverse_lazy('sweb:bancos_list')
        context['action'] = 'detail'
        return context
