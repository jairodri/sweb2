from django.shortcuts import render
from core.sweb.models import FormaDePago


def formasdepago_list(request):
    data = {
        'title': 'Formas de Pago - Listado',
        'formasdepago': FormaDePago.objects.all()
    }
    return render(request, 'formasdepago/list.html', data)
