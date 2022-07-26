from django.http import JsonResponse
from django.urls import reverse_lazy
from core.sweb.forms import OperarioForm
from core.sweb.models import Operario
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from django.db.models import Q


class OperarioListView(BasicListView, ListView):
    folder = 'opetaller'
    model = Operario
    template_name = f'{folder}/list.html'


class OperarioCreateView(BasicCreateView, CreateView):
    folder = 'opetaller'
    model = Operario
    form_class = OperarioForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'

    def get_initial(self):
        # valores por defecto
        initial = {
            'actividad': 'T',
            'hExtCurInvertidoMes': 0.00,
            'hExtFacInvertidoMes': 0.00,
            'hExtFacBaremoMes': 0.00,
            'horasExtraMes': 0.00,
            'hExtCurInvertidoAno': 0.00,
            'hExtFacInvertidoAno': 0.00,
            'hExtFacBaremoAno': 0.00,
            'horasExtraAno': 0.00,
            'hIntCurInvertidoMes': 0.00,
            'hIntFacInvertidoMes': 0.00,
            'hIntFacBaremoMes': 0.00,
            'absentismoMes': 0.00,
            'hIntCurInvertidoAno': 0.00,
            'hIntFacInvertidoAno': 0.00,
            'hIntFacBaremoAno': 0.00,
            'absentismoAno': 0.00,
            'hGarCurInvertidoMes': 0.00,
            'hGarFacInvertidoMes': 0.00,
            'hGarFacBaremoMes': 0.00,
            'absentismoSocialMes': 0.00,
            'hGarCurInvertidoAno': 0.00,
            'hGarFacInvertidoAno': 0.00,
            'hGarFacBaremoAno': 0.00,
            'absentismoSocialAno': 0.00,
            'hImpCurInvertidoMes': 0.00,
            'hImpFacInvertidoMes': 0.00,
            'hImpFacBaremoMes': 0.00,
            'hImpCurInvertidoAno': 0.00,
            'hImpFacInvertidoAno': 0.00,
            'hImpFacBaremoAno': 0.00,
        }
        return initial


class OperarioUpdateView(BasicUpdateView, UpdateView):
    folder = 'opetaller'
    model = Operario
    form_class = OperarioForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class OperarioDeleteView(BasicDeleteView, DeleteView):
    folder = 'opetaller'
    model = Operario
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class OperarioDetailView(BasicDetailView, DetailView):
    folder = 'opetaller'
    model = Operario
    template_name = f'{folder}/detail.html'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Gestionamos los botones de Anterior y Siguiente teniendo en cuenta las distintas posibilidades de ordenación
        print(self.request.session.get('search'))
        print(self.request.session.get('order_col_name'))
        order_col_name = self.request.session.get('order_col_name')
        if order_col_name == 'codigo':
            if self.object.codigo is None:
                filtro_prev = self.get_queryset().filter((Q(codigo__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(codigo__isnull=True) & Q(pk__gt=self.object.pk)) | Q(codigo__isnull=False)).order_by('codigo', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(codigo__lt=self.object.codigo) | (Q(codigo__exact=self.object.codigo) & Q(pk__lt=self.object.pk))) | Q(codigo__isnull=True)).order_by('-codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(codigo__gt=self.object.codigo)) | (Q(codigo__exact=self.object.codigo) & Q(pk__gt=self.object.pk))).order_by('codigo', 'id')
        elif order_col_name == '-codigo':
            if self.object.codigo is None:
                filtro_prev = self.get_queryset().filter((Q(codigo__isnull=True) & Q(pk__lt=self.object.pk)) | Q(codigo__isnull=False)).order_by('codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(codigo__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-codigo', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(codigo__gt=self.object.codigo)) | (Q(codigo__exact=self.object.codigo) & Q(pk__lt=self.object.pk))).order_by('codigo', '-id')
                filtro_next = self.get_queryset().filter((Q(codigo__lt=self.object.codigo) | (Q(codigo__exact=self.object.codigo) & Q(pk__gt=self.object.pk))) | Q(codigo__isnull=True)).order_by('-codigo', 'id')
        elif order_col_name == 'nombre':
            if self.object.nombre is None:
                filtro_prev = self.get_queryset().filter((Q(nombre__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-nombre', '-id')
                filtro_next = self.get_queryset().filter((Q(nombre__isnull=True) & Q(pk__gt=self.object.pk)) | Q(nombre__isnull=False)).order_by('nombre', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(nombre__lt=self.object.nombre) | (Q(nombre__exact=self.object.nombre) & Q(pk__lt=self.object.pk))) | Q(nombre__isnull=True)).order_by('-nombre', '-id')
                filtro_next = self.get_queryset().filter((Q(nombre__gt=self.object.nombre)) | (Q(nombre__exact=self.object.nombre) & Q(pk__gt=self.object.pk))).order_by('nombre', 'id')
        elif order_col_name == '-nombre':
            if self.object.nombre is None:
                filtro_prev = self.get_queryset().filter((Q(nombre__isnull=True) & Q(pk__lt=self.object.pk)) | Q(nombre__isnull=False)).order_by('nombre', '-id')
                filtro_next = self.get_queryset().filter((Q(nombre__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-nombre', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(nombre__gt=self.object.nombre)) | (Q(nombre__exact=self.object.nombre) & Q(pk__lt=self.object.pk))).order_by('nombre', '-id')
                filtro_next = self.get_queryset().filter((Q(nombre__lt=self.object.nombre) | (Q(nombre__exact=self.object.nombre) & Q(pk__gt=self.object.pk))) | Q(nombre__isnull=True)).order_by('-nombre', 'id')
        elif order_col_name == 'categoria__descripcion':
            if self.object.categoria is None:
                filtro_prev = self.get_queryset().filter((Q(categoria__isnull=True) & Q(pk__lt=self.object.pk))).order_by('-categoria__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(categoria__isnull=True) & Q(pk__gt=self.object.pk)) | Q(categoria__isnull=False)).order_by('categoria__descripcion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(categoria__descripcion__lt=self.object.categoria.descripcion) | (Q(categoria__descripcion__exact=self.object.categoria.descripcion) & Q(pk__lt=self.object.pk))) | Q(categoria__isnull=True)).order_by('-categoria__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(categoria__descripcion__gt=self.object.categoria.descripcion)) | (Q(categoria__descripcion__exact=self.object.categoria.descripcion) & Q(pk__gt=self.object.pk))).order_by('categoria__descripcion', 'id')
        elif order_col_name == '-categoria__descripcion':
            if self.object.categoria is None:
                filtro_prev = self.get_queryset().filter((Q(categoria__descripcion__isnull=True) & Q(pk__lt=self.object.pk)) | Q(categoria__descripcion__isnull=False)).order_by('categoria__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(categoria__descripcion__isnull=True) & Q(pk__gt=self.object.pk))).order_by('-categoria__descripcion', 'id')
            else:
                filtro_prev = self.get_queryset().filter((Q(categoria__descripcion__gt=self.object.categoria.descripcion)) | (Q(categoria__descripcion__exact=self.object.categoria.descripcion) & Q(pk__lt=self.object.pk))).order_by('categoria__descripcion', '-id')
                filtro_next = self.get_queryset().filter((Q(categoria__descripcion__lt=self.object.categoria.descripcion) | (Q(categoria__descripcion__exact=self.object.categoria.descripcion) & Q(pk__gt=self.object.pk))) | Q(categoria__descripcion__isnull=True)).order_by('-categoria__descripcion', 'id')

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
