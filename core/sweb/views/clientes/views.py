from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from decouple import config
from core.sweb.forms import ClienteForm, ClientLopdForm
from core.sweb.models import Cliente, TipoClienteRecambios, FormaDePago, DescuentoMO, NumeracionAutomatica
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicView

folder = 'clientes'


class ClienteListView(BasicView, ListView):
    model = Cliente
    template_name = f'{folder}/list.html'

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        # data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # recuperamos solo los campos necesarios para la paginación
                for i in Cliente.objects.all().values('id', 'codigo', 'razonSocial', 'cif', 'telefono', 'tlfmovil', 'poblacion', 'provincia'):
                    data.append(i)
            else:
                data = {'error': 'Ha ocurrido un error'}
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Cliente._meta.verbose_name_plural
        context['add_url'] = reverse_lazy(f'sweb:{folder}_add')
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        context['entity'] = Cliente._meta.verbose_name_plural
        return context


class ClienteCreateView(BasicView, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')

    def get_next_contador(self):
        codigo_numaut = '00'
        codigo = ''

        numautos = NumeracionAutomatica.objects.filter(codigo=codigo_numaut)
        if not numautos or numautos[0].activo is False:
            return codigo

        valido = False
        nextnumber = numautos[0].contador
        while not valido:
            nextnumber = nextnumber + 1
            codigo = str(nextnumber)
            codigo = codigo.strip().zfill(6)
            cliente = Cliente.objects.filter(codigo=codigo)
            if not cliente:
                NumeracionAutomatica.objects.filter(codigo=codigo_numaut).update(contador=nextnumber)
                valido = True

        return codigo

    def get_initial(self):
        # valores por defecto
        codigo = self.get_next_contador()
        tipo_cl = TipoClienteRecambios.objects.get(codigo='CL').id
        forma_pago = FormaDePago.objects.get(codigo='00').id
        dtomo = DescuentoMO.objects.get(codigo='0').id
        dtopieza = '0'
        diaPagoDesde = 1
        diaPagoHasta = 31
        bloquearCredito = True
        emitirRecibos = True
        aplicarIva = True
        listarnetodto = True
        ocultarCuenta = True
        # confirm_cif = False
        ivaEpecial = 0.00
        dtoEpecial = 0.00
        creditoDisponible = 0.00
        initial = {
            'codigo': codigo,
            'tipoCliente': tipo_cl,
            'formaDePago': forma_pago,
            'dtomo': dtomo,
            'dtopieza': dtopieza,
            'diaPagoDesde': diaPagoDesde,
            'diaPagoHasta': diaPagoHasta,
            'bloquearCredito': bloquearCredito,
            'emitirRecibos': emitirRecibos,
            'aplicarIva': aplicarIva,
            'listarnetodto': listarnetodto,
            'ocultarCuenta': ocultarCuenta,
            'ivaEpecial': ivaEpecial,
            'dtoEpecial': dtoEpecial,
            'creditoDisponible': creditoDisponible,
            # 'confirm_cif': confirm_cif,
        }
        return initial

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Añadir {Cliente._meta.verbose_name}'
        context['entity'] = Cliente._meta.verbose_name_plural
        context['action'] = 'add'
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f'{Cliente._meta.verbose_name} añadido')
        return super().form_valid(form)


class ClienteUpdateView(BasicView, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    formLopd = ClientLopdForm()

    # redefinimos el post para la gestión del modal de LOPD
    def post(self, request, *args, **kwargs):
        try:
            data = {}
            # print(request.POST)
            tipo_form = request.POST['tipo_form']
            if tipo_form == 'formlopd':
                action2 = request.POST['action2']
                pk = kwargs['pk']
                if action2 == 'initlopd':
                    # recuperamos los datos de LOPD
                    data = Cliente.objects.all().values('lopd1', 'lopd2', 'lopd3', 'lopdfirma').get(id=pk)
                elif action2 == 'editlopd':
                    clienteLopd = Cliente.objects.get(id=pk)
                    # los boolean llegan en minúsculas de modo que hay que utilizar capitalize()
                    # utilizamos eval para convertir el string a boolean
                    clienteLopd.lopd1 = eval(request.POST['lopd1'].capitalize())
                    clienteLopd.lopd2 = eval(request.POST['lopd2'].capitalize())
                    clienteLopd.lopd3 = eval(request.POST['lopd3'].capitalize())
                    clienteLopd.lopdfirma = eval(request.POST['lopdfirma'].capitalize())

                    if clienteLopd.lopd1 is True and clienteLopd.lopd2 is True and clienteLopd.lopd3 is True:
                        clienteLopd.exentoMail = False
                    elif clienteLopd.lopd1 is False or clienteLopd.lopd2 is False or clienteLopd.lopd3 is False:
                        clienteLopd.exentoMail = True

                    clienteLopd.save()
                    data = {
                        'exentoMail': clienteLopd.exentoMail
                    }
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            print(e)
            data = {
                'error': str(e)
            }

        # print(data)
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar {Cliente._meta.verbose_name}'
        context['entity'] = Cliente._meta.verbose_name_plural
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        context['defclien'] = config('DEFCLIEN')
        # enviamos también el formulario LOPD por si es necesario
        context['formlopd'] = self.formLopd
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f'{Cliente._meta.verbose_name} modificado')
        return super().form_valid(form)


class ClienteDeleteView(BasicView, DeleteView):
    model = Cliente
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Borrar {Cliente._meta.verbose_name}'
        context['entity'] = Cliente._meta.verbose_name_plural
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        # Reescribimos form_valid para controlar los ProtectedError
        try:
            self.object.delete()
            messages.success(self.request, f'{Cliente._meta.verbose_name} eliminado')
            return HttpResponseRedirect(self.success_url)
        except ProtectedError as e:
            messages.error(self.request,
                           f'No se puede borrar este {Cliente._meta.verbose_name} porque está siendo utilizado en otra tabla')
            return self.render_to_response(context=self.get_context_data())
        # messages.add_message(self.request, messages.SUCCESS, 'Cliente eliminado')
        # return super().form_valid(form)


class ClienteDetailView(BasicView, DetailView):
    model = Cliente
    template_name = f'{folder}/detail.html'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalle {Cliente._meta.verbose_name}'
        context['entity'] = Cliente._meta.verbose_name_plural
        context['list_url'] = reverse_lazy(f'sweb:{folder}_list')
        context['action'] = 'detail'
        context['defclien'] = config('DEFCLIEN')
        return context
