from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import ProtectedError
from django.forms import *
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from core.models import BaseModel
from crum import get_current_user


class CodigoBaseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True

    def clean_codigo(self):
        # print('clean mixin')
        codigo = self.cleaned_data['codigo']
        if not codigo:
            raise ValidationError('El campo Código es obligatorio')

        # convertimos a mayúsculas
        codigo = codigo.upper()
        return codigo


# Redefinimos la función save para actualizar los campos de auditoría del user
class ModelMixin(BaseModel):

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # Incluimos el código para la auditoría
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user_creation = user
        else:
            self.user_updated = user

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class BasicView(View):

    # utilizamos un decorador para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # print(f'request: {request}')
        # print(f'args: {args}')
        # print(f'kwargs: {kwargs}')
        return super().dispatch(request, *args, **kwargs)

    # Paginación en servidor
    def datatables_server(self, model, request, modal=False, level_nesting=None, key_value=None):
        # Recuperarmos los datos enviados por POST en la llamada ajax con el parámetro serverSide: true
        datatables = request.POST
        # print(model)
        # print(f'datatables: {datatables}')
        draw = int(datatables.get('draw'))
        # print(f'draw: {draw}')
        start = int(datatables.get('start'))
        # print(f'start: {start}')
        length = int(datatables.get('length'))
        # print(f'length: {length}')
        search = datatables.get('search[value]')
        # print(f'search: {search}')
        order_idx = int(datatables.get('order[0][column]'))
        # print(f'order idx: {order_idx}')
        order_dir = datatables.get('order[0][dir]')
        # print(f'order dir: {order_dir}')
        order_col = 'columns[' + str(order_idx) + '][data]'
        # print(f'order_col: {order_col}')
        order_col_name = datatables.get(order_col)
        # print(f'order_col_name: {order_col_name}')
        if order_dir == "desc":
            order_col_name = str('-' + order_col_name)

        # guardamos info en sesión para la vista de detalle, botones Anterior y Siguiente
        # como podemos anidar paginaciones diferenciamos con level_nesting las variables en sesión
        if level_nesting is None:
            request.session['search'] = search
            request.session['order_col_name'] = order_col_name
        else:
            request.session['search'+'_'+str(level_nesting)] = search
            request.session['order_col_name'+'_'+str(level_nesting)] = order_col_name

        # key-value identifica la id cuando se usan paginaciones anidadas
        if search:
            if modal:
                data_objects = model.to_search_modal(model, value=search)
            elif key_value is not None:
                data_objects = model.to_search(model, value=search, key_value=key_value)
            else:
                data_objects = model.to_search(model, value=search)
        elif key_value is not None:
            data_objects = model.to_search(model, value=None, key_value=key_value)
        else:
            data_objects = model.objects.all()
        # print(f'data_objects: {data_objects}')
        records_total = data_objects.count()
        # print(f'records_total: {records_total}')
        records_filtered = records_total
        # print(f'records_filtered: {records_filtered}')
        data_objects = data_objects.order_by(order_col_name)
        # print(f'data_objects: {data_objects}')

        page_number = int(start / length) + 1
        # print(f'page_number: {page_number}')
        paginator = Paginator(data_objects, length)
        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list
        # print(f'object_list: {object_list}')
        data = []
        for i in object_list:
            if modal:
                data.append(i.to_list_modal())
            else:
                data.append(i.to_list())
        # print(f'data: {data}')
        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


class BasicListView(BasicView):

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        try:
            action = request.POST['action']
            # diferenciamos si la paginación es en cliente o en servidor
            if action == 'searchdata_c':
                datos = []
                # recuperamos solo los campos necesarios para la paginación
                for i in self.model.objects.all():
                    datos.append(i.to_list())
            elif action == 'searchdata_s':
                datos = self.datatables_server(self.model, request)
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
        context['title'] = self.model._meta.verbose_name_plural
        context['add_url'] = reverse_lazy(f'sweb:{self.folder}_add')
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['folder'] = self.folder
        return context


class BasicCreateView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Añadir {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['action'] = 'add'
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        context['folder'] = self.folder
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
        return super().form_valid(form)


class BasicUpdateView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        context['folder'] = self.folder
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
        return super().form_valid(form)


class BasicDeleteView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Borrar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        context['action'] = 'delete'
        context['folder'] = self.folder
        return context

    def form_valid(self, form):
        # print(f'BasicDeleteView')
        # Reescribimos form_valid para controlar los ProtectedError
        try:
            self.object.delete()
            messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
            return HttpResponseRedirect(self.success_url)
        except ProtectedError as e:
            messages.error(self.request,
                           f'{self.start_message_error} {self.model._meta.verbose_name} {self.end_message_error}')
            return self.render_to_response(context=self.get_context_data())


class BasicDetailView(BasicView):

