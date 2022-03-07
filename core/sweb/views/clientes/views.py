from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from core.sweb.forms import ClienteForm
from core.sweb.models import Cliente, TipoClienteRecambios, FormaDePago, DescuentoMO
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/list.html'

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # recuperamos solo los campos necesarios para la paginación
                for i in Cliente.objects.all().values('id', 'codigo', 'razonSocial', 'cif', 'telefono', 'tlfmovil', 'poblacion', 'provincia'):
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        context['add_url'] = reverse_lazy('sweb:clientes_add')
        context['list_url'] = reverse_lazy('sweb:clientes_list')
        context['entity'] = 'Clientes'
        return context


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/create.html'
    success_url = reverse_lazy('sweb:clientes_list')

    def get_initial(self):
        # valores por defecto
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

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Cliente'
        context['entity'] = 'Clientes'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('sweb:clientes_list')
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Cliente añadido')
        return super().form_valid(form)


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/create.html'
    success_url = reverse_lazy('sweb:clientes_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['entity'] = 'Clientes'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('sweb:clientes_list')
        return context

    def form_invalid(self, form):
        # print(f'form: {form.errors}')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Cliente modificado')
        return super().form_valid(form)


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/delete.html'
    success_url = reverse_lazy('sweb:clientes_list')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('sweb:clientes_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Cliente eliminado')
        return super().form_valid(form)


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/detail.html'

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('sweb:clientes_list')
        context['action'] = 'detail'
        return context
