from django.http import JsonResponse
from django.urls import reverse_lazy
from core.sweb.forms import BaremoForm
from core.sweb.models import Baremo, LineaBaremo
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from django.db.models import Q


class BaremoListView(BasicListView, ListView):
    folder = 'baremo'
    model = Baremo
    template_name = f'{folder}/list.html'


class BaremoCreateView(BasicCreateView, CreateView):
    folder = 'baremo'
    model = Baremo
    form_class = BaremoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'


class BaremoUpdateView(BasicUpdateView, UpdateView):
    folder = 'baremo'
    model = Baremo
    form_class = BaremoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        try:
            # print(f'Post: {request.POST}')
            action = request.POST['action']
            # diferenciamos si la paginación es en cliente o en servidor
            if action == 'searchdata_s':
                # Recuperamos las líneas que pertenzcan a la operación baremo a través de su id
                # activamos un segundo nivel de anidamiento de paginaciones con level_nesting=2
                datos = self.datatables_server(LineaBaremo, request, key_value=kwargs.get('pk'), level_nesting=2)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            return super().post(request, *args, **kwargs)

        return JsonResponse(datos, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity2'] = LineaBaremo._meta.verbose_name
        context['add_url2'] = reverse_lazy(f'sweb:linbaremo_add', kwargs={'pk': self.object.pk})
        path_edit = reverse_lazy(f'sweb:linbaremo_edit', kwargs={'pk0': self.object.pk, 'pk': 0})
        path_delete = reverse_lazy(f'sweb:linbaremo_delete', kwargs={'pk0': self.object.pk, 'pk': 0})
        context['edit_url2'] = path_edit.split('edit/0')[0]
        context['delete_url2'] = path_delete.split('delete/0')[0]
        # print(f'context: {context}')
        # print(f'edit_url2: {context["edit_url2"]}')
        return context


class BaremoDeleteView(BasicDeleteView, DeleteView):
    folder = 'baremo'
    model = Baremo
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        try:
            # print(f'Post: {request.POST}')
            action = request.POST['action']
            # diferenciamos si la paginación es en cliente o en servidor
            if action == 'searchdata_s':
                # Recuperamos las líneas que pertenzcan a la operación baremo a través de su id
                # activamos un segundo nivel de anidamiento de paginaciones con level_nesting=2
                datos = self.datatables_server(LineaBaremo, request, key_value=kwargs.get('pk'), level_nesting=2)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            return super().post(request, *args, **kwargs)

        return JsonResponse(datos, safe=False)


class BaremoDetailView(BasicDetailView, DetailView):
    folder = 'baremo'
    model = Baremo
    template_name = f'{folder}/detail.html'

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        try:
            # print(f'Post: {request.POST}')
            action = request.POST['action']
            # diferenciamos si la paginación es en cliente o en servidor
            if action == 'searchdata_s':
                # Recuperamos las líneas que pertenzcan a la operación baremo a través de su id
                # activamos un segundo nivel de anidamiento de paginaciones con level_nesting=2
                datos = self.datatables_server(LineaBaremo, request, key_value=kwargs.get('pk'), level_nesting=2)
            else:
                data = {'error': 'Ha ocurrido un error'}
        except Exception as e:
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Estamos en el primer nivel de anidamiento de paginaciones
        level_nesting = None
        # Gestionamos los botones de Anterior y Siguiente teniendo en cuenta las distintas posibilidades de ordenación
        # print(self.request.session.get('search'))
        # print(self.request.session.get('order_col_name'))
        order_col_name = self.request.session.get('order_col_name')
        if order_col_name == 'codigo':
            if self.object.codigo is None:
                filtro_prev = self.get_queryset().filter((Q(codigo__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(codigo__isnull=True) & Q(pk__gt=self.object.pk)) | Q(codigo__isnull=False)).order_by('codigo', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(codigo__lt=self.object.codigo) | (Q(codigo__exact=self.object.codigo) & Q(pk__lt=self.object.pk))) | Q(codigo__isnull=True)).order_by('-codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(codigo__gt=self.object.codigo)) | (Q(codigo__exact=self.object.codigo) & Q(pk__gt=self.object.pk))).order_by('codigo', 'id')
        elif order_col_name == '-codigo':
            if self.object.codigo is None:
                filtro_prev = self.get_queryset().filter((Q(codigo__isnull=True) & Q(pk__lt=self.object.pk)) | Q(codigo__isnull=False)).order_by('codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(codigo__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-codigo', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(codigo__gt=self.object.codigo)) | (Q(codigo__exact=self.object.codigo) & Q(pk__lt=self.object.pk))).order_by('codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(codigo__lt=self.object.codigo) | (Q(codigo__exact=self.object.codigo) & Q(pk__gt=self.object.pk))) | Q(codigo__isnull=True)).order_by('-codigo', 'id')
        elif order_col_name == 'descripcion':
            if self.object.descripcion is None:
                filtro_prev = self.get_queryset().filter((Q(descripcion__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(descripcion__isnull=True) & Q(pk__gt=self.object.pk)) | Q(descripcion__isnull=False)).order_by('descripcion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(descripcion__lt=self.object.descripcion) | (Q(descripcion__exact=self.object.descripcion) & Q(pk__lt=self.object.pk))) | Q(descripcion__isnull=True)).order_by('-descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(descripcion__gt=self.object.descripcion)) | (Q(descripcion__exact=self.object.descripcion) & Q(pk__gt=self.object.pk))).order_by('descripcion', 'id')
        elif order_col_name == '-descripcion':
            if self.object.descripcion is None:
                filtro_prev = self.get_queryset().filter((Q(descripcion__isnull=True) & Q(pk__lt=self.object.pk)) | Q(descripcion__isnull=False)).order_by('descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(descripcion__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-descripcion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(descripcion__gt=self.object.descripcion)) | (Q(descripcion__exact=self.object.descripcion) & Q(pk__lt=self.object.pk))).order_by('descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(descripcion__lt=self.object.descripcion) | (Q(descripcion__exact=self.object.descripcion) & Q(pk__gt=self.object.pk))) | Q(descripcion__isnull=True)).order_by('-descripcion', 'id')

        # print(f'filtro_prev: {filtro_prev}')
        # print(f'filtro_next: {filtro_next}')
        prev_pk = (filtro_prev.values('pk'))[:1]
        next_pk = (filtro_next.values('pk'))[:1]
        # print(f'prev_pk: {prev_pk}')
        # print(f'next_pk: {next_pk}')
        if prev_pk:
            context['prev_pk'] = prev_pk[0]['pk']
        if next_pk:
            context['next_pk'] = next_pk[0]['pk']

        return context