    def get_queryset(self, level_nesting=None):
        # print('BasicDetailView-get_queryset')
        # print(f'model: {self.model}')
        # print(f'level_nesting: {level_nesting}')
        if level_nesting is None:
            search = self.request.session.get('search')
            order_col_name = self.request.session.get('order_col_name')
        else:
            search = self.request.session.get('search'+'_'+str(level_nesting))
            order_col_name = self.request.session.get('order_col_name'+'_'+str(level_nesting))
        # print(f'search: {search}')
        # print(f'order_col_name: {order_col_name}')
        if search is not None:
            data_objects = self.model.to_search(self.model, value=search)
        else:
            data_objects = self.model.objects.all()
        data_objects = data_objects.order_by(order_col_name)
        # print(data_objects)
        return data_objects

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        # print('BasicDetailView-get_context_data')
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalle {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        context['action'] = 'detail'
        context['folder'] = self.folder
        return context


class DescuentoRecambiosListView(BasicView):

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        try:
            action = request.POST['action']
            if action == 'searchdata_c':
                data = []
                # recuperamos solo los campos necesarios para la paginación
                for i in self.model.objects.filter(tipo=self.tipo):
                    data.append(i.to_list())
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
        context['title'] = self.model_verbose_plural
        context['add_url'] = reverse_lazy(f'sweb:{self.subfolder}_add')
        context['list_url'] = reverse_lazy(f'sweb:{self.subfolder}_list')
        context['entity_plural'] = self.model_verbose_plural
        context['entity'] = self.model_verbose_name
        context['folder'] = self.folder
        context['subfolder'] = self.subfolder
        return context


class DescuentoRecambiosCreateView(BasicView):

    def get_initial(self):
        initial = {
            'tipo': self.tipo,
        }
        return initial

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Añadir {self.model_verbose_name}'
        context['entity'] = self.model_verbose_plural
        context['action'] = 'add'
        context['list_url'] = reverse_lazy(f'sweb:{self.subfolder}_list')
        context['subfolder'] = self.subfolder
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model_verbose_name} {self.end_message_success}')
        return super().form_valid(form)


class DescuentoRecambiosUpdateView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar {self.model_verbose_name}'
        context['entity'] = self.model_verbose_plural
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy(f'sweb:{self.subfolder}_list')
        context['subfolder'] = self.subfolder
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model_verbose_name} {self.end_message_success}')
        return super().form_valid(form)


class DescuentoRecambiosDeleteView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Borrar {self.model_verbose_name}'
        context['entity'] = self.model_verbose_plural
        context['list_url'] = reverse_lazy(f'sweb:{self.subfolder}_list')
        context['action'] = 'delete'
        context['subfolder'] = self.subfolder
        return context

    def form_valid(self, form):
        # Reescribimos form_valid para controlar los ProtectedError
        try:
            self.object.delete()
            messages.success(self.request, f'{self.model_verbose_name} {self.end_message_success}')
            return HttpResponseRedirect(self.success_url)
        except ProtectedError as e:
            messages.error(self.request,
                           f'{self.start_message_error} {self.model_verbose_name} {self.end_message_error}')
            return self.render_to_response(context=self.get_context_data())


class LineaMovimientoForm(ModelForm):
    # Campos comunes a las líneas de movimiento, están asociados a la referencia
    ubicacion = CharField(label='Ubicación', required=False, disabled=True)
    codigoObsoleto = CharField(label='Frecuencia Venta', required=False, disabled=True)
    existencias = IntegerField(label='Existencias', required=False, disabled=True)
    pedidosPendientes = IntegerField(label='Pedidos Pendientes', required=False, disabled=True)
    reserva = IntegerField(label='Reserva', required=False, disabled=True)
    tarifa = DecimalField(label='P.V.P.', required=False, disabled=True)
    precioCosteMedio = DecimalField(label='Precio Coste Medio', required=False, disabled=True)
    precioCoste = DecimalField(label='P.V.D.', required=False, disabled=True)
    codigoApro = CharField(label='Descuento Aprov.', required=False, disabled=True)
    codigoUrgte = CharField(label='Descuento Urgente', required=False, disabled=True)
    familia = CharField(label='Familia', required=False, disabled=True)

    def datos_articulo(self, articulo):
        self.fields['existencias'].initial = articulo.existencias
        self.fields['ubicacion'].initial = articulo.ubicacion
        self.fields['codigoObsoleto'].initial = articulo.codigoObsoleto
        self.fields['pedidosPendientes'].initial = articulo.pedidosPendientes
        self.fields['reserva'].initial = articulo.reserva
        self.fields['tarifa'].initial = articulo.tarifa
        self.fields['precioCosteMedio'].initial = articulo.precioCosteMedio
        self.fields['precioCoste'].initial = articulo.precioCoste
        if articulo.codigoApro is None:
            codigoApro = None
        else:
            codigoApro = f'{articulo.codigoApro.codigo} - {articulo.codigoApro.codpieza} - {articulo.codigoApro.descuento}%'
        if articulo.codigoUrgte is None:
            codigoUrgte = None
        else:
            codigoUrgte = f'{articulo.codigoUrgte.codigo} - {articulo.codigoUrgte.codpieza} - {articulo.codigoUrgte.descuento}%'
        if articulo.familia is None:
            familia = None
        else:
            familia = f'{articulo.familia.codigo} - {articulo.familia.descripcion}'
        self.fields['codigoApro'].initial = codigoApro
        self.fields['codigoUrgte'].initial = codigoUrgte
        self.fields['familia'].initial = familia


