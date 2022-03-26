from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from core.sweb.models import PrecioTarifa
from core.sweb.mixins import BasicListView, BasicView
import datetime


class PrecioTarifaListView(BasicView, ListView):
    folder = 'precios'
    model = PrecioTarifa
    template_name = f'{folder}/list.html'

    # def get(self, request, *args, **kwargs):
    #     print(request.GET)
    #     return super().get(request, *args, **kwargs)

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        # print(request.POST)
        datos = []
        try:
            action = request.POST['action']
            if action == 'searchdata':
                datos = self.datatables_server(request)
                # print(datos)
                # data = []
                # recuperamos solo los campos necesarios para la paginación
                # tiempo_inicial = datetime.datetime.now()
                # for i in self.model.objects.all():
                #     data.append(i.to_list())
                # tiempo_final = datetime.datetime.now()
                # tiempo_ejecucion = tiempo_final - tiempo_inicial
                # print(f'tiempo ejecución: {tiempo_ejecucion.total_seconds()}')
            else:
                datos = {'error': 'Ha ocurrido un error'}
        except Exception as e:
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)

    def datatables_server(self, request):
        # Recuperarmos los datos enviados por POST en la llamada ajax con el parámetro serverSide: true
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
            object_list = paginator.page(draw).object_list
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



