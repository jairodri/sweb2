from django.http import HttpResponse
from django.shortcuts import render
from core.sweb.models import FormaDePago


# Create your views here.
def vistaprueba(request):
    data = {
        'name': 'Jaime',
        'formasdepago': FormaDePago.objects.all()
    }
    return render(request, 'index.html', data)
