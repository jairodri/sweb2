from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.forms import BancoForm
from core.sweb.models import Banco
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from django.db.models import Q


class BancoListView(BasicListView, ListView):
    folder = 'bancos'
    model = Banco
    template_name = f'{folder}/list.html'


class BancoCreateView(BasicCreateView, CreateView):
    folder = 'bancos'
    model = Banco
    form_class = BancoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'


class BancoUpdateView(BasicUpdateView, UpdateView):
    folder = 'bancos'
    model = Banco
    form_class = BancoForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'modificado'


class BancoDeleteView(BasicDeleteView, DeleteView):
    folder = 'bancos'
    model = Banco
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class BancoDetailView(BasicDetailView, DetailView):
    folder = 'bancos'
    model = Banco
    template_name = f'{folder}/detail.html'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Gestionamos los botones de Anterior y Siguiente teniendo en cuenta las distintas posibilidades de orderación
        print(self.request.session.get('search'))
        print(self.request.session.get('order_col_name'))
        order_col_name = self.request.session.get('order_col_name')
        if order_col_name == 'codigo':
            filtro_prev = self.get_queryset().filter((Q(codigo__lt=self.object.codigo)) | (Q(codigo__exact=self.object.codigo) & Q(pk__lt=self.object.pk))).order_by('-codigo', '-id')
            filtro_next = self.get_queryset().filter((Q(codigo__gt=self.object.codigo)) | (Q(codigo__exact=self.object.codigo) & Q(pk__gt=self.object.pk))).order_by('codigo', 'id')
        elif order_col_name == '-codigo':
            filtro_prev = self.get_queryset().filter((Q(codigo__gt=self.object.codigo)) | (Q(codigo__exact=self.object.codigo) & Q(pk__gt=self.object.pk))).order_by('codigo', 'id')
            filtro_next = self.get_queryset().filter((Q(codigo__lt=self.object.codigo)) | (Q(codigo__exact=self.object.codigo) & Q(pk__lt=self.object.pk))).order_by('-codigo', '-id')
        elif order_col_name == 'sucursal':
            filtro_prev = self.get_queryset().filter((Q(sucursal__lt=self.object.sucursal)) | (Q(sucursal__exact=self.object.sucursal) & Q(pk__lt=self.object.pk))).order_by('-sucursal', '-id')
            filtro_next = self.get_queryset().filter((Q(sucursal__gt=self.object.sucursal)) | (Q(sucursal__exact=self.object.sucursal) & Q(pk__gt=self.object.pk))).order_by('sucursal', 'id')
        elif order_col_name == '-sucursal':
            filtro_prev = self.get_queryset().filter((Q(sucursal__gt=self.object.sucursal)) | (Q(sucursal__exact=self.object.sucursal) & Q(pk__gt=self.object.pk))).order_by('sucursal', 'id')
            filtro_next = self.get_queryset().filter((Q(sucursal__lt=self.object.sucursal)) | (Q(sucursal__exact=self.object.sucursal) & Q(pk__lt=self.object.pk))).order_by('-sucursal', '-id')
        elif order_col_name == 'razonsocial':
            filtro_prev = self.get_queryset().filter((Q(razonsocial__lt=self.object.razonsocial)) | (Q(razonsocial__exact=self.object.razonsocial) & Q(pk__lt=self.object.pk))).order_by('-razonsocial', '-id')
            filtro_next = self.get_queryset().filter((Q(razonsocial__gt=self.object.razonsocial)) | (Q(razonsocial__exact=self.object.razonsocial) & Q(pk__gt=self.object.pk))).order_by('razonsocial', 'id')
        elif order_col_name == '-razonsocial':
            filtro_prev = self.get_queryset().filter((Q(razonsocial__gt=self.object.razonsocial)) | (Q(razonsocial__exact=self.object.razonsocial) & Q(pk__gt=self.object.pk))).order_by('razonsocial', 'id')
            filtro_next = self.get_queryset().filter((Q(razonsocial__lt=self.object.razonsocial)) | (Q(razonsocial__exact=self.object.razonsocial) & Q(pk__lt=self.object.pk))).order_by('-razonsocial', '-id')
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

        # print(f'filtro_prev: {filtro_prev}')
        # print(f'filtro_next: {filtro_next}')
        prev_pk = (filtro_prev.values('pk'))[:1]
        next_pk = (filtro_next.values('pk'))[:1]

        if prev_pk:
            context['prev_pk'] = prev_pk[0]['pk']
        if next_pk:
            context['next_pk'] = next_pk[0]['pk']

        return context