class LineaMovimientoCreateView(BasicView):

    def get_initial(self):
        # Recuperamos la clave del registro de cabecera
        pk_movto = self.request.get_full_path().split('/')[4]
        movimiento_obj = self.movimiento.objects.get(pk=pk_movto)
        initial = {
            self.movimiento_field: movimiento_obj,
        }
        return initial

    # utilizamos un decorador para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # redefinimos el post para las operaciones con ajax
    def post(self, request, *args, **kwargs):
        # print(f'post: {request.POST}')
        # print(f'kwargs: {kwargs}')
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'formbase':
                action2 = request.POST['action2']
                if action2 == 'select2':
                    term = request.POST['term']
                    field = request.POST['field']
                    datos = []
                    if field == 'referencia':
                        referencias = self.artiulo_model.to_search_select(self.artiulo_model, term)
                        for i in referencias:
                            datos.append(i.to_list_select())
                elif action2 == 'referdata':
                    refid = request.POST['refid']
                    articulo = self.artiulo_model.objects.get(pk=refid)
                    if articulo is not None:
                        # Comprobamos si la referencia ha sido sustituida y no tiene existencias
                        if articulo.nuevaReferencia is not None and articulo.existencias <= 0:
                            nuevaReferencia = articulo.nuevaReferencia
                            articulo = self.artiulo_model.objects.get(referencia=nuevaReferencia)
                            sustituida = True
                            if articulo is None:
                                datos = {
                                    'error': 'Referencia no encontrada'
                                }
                        else:
                            sustituida = False

                        if articulo.codigoApro is None:
                            codigoApro = None
                        else:
                            codigoApro = f'{articulo.codigoApro.codigo} - {articulo.codigoApro.codpieza} - {articulo.codigoApro.descuento}%'
                        if articulo.codigoUrgte is None:
                            codigoUrgte = None
                        else:
                            codigoUrgte = f'{articulo.codigoUrgte.codigo} - {articulo.codigoUrgte.codpieza} - {articulo.codigoUrgte.descuento}%'
                        if articulo.familia is None:
                            familia = None
                        else:
                            familia = f'{articulo.familia.codigo} - {articulo.familia.descripcion}'
                        datos = {
                            'existencias': articulo.existencias,
                            'ubicacion': articulo.ubicacion,
                            'codigoObsoleto': articulo.codigoObsoleto,
                            'pedidosPendientes': articulo.pedidosPendientes,
                            'reserva': articulo.reserva,
                            'tarifa': articulo.tarifa,
                            'codigoApro': codigoApro,
                            'codigoUrgte': codigoUrgte,
                            'precioCosteMedio': articulo.precioCosteMedio,
                            'precioCoste': articulo.precioCoste,
                            'familia': familia,
                            'sustituida': sustituida,
                            'referencia': articulo.to_list_select()
                        }
                        # print(f'datos: {datos}')
                    else:
                        datos = {
                            'error': 'Referencia no encontrada'
                        }
                elif action2 == 'canceladd':
                    movto_id = kwargs['pk']
                    movto_id_field = self.movimiento_field + '_id'
                    # print(f'movto_id_field: {movto_id_field}')
                    lineas = self.model.objects.filter(**{movto_id_field: movto_id}).count()
                    # print(f'lineas: {lineas}')
                    if lineas == 0:
                        # print(f'Borramos cabecera')
                        movimiento_cab = self.movimiento.objects.get(pk=movto_id)
                        movimiento_cab.delete()
                        datos = {
                            'url': reverse_lazy(f'sweb:{self.list_view.folder}_list')
                        }
                        # print(datos)
                    else:
                        datos = {
                            'url': self.request.get_full_path().split(self.folder)[0]
                        }
                        # print(datos)
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