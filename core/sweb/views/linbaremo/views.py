from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import LineaBaremoForm
from core.sweb.models import LineaBaremo, Baremo
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.sweb.views.baremo.views import BaremoUpdateView


class LineaBaremoCreateView(CreateView):
    folder = 'linbaremo'
    model = LineaBaremo
    form_class = LineaBaremoForm
    template_name = f'{folder}/create.html'
    # success_url = ''
    end_message_success = 'añadido'

    def get_initial(self):
        # Recuperamos la clave del registro de cabecera
        pk_baremo = self.request.get_full_path().split('/')[4]
        baremo = Baremo.objects.get(pk=pk_baremo)
        initial = {
            'baremo': baremo,
            'modifica': '0000',
            'tiempo': 0.00,
        }
        return initial

    # utilizamos un decorador para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        path_to_return = self.request.get_full_path().split(self.folder)[0]
        context['title'] = f'Añadir {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['action'] = 'add'
        context['list_url'] = path_to_return
        context['folder'] = self.folder
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path().split(self.folder)[0]


class LineaBaremoUpdateView(UpdateView):
    folder = 'linbaremo'
    model = LineaBaremo
    form_class = LineaBaremoForm
    template_name = f'{folder}/create.html'
    # success_url = ''
    end_message_success = 'modificado'

    # def get_initial(self):
    #     # Recuperamos la clave del registro de cabecera
    #     pk_baremo = self.request.get_full_path().split('/')[4]
    #     baremo = Baremo.objects.get(pk=pk_baremo)
    #     initial = {
    #         'baremo': baremo,
    #     }
    #     return initial

    # utilizamos un decorador para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = f'Editar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['action'] = 'edit'
        context['list_url'] = self.request.get_full_path().split(self.folder)[0]
        context['folder'] = self.folder
        # print(f'context: {context}')
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path().split(self.folder)[0]


class LineaBaremoDeleteView(DeleteView):
    folder = 'linbaremo'
    model = LineaBaremo
    template_name = f'{folder}/delete.html'
    success_url = ''
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'

    # utilizamos un decorador para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = f'Borrar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['list_url'] = self.request.get_full_path().split(self.folder)[0]
        context['action'] = 'delete'
        context['folder'] = self.folder
        return context

    def form_valid(self, form):
        # Reescribimos form_valid para controlar los ProtectedError
        try:
            self.object.delete()
            messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError as e:
            messages.error(self.request,
                           f'{self.start_message_error} {self.model._meta.verbose_name} {self.end_message_error}')
            return self.render_to_response(context=self.get_context_data())

    def get_success_url(self):
        return self.request.get_full_path().split(self.folder)[0]


