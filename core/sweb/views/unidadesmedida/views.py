from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import UnidadMedidaForm
from core.sweb.models import UnidadMedida
from django.contrib import messages
from core.sweb.mixins import BasicView

folder = 'unidadesmedida'


class UnidadMedidaListView(BasicView, ListView):
    model = UnidadMedida
    template_name = f'{folder}/list.html'

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        # data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # recuperamos solo los campos necesarios para la paginación
                for i in UnidadMedida.objects.all().values('id', 'codigo', 'descripcion'):
                    data.append(i)
            else:
                data = {'error': 'Ha ocurrido un error'}
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = UnidadMedida._meta.verbose_name_plural
        context['add_url'] = reverse_lazy(f'sweb:{folder}_add')
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        context['entity'] = UnidadMedida._meta.verbose_name_plural
        return context


class UnidadMedidaCreateView(BasicView, CreateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Añadir {UnidadMedida._meta.verbose_name}'
        context['entity'] = UnidadMedida._meta.verbose_name_plural
        context['action'] = 'add'
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f'{UnidadMedida._meta.verbose_name} añadida')
        return super().form_valid(form)


class UnidadMedidaUpdateView(BasicView, UpdateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar {UnidadMedida._meta.verbose_name}'
        context['entity'] = UnidadMedida._meta.verbose_name_plural
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f'{UnidadMedida._meta.verbose_name} modificada')
        return super().form_valid(form)


class UnidadMedidaDeleteView(BasicView, DeleteView):
    model = UnidadMedida
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Borrar {UnidadMedida._meta.verbose_name}'
        context['entity'] = UnidadMedida._meta.verbose_name_plural
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        # Reescribimos form_valid para controlar los ProtectedError
        try:
            self.object.delete()
            messages.success(self.request, f'{UnidadMedida._meta.verbose_name} eliminada')
            return HttpResponseRedirect(self.success_url)
        except ProtectedError as e:
            messages.error(self.request,
                           f'No se puede borrar esta {UnidadMedida._meta.verbose_name} porque está siendo utilizada en otra tabla')
            return self.render_to_response(context=self.get_context_data())
        # messages.add_message(self.request, messages.SUCCESS, 'Unidad de Medida eliminada')
        # return super().form_valid(form)


