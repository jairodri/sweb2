from django.http import JsonResponse
from django.urls import reverse_lazy
from decouple import config
from core.sweb.forms import ArticuloForm, TasaForm
from core.sweb.models import Articulo, UnidadMedida, CodigoAproPieza, PrecioTarifa, CodigoIva, CodigoContable, Tasa, TasaCodigo
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from datetime import datetime


class ArticuloListView(BasicListView, ListView):
    folder = 'articulos'
    model = Articulo
    template_name = f'{folder}/list.html'


class ArticuloCreateView(BasicCreateView, CreateView):
    folder = 'articulos'
    model = Articulo
    form_class = ArticuloForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'

    def get_initial(self):
        # valores por defecto
        unidadMedida = UnidadMedida.objects.get(codigo='1').id
        codAproPieza = CodigoAproPieza.objects.get(codigo='X').id
        ivaPieza = CodigoIva.objects.get(codigo='02').id
        codigoContable = CodigoContable.objects.get(codigo='01').id
        fechaAlta = datetime.now()
        # codigoApro = DescuentoRecambios.objects.filter(tipo='1', codpieza='?')
        # codigoUrgte = DescuentoRecambios.objects.filter(tipo='2', codpieza='?')
        # codigoPromo = DescuentoRecambios.objects.filter(tipo='3', codpieza='?')

        initial = {
            'existencias': 0,
            'tarifa': 0.00,
            'stockSeguridad': 0,
            'puntoPedido': 0,
            'stockMinimo': 0,
            'unidadCompra': 1,
            'unidadVenta': 1,
            'unidadStock': 1,
            'multiplo': 1,
            'codigoObsoleto': '0',
            'unidadMedida': unidadMedida,
            'codAproPieza': codAproPieza,
            'ivaPieza': ivaPieza,
            'codigoContable': codigoContable,
            'fechaAlta': fechaAlta,
            # 'codigoApro': [],
            # 'codigoUrgte': codigoUrgte,
            # 'codigoPromo': codigoPromo,
        }
        return initial

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        # print(f'post: {request.POST}')
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'listprecios':
                action = request.POST['action']
                if action == 'searchdata_s':
                    datos = self.datatables_server(PrecioTarifa, request, modal=True)
                else:
                    return super().post(request, *args, **kwargs)
            # elif tipo_ == 'proveedor':
            #     action = request.POST['action']
            #     if action == 'proveedor_s':
            #         pk = request.POST['pk']
            #         datos = Cliente.objects.values('dtopieza').get(pk=pk)
            #         codigoApro = DescuentoRecambios.objects.filter(tipo='1', codigo=datos['dtopieza'])
            #         datos['codigoApro'] = codigoApro
            #         print(datos)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    # en este caso la info de defclien
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['defclien'] = config('DEFCLIEN')
        # print(context)
        return context


class ArticuloUpdateView(BasicUpdateView, UpdateView):
    folder = 'articulos'
    model = Articulo
    form_class = ArticuloForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    formTasa = TasaForm()
    end_message_success = 'modificado'

    def get_initial(self):

        # Inicializamos el campo del form de tasa con filtrando por código contable
        codcontable = self.get_object().codigoContable
        self.formTasa.fields['codigoTasa'].queryset = TasaCodigo.objects.filter(codcontable=codcontable)

        initial = {
            'funcionCitroen': self.get_object().codigoFuncion,
        }
        return initial

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        print(request.POST)
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'formtasa':
                pk = kwargs['pk']
                action2 = request.POST['action2']
                if action2 == 'inittasa':
                    try:
                        tasa = Tasa.objects.get(referencia=pk)
                        datos = {
                            'denominacion': tasa.denominacion,
                            'precio': tasa.precio,
                            'descuento': tasa.descuento,
                        }
                    except Exception as exc:
                        datos = {
                            'denominacion': '',
                            'precio': 0,
                            'descuento': 0,
                        }
                elif action2 == 'edittasa':
                    denominacion = request.POST['denominacion']
                    precio = request.POST['precio']
                    descuento = request.POST['descuento']
                    # print(f'{denominacion} - {precio} - {descuento}')
                    try:
                        tasa = Tasa.objects.get(referencia=pk)
                    except Exception as exc:
                        tasa = Tasa()
                        articulo = Articulo.objects.get(id=pk)
                        tasa.referencia = articulo
                    tasa.denominacion = denominacion
                    tasa.precio = float(precio)
                    if descuento.strip() == '':
                        descuento = None
                    else:
                        descuento = float(descuento)
                    tasa.descuento = descuento
                    tasa.save()
                    datos = {
                        'message': 'Tasa actualizada'
                    }
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    # en este caso la info de defclien
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['defclien'] = config('DEFCLIEN')
        context['formtasa'] = self.formTasa
        return context


class ArticuloDeleteView(BasicDeleteView, DeleteView):
    folder = 'articulos'
    model = Articulo
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            precioTarifa = PrecioTarifa.objects.get(referencia=self.object.referencia)
            precioTarifa = precioTarifa.to_list()
        except Exception as ex:
            precioTarifa = None

        context['precioTarifa'] = precioTarifa
        context['defclien'] = config('DEFCLIEN')
        return context


class ArticuloDetailView(BasicDetailView, DetailView):
    folder = 'articulos'
    model = Articulo
    template_name = f'{folder}/detail.html'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            precioTarifa = PrecioTarifa.objects.get(referencia=self.object.referencia)
            precioTarifa = precioTarifa.to_list()
        except Exception as ex:
            precioTarifa = None

        context['precioTarifa'] = precioTarifa
        context['defclien'] = config('DEFCLIEN')
        return context
