from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from core.sweb.forms import ImportarForm
from core.sweb.resources import DescuentoMOResource, ClienteResource
from tablib import Dataset
from django.contrib import messages


class ImportarView(FormView):
    template_name = 'administrador/importar.html'
    form_class = ImportarForm
    success_url = reverse_lazy('sweb:dashboard')

    # se pueden utilizar decoradores para añadir la funcionalidad de control de autenticación
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Importar Tablas VBSIR'
        context['entity'] = 'Importar'
        context['action'] = 'importar'
        context['list_url'] = reverse_lazy('sweb:administrador_importar')
        context['dashboard_url'] = reverse_lazy('sweb:dashboard')
        return context

    def form_invalid(self, form):
        print(f'form: {form.errors}')
        return super().form_invalid(form)

    def form_valid(self, form):
        # print(f'files: {self.request.FILES}')
        lista_tablas = self.request.POST['lista_tablas']
        print(lista_tablas)
        import_file = self.request.FILES['fichero_tabla']
        # print(f'name: {import_file.name} - {import_file.size}')
        if lista_tablas == '01':
            dtomo_resource = DescuentoMOResource()
            dtomo_file = import_file
        elif lista_tablas == '05':
            cliente_resource = ClienteResource()
            cliente_file = import_file
        dataset = Dataset()
        imported_data = dataset.load(import_file.read().decode(), format='json')
        print(imported_data)
        if lista_tablas == '01':
            result = dtomo_resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                result = dtomo_resource.import_data(dataset, dry_run=False)
                messages.add_message(self.request, messages.SUCCESS, 'Fichero importado')
            else:
                print(result.base_errors)
                print(result.row_errors())
        elif lista_tablas == '05':
            result = cliente_resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                result = cliente_resource.import_data(dataset, dry_run=False)
                messages.add_message(self.request, messages.SUCCESS, 'Fichero importado')
            else:
                print(result.base_errors)
                print(result.row_errors())

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        # print(f'post file {request.FILES}')
        return super().post(request, *args, **kwargs)


