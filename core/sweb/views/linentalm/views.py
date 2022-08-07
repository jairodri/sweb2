from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from core.sweb.forms import LineaEntradaAlmacenForm
from core.sweb.models import LineaEntradaAlmacen, EntradaAlmacen, Articulo
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.sweb.views.entalmacen.views import EntradaAlmacenListView
from datetime import datetime
from django.utils.timezone import get_current_timezone


class LineaEntradaAlmacenCreateView(CreateView):
    folder = 'linentalm'
    model = LineaEntradaAlmacen
    form_class = LineaEntradaAlmacenForm
    template_name = f'{folder}/create.html'
    # success_url = ''
    end_message_success = 'añadida'

    def get_initial(self):
        # Recuperamos la clave del registro de cabecera
        pk_entalmacen = self.request.get_full_path().split('/')[4]
        entradaAlmacen = EntradaAlmacen.objects.get(pk=pk_entalmacen)
        initial = {
            'entradaAlmacen': entradaAlmacen,
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
                        referencias = Articulo.to_search_select(Articulo, term)
                        for i in referencias:
                            datos.append(i.to_list_select())
                elif action2 == 'referdata':
                    refid = request.POST['refid']
                    articulo = Articulo.objects.get(pk=refid)
                    if articulo is not None:
                        # Comprobamos si la referencia ha sido sustituida y no tiene existencias
                        if articulo.nuevaReferencia is not None and articulo.existencias <= 0:
                            nuevaReferencia = articulo.nuevaReferencia
                            articulo = Articulo.objects.get(referencia=nuevaReferencia)
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
                    entalm_id = kwargs['pk']
                    lineas = LineaEntradaAlmacen.objects.filter(entradaAlmacen_id=entalm_id).count()
                    # print(f'lineas: {lineas}')
                    if lineas == 0:
                        # print(f'Borramos cabecera')
                        entradaAlmacen = EntradaAlmacen.objects.get(pk=entalm_id)
                        entradaAlmacen.delete()
                        datos = {
                            'url': reverse_lazy(f'sweb:{EntradaAlmacenListView.folder}_list')
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


class LineaEntradaAlmacenUpdateView(UpdateView):
    folder = 'linentalm'
    model = LineaEntradaAlmacen
    form_class = LineaEntradaAlmacenForm
    template_name = f'{folder}/create.html'
    # success_url = ''
    end_message_success = 'modificada'

    # utilizamos un decorador para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = f'Editar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['action'] = 'edit'
        context['list_url'] = self.request.get_full_path().split(self.folder)[0]
        context['folder'] = self.folder
        # print(f'context: {context}')
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path().split(self.folder)[0]


class LineaEntradaAlmacenDeleteView(DeleteView):
    folder = 'linentalm'
    model = LineaEntradaAlmacen
    template_name = f'{folder}/delete.html'
    success_url = ''
    end_message_success = 'eliminada'
    start_message_error = 'No se puede borrar esta'
    end_message_error = 'porque está siendo utilizada en otra tabla'

    # utilizamos un decorador para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = f'Borrar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['entity_plural'] = self.model._meta.verbose_name_plural
        context['list_url'] = self.request.get_full_path().split(self.folder)[0]
        context['action'] = 'delete'
        context['folder'] = self.folder
        return context

    def form_valid(self, form):
        print('LineaEntradaAlmacenDeleteView - form_valid')
        # Añadimos la lógica adicional al borrado de una línea
        if self.object.entradaAlmacen.impreso:
            messages.error(self.request, 'No se puede borrar, el Documento ya ha sido impreso')
            return self.render_to_response(context=self.get_context_data())
        if self.object.referencia.bloqueo:
            messages.error(self.request, f'No se puede borrar, la Referencia {self.object.referencia} está pendiente de inventario')
            return self.render_to_response(context=self.get_context_data())

        # Actualizamos la Entrada Almacén
        self.object.entradaAlmacen.importe -= self.object.importeCoste
        self.object.entradaAlmacen.save()

        # Actualizamos la Referencia
        self.object.referencia.existencias -= self.object.cantidad
        if self.object.referencia.existencias > 0:
            self.object.referencia.precioCosteMedio = round(
                (self.object.referencia.precioCosteMedio * self.object.referencia.existencias - self.object.importeCoste) / self.object.referencia.existencias, 2)

        self.object.referencia.entradasMes -= self.object.cantidad
        self.object.referencia.entradasAcumuladas -= self.object.cantidad
        self.object.referencia.unidadesCompradasMes -= self.object.cantidad
        self.object.referencia.unidadesCompradasAno -= self.object.cantidad
        self.object.referencia.importeComprasMes -= self.object.importeCoste
        self.object.referencia.importeComprasAno -= self.object.importeCoste
        self.object.referencia.fechaUltMovimiento = datetime.now(tz=get_current_timezone())
        self.object.referencia.save()

        # Actualizamos el proveedor
        if self.object.entradaAlmacen.proveedor is not None:
            self.object.entradaAlmacen.proveedor.comprasMes -= self.object.importeCoste
            self.object.entradaAlmacen.proveedor.comprasAno -= self.object.importeCoste
            self.object.entradaAlmacen.proveedor.save()

        # Reescribimos form_valid para controlar los ProtectedError
        try:
            entalm_id = self.object.entradaAlmacen.id
            self.object.delete()
            messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
            # comprobamos si hemos borrado la última línea
            lineas = LineaEntradaAlmacen.objects.filter(entradaAlmacen_id=entalm_id).count()
            print(f'lineas: {lineas}')
            if lineas == 0:
                # si no hay más líneas borramos también la Entrada Almacén
                entradaAlmacen = EntradaAlmacen.objects.get(pk=entalm_id)
                entradaAlmacen.delete()
                return HttpResponseRedirect(reverse_lazy(f'sweb:{EntradaAlmacenListView.folder}_list'))
            else:
                return HttpResponseRedirect(self.get_success_url())
        except ProtectedError as e:
            messages.error(self.request,
                           f'{self.start_message_error} {self.model._meta.verbose_name} {self.end_message_error}')
            return self.render_to_response(context=self.get_context_data())

    def get_success_url(self):
        return self.request.get_full_path().split(self.folder)[0]


