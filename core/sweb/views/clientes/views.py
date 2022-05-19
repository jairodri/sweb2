from django.http import JsonResponse
from django.urls import reverse_lazy
from decouple import config
from core.sweb.forms import ClienteForm, ClientLopdForm
from core.sweb.models import Cliente, TipoClienteRecambios, FormaDePago, DescuentoMO, NumeracionAutomatica
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from django.db.models import Q


class ClienteListView(BasicListView, ListView):
    folder = 'clientes'
    model = Cliente
    template_name = f'{folder}/list.html'


class ClienteCreateView(BasicCreateView, CreateView):
    folder = 'clientes'
    model = Cliente
    form_class = ClienteForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'

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


class ClienteUpdateView(BasicUpdateView, UpdateView):
    folder = 'clientes'
    model = Cliente
    form_class = ClienteForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    formLopd = ClientLopdForm()
    end_message_success = 'modificado'

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
    # en este caso la info de lopd
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['defclien'] = config('DEFCLIEN')
        # enviamos también el formulario LOPD por si es necesario
        context['formlopd'] = self.formLopd
        return context


class ClienteDeleteView(BasicDeleteView, DeleteView):
    folder = 'clientes'
    model = Cliente
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class ClienteDetailView(BasicDetailView, DetailView):
    folder = 'clientes'
    model = Cliente
    template_name = f'{folder}/detail.html'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['defclien'] = config('DEFCLIEN')

        # Gestionamos los botones de Anterior y Siguiente teniendo en cuenta las distintas posibilidades de orderación
        # print(self.request.session.get('search'))
        # print(self.request.session.get('order_col_name'))
        order_col_name = self.request.session.get('order_col_name')
        if order_col_name == 'codigo':
            filtro_prev = self.get_queryset().filter(Q(codigo__lt=self.object.codigo)).order_by('-codigo')
            filtro_next = self.get_queryset().filter(Q(codigo__gt=self.object.codigo)).order_by('codigo')
        elif order_col_name == '-codigo':
            filtro_prev = self.get_queryset().filter(Q(codigo__gt=self.object.codigo)).order_by('codigo')
            filtro_next = self.get_queryset().filter(Q(codigo__lt=self.object.codigo)).order_by('-codigo')
        elif order_col_name == 'razonSocial':
            if self.object.razonSocial is None:
                filtro_prev = self.get_queryset().filter((Q(razonSocial__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-razonSocial', '-id')
                filtro_next = self.get_queryset().filter((Q(razonSocial__isnull=True) & Q(pk__gt=self.object.pk)) | Q(razonSocial__isnull=False)).order_by('razonSocial', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(razonSocial__lt=self.object.razonSocial) | (Q(razonSocial__exact=self.object.razonSocial) & Q(pk__lt=self.object.pk))) | Q(razonSocial__isnull=True)).order_by('-razonSocial', '-id')
                filtro_next = self.get_queryset().filter((Q(razonSocial__gt=self.object.razonSocial)) | (Q(razonSocial__exact=self.object.razonSocial) & Q(pk__gt=self.object.pk))).order_by('razonSocial', 'id')
        elif order_col_name == '-razonSocial':
            if self.object.razonSocial is None:
                filtro_prev = self.get_queryset().filter((Q(razonSocial__isnull=True) & Q(pk__lt=self.object.pk)) | Q(razonSocial__isnull=False)).order_by('razonSocial', '-id')
                filtro_next = self.get_queryset().filter((Q(razonSocial__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-razonSocial', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(razonSocial__gt=self.object.razonSocial)) | (Q(razonSocial__exact=self.object.razonSocial) & Q(pk__lt=self.object.pk))).order_by('razonSocial', '-id')
                filtro_next = self.get_queryset().filter((Q(razonSocial__lt=self.object.razonSocial) | (Q(razonSocial__exact=self.object.razonSocial) & Q(pk__gt=self.object.pk))) | Q(razonSocial__isnull=True)).order_by('-razonSocial', 'id')
        elif order_col_name == 'cif':
            if self.object.cif is None:
                filtro_prev = self.get_queryset().filter((Q(cif__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-cif', '-id')
                filtro_next = self.get_queryset().filter((Q(cif__isnull=True) & Q(pk__gt=self.object.pk)) | Q(cif__isnull=False)).order_by('cif', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(cif__lt=self.object.cif) | (Q(cif__exact=self.object.cif) & Q(pk__lt=self.object.pk))) | Q(cif__isnull=True)).order_by('-cif', '-id')
                filtro_next = self.get_queryset().filter((Q(cif__gt=self.object.cif)) | (Q(cif__exact=self.object.cif) & Q(pk__gt=self.object.pk))).order_by('cif', 'id')
        elif order_col_name == '-cif':
            if self.object.cif is None:
                filtro_prev = self.get_queryset().filter((Q(cif__isnull=True) & Q(pk__lt=self.object.pk)) | Q(cif__isnull=False)).order_by('cif', '-id')
                filtro_next = self.get_queryset().filter((Q(cif__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-cif', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(cif__gt=self.object.cif)) | (Q(cif__exact=self.object.cif) & Q(pk__lt=self.object.pk))).order_by('cif', '-id')
                filtro_next = self.get_queryset().filter((Q(cif__lt=self.object.cif) | (Q(cif__exact=self.object.cif) & Q(pk__gt=self.object.pk))) | Q(cif__isnull=True)).order_by('-cif', 'id')
        elif order_col_name == 'telefono':
            if self.object.telefono is None:
                filtro_prev = self.get_queryset().filter((Q(telefono__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-telefono', '-id')
                filtro_next = self.get_queryset().filter((Q(telefono__isnull=True) & Q(pk__gt=self.object.pk)) | Q(telefono__isnull=False)).order_by('telefono', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(telefono__lt=self.object.telefono) | (Q(telefono__exact=self.object.telefono) & Q(pk__lt=self.object.pk))) | Q(telefono__isnull=True)).order_by('-telefono', '-id')
                filtro_next = self.get_queryset().filter((Q(telefono__gt=self.object.telefono)) | (Q(telefono__exact=self.object.telefono) & Q(pk__gt=self.object.pk))).order_by('telefono', 'id')
        elif order_col_name == '-telefono':
            if self.object.telefono is None:
                filtro_prev = self.get_queryset().filter((Q(telefono__isnull=True) & Q(pk__lt=self.object.pk)) | Q(telefono__isnull=False)).order_by('telefono', '-id')
                filtro_next = self.get_queryset().filter((Q(telefono__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-telefono', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(telefono__gt=self.object.telefono)) | (Q(telefono__exact=self.object.telefono) & Q(pk__lt=self.object.pk))).order_by('telefono', '-id')
                filtro_next = self.get_queryset().filter((Q(telefono__lt=self.object.telefono) | (Q(telefono__exact=self.object.telefono) & Q(pk__gt=self.object.pk))) | Q(telefono__isnull=True)).order_by('-telefono', 'id')
        elif order_col_name == 'tlfmovil':
            if self.object.tlfmovil is None:
                filtro_prev = self.get_queryset().filter((Q(tlfmovil__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-tlfmovil', '-id')
                filtro_next = self.get_queryset().filter((Q(tlfmovil__isnull=True) & Q(pk__gt=self.object.pk)) | Q(tlfmovil__isnull=False)).order_by('tlfmovil', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(tlfmovil__lt=self.object.tlfmovil) | (Q(tlfmovil__exact=self.object.tlfmovil) & Q(pk__lt=self.object.pk))) | Q(tlfmovil__isnull=True)).order_by('-tlfmovil', '-id')
                filtro_next = self.get_queryset().filter((Q(tlfmovil__gt=self.object.tlfmovil)) | (Q(tlfmovil__exact=self.object.tlfmovil) & Q(pk__gt=self.object.pk))).order_by('tlfmovil', 'id')
        elif order_col_name == '-tlfmovil':
            if self.object.tlfmovil is None:
                filtro_prev = self.get_queryset().filter((Q(tlfmovil__isnull=True) & Q(pk__lt=self.object.pk)) | Q(tlfmovil__isnull=False)).order_by('tlfmovil', '-id')
                filtro_next = self.get_queryset().filter((Q(tlfmovil__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-tlfmovil', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(tlfmovil__gt=self.object.tlfmovil)) | (Q(tlfmovil__exact=self.object.tlfmovil) & Q(pk__lt=self.object.pk))).order_by('tlfmovil', '-id')
                filtro_next = self.get_queryset().filter((Q(tlfmovil__lt=self.object.tlfmovil) | (Q(tlfmovil__exact=self.object.tlfmovil) & Q(pk__gt=self.object.pk))) | Q(tlfmovil__isnull=True)).order_by('-tlfmovil', 'id')
        elif order_col_name == 'poblacion':
            if self.object.poblacion is None:
                filtro_prev = self.get_queryset().filter((Q(poblacion__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-poblacion', '-id')
                filtro_next = self.get_queryset().filter((Q(poblacion__isnull=True) & Q(pk__gt=self.object.pk)) | Q(poblacion__isnull=False)).order_by('poblacion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(poblacion__lt=self.object.poblacion) | (Q(poblacion__exact=self.object.poblacion) & Q(pk__lt=self.object.pk))) | Q(poblacion__isnull=True)).order_by('-poblacion', '-id')
                filtro_next = self.get_queryset().filter((Q(poblacion__gt=self.object.poblacion)) | (Q(poblacion__exact=self.object.poblacion) & Q(pk__gt=self.object.pk))).order_by('poblacion', 'id')
        elif order_col_name == '-poblacion':
            if self.object.poblacion is None:
                filtro_prev = self.get_queryset().filter((Q(poblacion__isnull=True) & Q(pk__lt=self.object.pk)) | Q(poblacion__isnull=False)).order_by('poblacion', '-id')
                filtro_next = self.get_queryset().filter((Q(poblacion__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-poblacion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(poblacion__gt=self.object.poblacion)) | (Q(poblacion__exact=self.object.poblacion) & Q(pk__lt=self.object.pk))).order_by('poblacion', '-id')
                filtro_next = self.get_queryset().filter((Q(poblacion__lt=self.object.poblacion) | (Q(poblacion__exact=self.object.poblacion) & Q(pk__gt=self.object.pk))) | Q(poblacion__isnull=True)).order_by('-poblacion', 'id')
        elif order_col_name == 'provincia':
            if self.object.provincia is None:
                filtro_prev = self.get_queryset().filter((Q(provincia__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-provincia', '-id')
                filtro_next = self.get_queryset().filter((Q(provincia__isnull=True) & Q(pk__gt=self.object.pk)) | Q(provincia__isnull=False)).order_by('provincia', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(provincia__lt=self.object.provincia) | (Q(provincia__exact=self.object.provincia) & Q(pk__lt=self.object.pk))) | Q(provincia__isnull=True)).order_by('-provincia', '-id')
                filtro_next = self.get_queryset().filter((Q(provincia__gt=self.object.provincia)) | (Q(provincia__exact=self.object.provincia) & Q(pk__gt=self.object.pk))).order_by('provincia', 'id')
        elif order_col_name == '-provincia':
            if self.object.provincia is None:
                filtro_prev = self.get_queryset().filter((Q(provincia__isnull=True) & Q(pk__lt=self.object.pk)) | Q(provincia__isnull=False)).order_by('provincia', '-id')
                filtro_next = self.get_queryset().filter((Q(provincia__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-provincia', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(provincia__gt=self.object.provincia)) | (Q(provincia__exact=self.object.provincia) & Q(pk__lt=self.object.pk))).order_by('provincia', '-id')
                filtro_next = self.get_queryset().filter((Q(provincia__lt=self.object.provincia) | (Q(provincia__exact=self.object.provincia) & Q(pk__gt=self.object.pk))) | Q(provincia__isnull=True)).order_by('-provincia', 'id')

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
