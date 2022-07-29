from django.http import JsonResponse
from django.urls import reverse_lazy
from core.sweb.forms import EntradaAlmacenForm
from core.sweb.models import EntradaAlmacen, LineaBaremo, NumeracionAutomatica, Cliente
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from django.db.models import Q
from datetime import datetime
from decouple import config


class EntradaAlmacenListView(BasicListView, ListView):
    folder = 'entalmacen'
    model = EntradaAlmacen
    template_name = f'{folder}/list.html'


class EntradaAlmacenCreateView(BasicCreateView, CreateView):
    folder = 'entalmacen'
    model = EntradaAlmacen
    form_class = EntradaAlmacenForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'

    def get_next_contador(self):
        codigo_numaut = '01'
        codigo = ''

        numautos = NumeracionAutomatica.objects.filter(codigo=codigo_numaut)
        if not numautos or numautos[0].activo is False:
            return codigo

        valido = False
        serie = numautos[0].serie
        nextnumber = numautos[0].contador
        while not valido:
            nextnumber = nextnumber + 1
            codigo = str(nextnumber)
            codigo = codigo.strip().zfill(5)
            codigo = serie + codigo
            entradaAlmacen = EntradaAlmacen.objects.filter(documento=codigo)
            if not entradaAlmacen:
                NumeracionAutomatica.objects.filter(codigo=codigo_numaut).update(contador=nextnumber)
                valido = True

        return codigo

    def get_initial(self):
        # valores por defecto
        fechaMovimiento = datetime.now()
        documento = self.get_next_contador()

        initial = {
            'documento': documento,
            'fechaMovimiento': fechaMovimiento,
            'almacen': config('DEFALMA'),
            'importePiCoste': 0.00,
        }
        return initial

    # redefinimos el post para las operaciones con ajax
    def post(self, request, *args, **kwargs):
        print(f'post: {request.POST}')
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'formbase':
                action2 = request.POST['action2']
                if action2 == 'select2':
                    term = request.POST['term']
                    field = request.POST['field']
                    datos = []
                    if field == 'proveedor':
                        proveedores = Cliente.to_search_select(Cliente, term)
                        for i in proveedores:
                            datos.append(i.to_list_select())
                else:
                    return super().post(request, *args, **kwargs)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            # return super().post(request, *args, **kwargs)
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)


class EntradaAlmacenUpdateView(BasicUpdateView, UpdateView):
    folder = 'entalmacen'
    model = EntradaAlmacen
    form_class = EntradaAlmacenForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'

    # redefinimos el post para las operaciones con ajax
    def post(self, request, *args, **kwargs):
        print(f'post: {request.POST}')
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'formbase':
                action2 = request.POST['action2']
                if action2 == 'select2':
                    term = request.POST['term']
                    field = request.POST['field']
                    datos = []
                    if field == 'proveedor':
                        proveedores = Cliente.to_search_select(Cliente, term)
                        for i in proveedores:
                            datos.append(i.to_list_select())
                else:
                    return super().post(request, *args, **kwargs)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            # return super().post(request, *args, **kwargs)
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)
#
#     # redefinimos el post para cargar la datatable con ajax
#     def post(self, request, *args, **kwargs):
#         try:
#             # print(f'Post: {request.POST}')
#             action = request.POST['action']
#             # diferenciamos si la paginación es en cliente o en servidor
#             if action == 'searchdata_s':
#                 # Recuperamos las líneas que pertenzcan a la operación baremo a través de su id
#                 # activamos un segundo nivel de anidamiento de paginaciones con level_nesting=2
#                 datos = self.datatables_server(LineaBaremo, request, key_value=kwargs.get('pk'), level_nesting=2)
#             else:
#                 return super().post(request, *args, **kwargs)
#         except Exception as e:
#             return super().post(request, *args, **kwargs)
#
#         return JsonResponse(datos, safe=False)
#
#     # sobreescribimos el método get_context_data para añadir info al contexto
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['entity2'] = LineaBaremo._meta.verbose_name
#         context['add_url2'] = reverse_lazy(f'sweb:linbaremo_add', kwargs={'pk': self.object.pk})
#         path_edit = reverse_lazy(f'sweb:linbaremo_edit', kwargs={'pk0': self.object.pk, 'pk': 0})
#         path_delete = reverse_lazy(f'sweb:linbaremo_delete', kwargs={'pk0': self.object.pk, 'pk': 0})
#         context['edit_url2'] = path_edit.split('edit/0')[0]
#         context['delete_url2'] = path_delete.split('delete/0')[0]
#         # print(f'context: {context}')
#         # print(f'edit_url2: {context["edit_url2"]}')
#         return context


