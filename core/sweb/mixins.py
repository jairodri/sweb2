from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import ProtectedError
from django.forms import ModelForm
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
        return super().dispatch(request, *args, **kwargs)


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
                datos = self.datatables_server(request)
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

    def datatables_server(self, request):
        # Recuperarmos los datos enviados por POST en la llamada ajax con el parámetro serverSide: true
        # < QueryDict:
        # {
        #     'draw': ['1'],
        #     'columns[0][data]': ['referencia'],
        #     'columns[0][name]': [''],
        #     'columns[0][searchable]': ['true'],
        #     'columns[0][orderable]': ['true'],
        #     'columns[0][search][value]': [''],
        #     'columns[0][search][regex]': ['false'],
        #     'columns[1][data]': ['denominacion'],
        #     'columns[1][name]': [''],
        #     'columns[1][searchable]': ['true'],
        #     'columns[1][orderable]': ['true'],
        #     'columns[1][search][value]': [''],
        #     'columns[1][search][regex]': ['false'],
        #     'columns[2][data]': ['f9'],
        #     'columns[2][name]': [''],
        #     'columns[2][searchable]': ['true'],
        #     'columns[2][orderable]': ['true'],
        #     'columns[2][search][value]': [''],
        #     'columns[2][search][regex]': ['false'],
        #     'columns[3][data]': ['nuevaReferencia'],
        #     'columns[3][name]': [''],
        #     'columns[3][searchable]': ['true'],
        #     'columns[3][orderable]': ['true'],
        #     'columns[3][search][value]': [''],
        #     'columns[3][search][regex]': ['false'],
        #     'columns[4][data]': ['pvp1'],
        #     'columns[4][name]': [''],
        #     'columns[4][searchable]': ['true'],
        #     'columns[4][orderable]': ['true'],
        #     'columns[4][search][value]': [''],
        #     'columns[4][search][regex]': ['false'],
        #     'columns[5][data]': ['multiplo'],
        #     'columns[5][name]': [''],
        #     'columns[5][searchable]': ['true'],
        #     'columns[5][orderable]': ['true'],
        #     'columns[5][search][value]': [''],
        #     'columns[5][search][regex]': ['false'],
        #     'columns[6][data]': ['codigoDescuento'],
        #     'columns[6][name]': [''],
        #     'columns[6][searchable]': ['true'],
        #     'columns[6][orderable]': ['true'],
        #     'columns[6][search][value]': [''],
        #     'columns[6][search][regex]': ['false'],
        #     'columns[7][data]': ['penetracion'],
        #     'columns[7][name]': [''],
        #     'columns[7][searchable]': ['true'],
        #     'columns[7][orderable]': ['true'],
        #     'columns[7][search][value]': [''],
        #     'columns[7][search][regex]': ['false'],
        #     'columns[8][data]': ['familiaMarketing'],
        #     'columns[8][name]': [''],
        #     'columns[8][searchable]': ['true'],
        #     'columns[8][orderable]': ['true'],
        #     'columns[8][search][value]': [''],
        #     'columns[8][search][regex]': ['false'],
        #     'columns[9][data]': ['f1'],
        #     'columns[9][name]': [''],
        #     'columns[9][searchable]': ['true'],
        #     'columns[9][orderable]': ['true'],
        #     'columns[9][search][value]': [''],
        #     'columns[9][search][regex]': ['false'],
        #     'order[0][column]': ['0'],
        #     'order[0][dir]': ['asc'],
        #     'start': ['0'],
        #     'length': ['10'],
        #     'search[value]': [''],
        #     'search[regex]': ['false'],
        #     'action': ['searchdata']
        # } >
        datatables = request.POST
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
        order_col_name = datatables.get(order_col)
        # print(f'order_col_name: {order_col_name}')
        if order_dir == "desc":
            order_col_name = str('-' + order_col_name)

        if search:
            data_objects = self.model.to_search(self.model,value=search)
        else:
            data_objects = self.model.objects.all()
        records_total = data_objects.count()
        records_filtered = records_total
        data_objects = data_objects.order_by(order_col_name)

        page_number = int(start / length) + 1
        # print(f'page_number: {page_number}')
        paginator = Paginator(data_objects, length)
        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list

        data = []
        for i in object_list:
            data.append(i.to_list())

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


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

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
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