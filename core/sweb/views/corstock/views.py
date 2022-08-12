from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from core.sweb.forms import CorreccionStockForm
from core.sweb.models import CorreccionStock, LineaCorreccionStock, NumeracionAutomatica
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from django.db.models import Q
from datetime import datetime
from django.utils.timezone import get_current_timezone
from decouple import config
from django.contrib import messages


class CorreccionStockListView(BasicListView, ListView):
    folder = 'corstock'
    model = CorreccionStock
    template_name = f'{folder}/list.html'


class CorreccionStockCreateView(BasicCreateView, CreateView):
    folder = 'corstock'
    model = CorreccionStock
    form_class = CorreccionStockForm
    template_name = f'{folder}/create.html'
    # en el caso de las altas tenemos que redirigir al alta de líneas
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadida'

    def get_next_contador(self):
        codigo_numaut = '02'
        codigo = ''

        numautos = NumeracionAutomatica.objects.filter(codigo=codigo_numaut)
        if not numautos or numautos[0].activo is False:
            return codigo

        # si queremos que no haya espacios entre contadores debemos leerlos todos hasta encontrar el primero libre
        serie = numautos[0].serie
        # print(f'serie: {serie}')
        entradas = CorreccionStock.objects.filter(documento__startswith=serie).order_by('documento').values('documento')
        # print(f'entradas: {entradas}')
        nextnumber = 1
        for ent in entradas:
            numdoc = int(ent['documento'][2:])
            # print(f'doc: {numdoc}')
            if nextnumber < numdoc:
                codigo = str(nextnumber)
                codigo = codigo.strip().zfill(5)
                codigo = serie + codigo
                NumeracionAutomatica.objects.filter(codigo=codigo_numaut).update(contador=nextnumber)
                return codigo
            else:
                nextnumber += 1

        # no había huecos de modo que utilizamos el último número generado
        codigo = str(nextnumber)
        codigo = codigo.strip().zfill(5)
        codigo = serie + codigo
        NumeracionAutomatica.objects.filter(codigo=codigo_numaut).update(contador=nextnumber)
        return codigo

    def get_initial(self):
        # valores por defecto
        fechaMovimiento = datetime.now(tz=get_current_timezone()).strftime("%d/%m/%Y")
        documento = self.get_next_contador()

        initial = {
            'documento': documento,
            'fechaMovimiento': fechaMovimiento,
            'almacen': config('DEFALMA'),
        }
        return initial

    # Las altas de Corrección de Stock deben enlazar con las altas de líneas
    def get_success_url(self):
        # print(f'sweb:{self.folder}_list')
        return reverse_lazy(f'sweb:lincorstk_add', kwargs={'pk': self.object.pk})


class CorreccionStockUpdateView(BasicUpdateView, UpdateView):
    folder = 'corstock'
    model = CorreccionStock
    form_class = CorreccionStockForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificada'

    def get_initial(self):
        initial = {
            'fechaMovimiento': self.object.fechaMovimiento.strftime("%d/%m/%Y"),
        }
        return initial

    # redefinimos el post para las operaciones con ajax
    def post(self, request, *args, **kwargs):
        # print(f'post: {request.POST}')
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'search':
                action = request.POST['action']
                if action == 'searchdata_s':
                    # Recuperamos las líneas que pertenzcan a la entrada almacén a través de su id
                    # activamos un segundo nivel de anidamiento de paginaciones con level_nesting=2
                    datos = self.datatables_server(LineaCorreccionStock, request, key_value=kwargs.get('pk'),
                                                   level_nesting=2)
                else:
                    data = {'error': 'Ha ocurrido un error'}
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
        context['entity2'] = LineaCorreccionStock._meta.verbose_name
        context['add_url2'] = reverse_lazy(f'sweb:lincorstk_add', kwargs={'pk': self.object.pk})
        return context


class CorreccionStockDetailView(BasicDetailView, DetailView):
    folder = 'corstock'
    model = CorreccionStock
    template_name = f'{folder}/detail.html'

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        try:
            # print(f'Post: {request.POST}')
            action = request.POST['action']
            # diferenciamos si la paginación es en cliente o en servidor
            if action == 'searchdata_s':
                # Recuperamos las líneas que pertenzcan al movimiento a través de su id
                # activamos un segundo nivel de anidamiento de paginaciones con level_nesting=2
                datos = self.datatables_server(LineaCorreccionStock, request, key_value=kwargs.get('pk'), level_nesting=2)
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

        # algunos de los campos no son paginables en detail por su tipo, así que los ignoramos y salimos
        not_paginable = ['fechaMovimiento', '-fechaMovimiento', 'impreso', '-impreso']
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
