from django.http import JsonResponse
from django.urls import reverse_lazy
from decouple import config
from core.sweb.forms import ArticuloForm
from core.sweb.models import Articulo, UnidadMedida, CodigoAproPieza
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
        fechaAlta = datetime.now()

        initial = {
            'stockSeguridad': 0,
            'puntoPedido': 0,
            'stockMinimo': 0,
            'unidadCompra': 1,
            'unidadVenta': 1,
            'unidadStock': 1,
            'multiplo': 1,
            'unidadMedida': unidadMedida,
            'codAproPieza': codAproPieza,
            'fechaAlta': fechaAlta,
        }
        return initial


class ArticuloUpdateView(BasicUpdateView, UpdateView):
    folder = 'articulos'
    model = Articulo
    form_class = ArticuloForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'
#
#     # redefinimos el post para la gestión del modal de LOPD
#     def post(self, request, *args, **kwargs):
#         try:
#             data = {}
#             # print(request.POST)
#             tipo_form = request.POST['tipo_form']
#             if tipo_form == 'formlopd':
#                 action2 = request.POST['action2']
#                 pk = kwargs['pk']
#                 if action2 == 'initlopd':
#                     # recuperamos los datos de LOPD
#                     data = Cliente.objects.all().values('lopd1', 'lopd2', 'lopd3', 'lopdfirma').get(id=pk)
#                 elif action2 == 'editlopd':
#                     clienteLopd = Cliente.objects.get(id=pk)
#                     # los boolean llegan en minúsculas de modo que hay que utilizar capitalize()
#                     # utilizamos eval para convertir el string a boolean
#                     clienteLopd.lopd1 = eval(request.POST['lopd1'].capitalize())
#                     clienteLopd.lopd2 = eval(request.POST['lopd2'].capitalize())
#                     clienteLopd.lopd3 = eval(request.POST['lopd3'].capitalize())
#                     clienteLopd.lopdfirma = eval(request.POST['lopdfirma'].capitalize())
#
#                     if clienteLopd.lopd1 is True and clienteLopd.lopd2 is True and clienteLopd.lopd3 is True:
#                         clienteLopd.exentoMail = False
#                     elif clienteLopd.lopd1 is False or clienteLopd.lopd2 is False or clienteLopd.lopd3 is False:
#                         clienteLopd.exentoMail = True
#
#                     clienteLopd.save()
#                     data = {
#                         'exentoMail': clienteLopd.exentoMail
#                     }
#             else:
#                 return super().post(request, *args, **kwargs)
#         except Exception as e:
#             print(e)
#             data = {
#                 'error': str(e)
#             }
#
#         # print(data)
#         return JsonResponse(data, safe=False)
#
#     # sobreescribimos el método get_context_data para añadir info al contexto
#     # en este caso la info de lopd
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['defclien'] = config('DEFCLIEN')
#         # enviamos también el formulario LOPD por si es necesario
#         context['formlopd'] = self.formLopd
#         return context
#
#
# class ClienteDeleteView(BasicDeleteView, DeleteView):
#     folder = 'clientes'
#     model = Cliente
#     template_name = f'{folder}/delete.html'
#     success_url = reverse_lazy(f'sweb:{folder}_list')
#     end_message_success = 'eliminado'
#     start_message_error = 'No se puede borrar este'
#     end_message_error = 'porque está siendo utilizado en otra tabla'
#
#
# class ClienteDetailView(BasicDetailView, DetailView):
#     folder = 'clientes'
#     model = Cliente
#     template_name = f'{folder}/detail.html'
#
#     # sobreescribimos el método get_context_data para añadir info al contexto
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['defclien'] = config('DEFCLIEN')
#         return context
