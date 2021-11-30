from django.contrib import admin
from core.sweb.models import *

# Register your models here.
# Para que se muestren en el panel administrador del servidor
admin.site.register(Banco)
admin.site.register(DescuentoMO)
admin.site.register(FormaDePago)
admin.site.register(TipoClienteRecambios)
