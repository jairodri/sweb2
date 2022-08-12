from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from core.sweb.forms import LineaEntradaAlmacenForm
from core.sweb.mixins import LineaMovimientoCreateView
from core.sweb.models import LineaEntradaAlmacen, EntradaAlmacen, Articulo
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.sweb.views.entalmacen.views import EntradaAlmacenListView
from datetime import datetime
from django.utils.timezone import get_current_timezone


class LineaEntradaAlmacenCreateView(LineaMovimientoCreateView, CreateView):
    folder = 'linentalm'
    model = LineaEntradaAlmacen
    form_class = LineaEntradaAlmacenForm
    template_name = f'{folder}/create.html'
    # success_url = ''
    end_message_success = 'añadida'
    movimiento = EntradaAlmacen
    movimiento_field = 'entradaAlmacen'
    list_view = EntradaAlmacenListView
    artiulo_model = Articulo


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


