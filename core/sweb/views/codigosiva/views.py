from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import CodigoIvaForm
from core.sweb.models import CodigoIva
from django.contrib import messages
from core.sweb.mixins import BasicView

folder = 'codigosiva'


class CodigoIvaListView(BasicView, ListView):
    model = CodigoIva
    template_name = f'{folder}/list.html'

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        # data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # recuperamos solo los campos necesarios para la paginación
                for i in CodigoIva.objects.all().values('id', 'codigo', 'descripcion', 'porcentaje'):
                    data.append(i)
            else:
                data = {'error': 'Ha ocurrido un error'}
        except Exception as e:
            data = {
                'error': str(e)
            }
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CodigoIva._meta.verbose_name_plural
        context['add_url'] = reverse_lazy(f'sweb:{folder}_add')
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        context['entity'] = CodigoIva._meta.verbose_name_plural
        return context


class CodigoIvaCreateView(BasicView, CreateView):
    model = CodigoIva
    form_class = CodigoIvaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Añadir {CodigoIva._meta.verbose_name}'
        context['entity'] = CodigoIva._meta.verbose_name_plural
        context['action'] = 'add'
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f'{CodigoIva._meta.verbose_name} añadido')
        return super().form_valid(form)


class CodigoIvaUpdateView(BasicView, UpdateView):
    model = CodigoIva
    form_class = CodigoIvaForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar {CodigoIva._meta.verbose_name}'
        context['entity'] = CodigoIva._meta.verbose_name_plural
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f'{CodigoIva._meta.verbose_name} modificado')
        return super().form_valid(form)


class CodigoIvaDeleteView(BasicView, DeleteView):
    model = CodigoIva
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Borrar {CodigoIva._meta.verbose_name}'
        context['entity'] = CodigoIva._meta.verbose_name_plural
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        # Reescribimos form_valid para controlar los ProtectedError
        try:
            self.object.delete()
            messages.success(self.request, f'{CodigoIva._meta.verbose_name} eliminado')
            return HttpResponseRedirect(self.success_url)
        except ProtectedError as e:
            messages.error(self.request,
                           f'No se puede borrar este {CodigoIva._meta.verbose_name} porque está siendo utilizado en otra tabla')
            return self.render_to_response(context=self.get_context_data())







