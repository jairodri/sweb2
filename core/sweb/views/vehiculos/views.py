from django.http import JsonResponse
from django.urls import reverse_lazy
from core.sweb.forms import VehiculoForm
from core.sweb.models import Vehiculo, Cliente
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from django.db.models import Q


class VehiculoListView(BasicListView, ListView):
    folder = 'vehiculos'
    model = Vehiculo
    template_name = f'{folder}/list.html'


class VehiculoCreateView(BasicCreateView, CreateView):
    folder = 'vehiculos'
    model = Vehiculo
    form_class = VehiculoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'

    # redefinimos el post para las operaciones con ajax
    def post(self, request, *args, **kwargs):
        print(f'post: {request.POST}')
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'formbase':
                action2 = request.POST['action2']
                if action2 == 'select2':
                    term = request.POST['term']
                    field = request.POST['field']
                    datos = []
                    if field == 'cliente':
                        clientes = Cliente.to_search_select(Cliente, term)
                        for i in clientes:
                            datos.append(i.to_list_select_veh())
                else:
                    return super().post(request, *args, **kwargs)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)


class VehiculoUpdateView(BasicUpdateView, UpdateView):
    folder = 'vehiculos'
    model = Vehiculo
    form_class = VehiculoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'

    # redefinimos el post para las operaciones con ajax
    def post(self, request, *args, **kwargs):
        print(f'post: {request.POST}')
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'formbase':
                action2 = request.POST['action2']
                if action2 == 'select2':
                    term = request.POST['term']
                    field = request.POST['field']
                    datos = []
                    if field == 'cliente':
                        clientes = Cliente.to_search_select(Cliente, term)
                        for i in clientes:
                            datos.append(i.to_list_select_veh())
                else:
                    return super().post(request, *args, **kwargs)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)


