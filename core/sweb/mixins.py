from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.forms import ModelForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from core.models import BaseModel
from crum import get_current_user


# Redefinimos la función save para actualizar los campos de auditoría del user
class ModelMixin(BaseModel):

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # Incluimos el código para la auditoría
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user_creation = user
        else:
            self.user_updated = user

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class BasicView(View):

    # utilizamos un decorador para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BasicListView(BasicView):

    # redefinimos el post para cargar la datatable con ajax
    def post(self, request, *args, **kwargs):
        list_values = self.list_values
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # recuperamos solo los campos necesarios para la paginación
                for i in self.model.objects.all().values(*list_values):
                    data.append(i)
            else:
                data = {'error': 'Ha ocurrido un error'}
        except Exception as e:
            data = {
                'error': str(e)
            }
        return JsonResponse(data, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.model._meta.verbose_name_plural
        context['add_url'] = reverse_lazy(f'sweb:{self.folder}_add')
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        context['entity'] = self.model._meta.verbose_name_plural
        return context


class BasicCreateView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Añadir {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name_plural
        context['action'] = 'add'
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
        return super().form_valid(form)


class BasicUpdateView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name_plural
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
        return super().form_valid(form)


class BasicDeleteView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Borrar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name_plural
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        # Reescribimos form_valid para controlar los ProtectedError
        try:
            self.object.delete()
            messages.success(self.request, f'{self.model._meta.verbose_name} {self.end_message_success}')
            return HttpResponseRedirect(self.success_url)
        except ProtectedError as e:
            messages.error(self.request,
                           f'{self.start_message_error} {self.model._meta.verbose_name} {self.end_message_error}')
            return self.render_to_response(context=self.get_context_data())


class BasicDetailView(BasicView):

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalle {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name_plural
        context['list_url'] = reverse_lazy(f'sweb:{self.folder}_list')
        context['action'] = 'detail'
        return context


class CodigoBaseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # diferenciamos add/edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:  # diferenciamos add/edit
            self.fields['codigo'].disabled = True
        else:
            self.fields['codigo'].widget.attrs['autofocus'] = True