class EntradaAlmacenDeleteView(BasicDeleteView, DeleteView):
    folder = 'entalmacen'
    model = EntradaAlmacen
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'
#
#     # redefinimos el post para cargar la datatable con ajax
#     def post(self, request, *args, **kwargs):
#         try:
#             # print(f'Post: {request.POST}')
#             action = request.POST['action']
#             # diferenciamos si la paginación es en cliente o en servidor
#             if action == 'searchdata_s':
#                 # Recuperamos las líneas que pertenzcan a la operación baremo a través de su id
#                 # activamos un segundo nivel de anidamiento de paginaciones con level_nesting=2
#                 datos = self.datatables_server(LineaBaremo, request, key_value=kwargs.get('pk'), level_nesting=2)
#             else:
#                 return super().post(request, *args, **kwargs)
#         except Exception as e:
#             return super().post(request, *args, **kwargs)
#
#         return JsonResponse(datos, safe=False)


class EntradaAlmacenDetailView(BasicDetailView, DetailView):
    folder = 'entalmacen'
    model = EntradaAlmacen
    template_name = f'{folder}/detail.html'
#
#     # redefinimos el post para cargar la datatable con ajax
#     def post(self, request, *args, **kwargs):
#         try:
#             # print(f'Post: {request.POST}')
#             action = request.POST['action']
#             # diferenciamos si la paginación es en cliente o en servidor
#             if action == 'searchdata_s':
#                 # Recuperamos las líneas que pertenzcan a la operación baremo a través de su id
#                 # activamos un segundo nivel de anidamiento de paginaciones con level_nesting=2
#                 datos = self.datatables_server(LineaBaremo, request, key_value=kwargs.get('pk'), level_nesting=2)
#             else:
#                 data = {'error': 'Ha ocurrido un error'}
#         except Exception as e:
#             datos = {
#                 'error': str(e)
#             }
#         return JsonResponse(datos, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Estamos en el primer nivel de anidamiento de paginaciones
        level_nesting = None
        # Gestionamos los botones de Anterior y Siguiente teniendo en cuenta las distintas posibilidades de ordenación
        # print(self.request.session.get('search'))
        # print(self.request.session.get('order_col_name'))
        order_col_name = self.request.session.get('order_col_name')

        # algunos de los campos no son paginables en detail por su tipo, así que los ignoramos y salimos
        not_paginable = ['fechaMovimiento', '-fechaMovimiento', 'importe', '-importe']
        if order_col_name in not_paginable:
            return context

        if order_col_name == 'documento':
            if self.object.documento is None:
                filtro_prev = self.get_queryset().filter((Q(documento__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-documento', '-id')
                filtro_next = self.get_queryset().filter((Q(documento__isnull=True) & Q(pk__gt=self.object.pk)) | Q(documento__isnull=False)).order_by('documento', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(documento__lt=self.object.documento) | (Q(documento__exact=self.object.documento) & Q(pk__lt=self.object.pk))) | Q(documento__isnull=True)).order_by('-documento', '-id')
                filtro_next = self.get_queryset().filter((Q(documento__gt=self.object.documento)) | (Q(documento__exact=self.object.documento) & Q(pk__gt=self.object.pk))).order_by('documento', 'id')
        elif order_col_name == '-documento':
            if self.object.documento is None:
                filtro_prev = self.get_queryset().filter((Q(documento__isnull=True) & Q(pk__lt=self.object.pk)) | Q(documento__isnull=False)).order_by('documento', '-id')
                filtro_next = self.get_queryset().filter((Q(documento__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-documento', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(documento__gt=self.object.documento)) | (Q(documento__exact=self.object.documento) & Q(pk__lt=self.object.pk))).order_by('documento', '-id')
                filtro_next = self.get_queryset().filter((Q(documento__lt=self.object.documento) | (Q(documento__exact=self.object.documento) & Q(pk__gt=self.object.pk))) | Q(documento__isnull=True)).order_by('-documento', 'id')
        elif order_col_name == 'albaranProveedor':
            if self.object.albaranProveedor is None:
                filtro_prev = self.get_queryset().filter((Q(albaranProveedor__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-albaranProveedor', '-id')
                filtro_next = self.get_queryset().filter((Q(albaranProveedor__isnull=True) & Q(pk__gt=self.object.pk)) | Q(albaranProveedor__isnull=False)).order_by('albaranProveedor', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(albaranProveedor__lt=self.object.albaranProveedor) | (Q(albaranProveedor__exact=self.object.albaranProveedor) & Q(pk__lt=self.object.pk))) | Q(albaranProveedor__isnull=True)).order_by('-albaranProveedor', '-id')
                filtro_next = self.get_queryset().filter((Q(albaranProveedor__gt=self.object.albaranProveedor)) | (Q(albaranProveedor__exact=self.object.albaranProveedor) & Q(pk__gt=self.object.pk))).order_by('albaranProveedor', 'id')
        elif order_col_name == '-albaranProveedor':
            if self.object.albaranProveedor is None:
                filtro_prev = self.get_queryset().filter((Q(albaranProveedor__isnull=True) & Q(pk__lt=self.object.pk)) | Q(albaranProveedor__isnull=False)).order_by('albaranProveedor', '-id')
                filtro_next = self.get_queryset().filter((Q(albaranProveedor__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-albaranProveedor', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(albaranProveedor__gt=self.object.albaranProveedor)) | (Q(albaranProveedor__exact=self.object.albaranProveedor) & Q(pk__lt=self.object.pk))).order_by('albaranProveedor', '-id')
                filtro_next = self.get_queryset().filter((Q(albaranProveedor__lt=self.object.albaranProveedor) | (Q(albaranProveedor__exact=self.object.albaranProveedor) & Q(pk__gt=self.object.pk))) | Q(albaranProveedor__isnull=True)).order_by('-albaranProveedor', 'id')
        elif order_col_name == 'proveedor__codigo':
            if self.object.proveedor is None:
                filtro_prev = self.get_queryset().filter((Q(proveedor__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-proveedor__codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(proveedor__isnull=True) & Q(pk__gt=self.object.pk)) | Q(proveedor__isnull=False)).order_by('proveedor__codigo', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(proveedor__codigo__lt=self.object.proveedor.codigo) | (Q(proveedor__codigo__exact=self.object.proveedor.codigo) & Q(pk__lt=self.object.pk))) | Q(proveedor__isnull=True)).order_by('-proveedor__codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(proveedor__codigo__gt=self.object.proveedor.codigo)) | (Q(proveedor__codigo__exact=self.object.proveedor.codigo) & Q(pk__gt=self.object.pk))).order_by('proveedor__codigo', 'id')
        elif order_col_name == '-proveedor__codigo':
            if self.object.proveedor is None:
                filtro_prev = self.get_queryset().filter((Q(proveedor__codigo__isnull=True) & Q(pk__lt=self.object.pk)) | Q(proveedor__codigo__isnull=False)).order_by('proveedor__codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(proveedor__codigo__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-proveedor__codigo', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(proveedor__codigo__gt=self.object.proveedor.codigo)) | (Q(proveedor__codigo__exact=self.object.proveedor.codigo) & Q(pk__lt=self.object.pk))).order_by('proveedor__codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(proveedor__codigo__lt=self.object.proveedor.codigo) | (Q(proveedor__codigo__exact=self.object.proveedor.codigo) & Q(pk__gt=self.object.pk))) | Q(proveedor__codigo__isnull=True)).order_by('-proveedor__codigo', 'id')

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