class VehiculoDeleteView(BasicDeleteView, DeleteView):
    folder = 'vehiculos'
    model = Vehiculo
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class VehiculoDetailView(BasicDetailView, DetailView):
    folder = 'vehiculos'
    model = Vehiculo
    template_name = f'{folder}/detail.html'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Gestionamos los botones de Anterior y Siguiente teniendo en cuenta las distintas posibilidades de ordenación
        # print(self.request.session.get('search'))
        # print(self.request.session.get('order_col_name'))
        order_col_name = self.request.session.get('order_col_name')
        if order_col_name == 'matricula':
            if self.object.matricula is None:
                filtro_prev = self.get_queryset().filter((Q(matricula__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-matricula', '-id')
                filtro_next = self.get_queryset().filter((Q(matricula__isnull=True) & Q(pk__gt=self.object.pk)) | Q(matricula__isnull=False)).order_by('matricula', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(matricula__lt=self.object.matricula) | (Q(matricula__exact=self.object.matricula) & Q(pk__lt=self.object.pk))) | Q(matricula__isnull=True)).order_by('-matricula', '-id')
                filtro_next = self.get_queryset().filter((Q(matricula__gt=self.object.matricula)) | (Q(matricula__exact=self.object.matricula) & Q(pk__gt=self.object.pk))).order_by('matricula', 'id')
        elif order_col_name == '-matricula':
            if self.object.matricula is None:
                filtro_prev = self.get_queryset().filter((Q(matricula__isnull=True) & Q(pk__lt=self.object.pk)) | Q(matricula__isnull=False)).order_by('matricula', '-id')
                filtro_next = self.get_queryset().filter((Q(matricula__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-matricula', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(matricula__gt=self.object.matricula)) | (Q(matricula__exact=self.object.matricula) & Q(pk__lt=self.object.pk))).order_by('matricula', '-id')
                filtro_next = self.get_queryset().filter((Q(matricula__lt=self.object.matricula) | (Q(matricula__exact=self.object.matricula) & Q(pk__gt=self.object.pk))) | Q(matricula__isnull=True)).order_by('-matricula', 'id')
        elif order_col_name == 'vin':
            if self.object.vin is None:
                filtro_prev = self.get_queryset().filter((Q(vin__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-vin', '-id')
                filtro_next = self.get_queryset().filter((Q(vin__isnull=True) & Q(pk__gt=self.object.pk)) | Q(vin__isnull=False)).order_by('vin', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(vin__lt=self.object.vin) | (Q(vin__exact=self.object.vin) & Q(pk__lt=self.object.pk))) | Q(vin__isnull=True)).order_by('-vin', '-id')
                filtro_next = self.get_queryset().filter((Q(vin__gt=self.object.vin)) | (Q(vin__exact=self.object.vin) & Q(pk__gt=self.object.pk))).order_by('vin', 'id')
        elif order_col_name == '-vin':
            if self.object.vin is None:
                filtro_prev = self.get_queryset().filter((Q(vin__isnull=True) & Q(pk__lt=self.object.pk)) | Q(vin__isnull=False)).order_by('vin', '-id')
                filtro_next = self.get_queryset().filter((Q(vin__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-vin', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(vin__gt=self.object.vin)) | (Q(vin__exact=self.object.vin) & Q(pk__lt=self.object.pk))).order_by('vin', '-id')
                filtro_next = self.get_queryset().filter((Q(vin__lt=self.object.vin) | (Q(vin__exact=self.object.vin) & Q(pk__gt=self.object.pk))) | Q(vin__isnull=True)).order_by('-vin', 'id')
        elif order_col_name == 'cliente__codigo':
            if self.object.cliente.codigo is None:
                filtro_prev = self.get_queryset().filter((Q(cliente__codigo__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-cliente__codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(cliente__codigo__isnull=True) & Q(pk__gt=self.object.pk)) | Q(cliente__codigo__isnull=False)).order_by('cliente__codigo', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(cliente__codigo__lt=self.object.cliente.codigo) | (Q(cliente__codigo__exact=self.object.cliente.codigo) & Q(pk__lt=self.object.pk))) | Q(cliente__codigo__isnull=True)).order_by('-cliente__codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(cliente__codigo__gt=self.object.cliente.codigo)) | (Q(cliente__codigo__exact=self.object.cliente.codigo) & Q(pk__gt=self.object.pk))).order_by('cliente__codigo', 'id')
        elif order_col_name == '-cliente__codigo':
            if self.object.cliente.codigo is None:
                filtro_prev = self.get_queryset().filter((Q(cliente__codigo__isnull=True) & Q(pk__lt=self.object.pk)) | Q(cliente__codigo__isnull=False)).order_by('cliente__codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(cliente__codigo__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-cliente__codigo', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(cliente__codigo__gt=self.object.cliente.codigo)) | (Q(cliente__codigo__exact=self.object.cliente.codigo) & Q(pk__lt=self.object.pk))).order_by('cliente__codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(cliente__codigo__lt=self.object.cliente.codigo) | (Q(cliente__codigo__exact=self.object.cliente.codigo) & Q(pk__gt=self.object.pk))) | Q(cliente__codigo__isnull=True)).order_by('-cliente__codigo', 'id')
        elif order_col_name == 'marca__descripcion':
            if self.object.marca is None:
                filtro_prev = self.get_queryset().filter((Q(marca__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-marca__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(marca__isnull=True) & Q(pk__gt=self.object.pk)) | Q(marca__isnull=False)).order_by('marca__descripcion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(marca__descripcion__lt=self.object.marca.descripcion) | (Q(marca__descripcion__exact=self.object.marca.descripcion) & Q(pk__lt=self.object.pk))) | Q(marca__isnull=True)).order_by('-marca__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(marca__descripcion__gt=self.object.marca.descripcion)) | (Q(marca__descripcion__exact=self.object.marca.descripcion) & Q(pk__gt=self.object.pk))).order_by('marca__descripcion', 'id')
        elif order_col_name == '-marca__descripcion':
            if self.object.marca is None:
                filtro_prev = self.get_queryset().filter((Q(marca__descripcion__isnull=True) & Q(pk__lt=self.object.pk)) | Q(marca__descripcion__isnull=False)).order_by('marca__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(marca__descripcion__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-marca__descripcion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(marca__descripcion__gt=self.object.marca.descripcion)) | (Q(marca__descripcion__exact=self.object.marca.descripcion) & Q(pk__lt=self.object.pk))).order_by('marca__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(marca__descripcion__lt=self.object.marca.descripcion) | (Q(marca__descripcion__exact=self.object.marca.descripcion) & Q(pk__gt=self.object.pk))) | Q(marca__descripcion__isnull=True)).order_by('-marca__descripcion', 'id')
        elif order_col_name == 'modelo__descripcion':
            if self.object.modelo is None:
                filtro_prev = self.get_queryset().filter((Q(modelo__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-modelo__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(modelo__isnull=True) & Q(pk__gt=self.object.pk)) | Q(modelo__isnull=False)).order_by('modelo__descripcion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(modelo__descripcion__lt=self.object.modelo.descripcion) | (Q(modelo__descripcion__exact=self.object.modelo.descripcion) & Q(pk__lt=self.object.pk))) | Q(modelo__isnull=True)).order_by('-modelo__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(modelo__descripcion__gt=self.object.modelo.descripcion)) | (Q(modelo__descripcion__exact=self.object.modelo.descripcion) & Q(pk__gt=self.object.pk))).order_by('modelo__descripcion', 'id')
        elif order_col_name == '-modelo__descripcion':
            if self.object.modelo is None:
                filtro_prev = self.get_queryset().filter((Q(modelo__descripcion__isnull=True) & Q(pk__lt=self.object.pk)) | Q(modelo__descripcion__isnull=False)).order_by('modelo__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(modelo__descripcion__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-modelo__descripcion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(modelo__descripcion__gt=self.object.modelo.descripcion)) | (Q(modelo__descripcion__exact=self.object.modelo.descripcion) & Q(pk__lt=self.object.pk))).order_by('modelo__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(modelo__descripcion__lt=self.object.modelo.descripcion) | (Q(modelo__descripcion__exact=self.object.modelo.descripcion) & Q(pk__gt=self.object.pk))) | Q(modelo__descripcion__isnull=True)).order_by('-modelo__descripcion', 'id')

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
