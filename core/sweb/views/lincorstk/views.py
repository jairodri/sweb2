from django.views.generic import CreateView
from core.sweb.forms import LineaCorreccionStockForm
from core.sweb.mixins import LineaMovimientoCreateView
from core.sweb.models import LineaCorreccionStock, CorreccionStock, Articulo
from core.sweb.views.corstock.views import CorreccionStockListView


class LineaCorreccionStockCreateView(LineaMovimientoCreateView, CreateView):
    folder = 'lincorstk'
    model = LineaCorreccionStock
    form_class = LineaCorreccionStockForm
    template_name = f'{folder}/create.html'
    # success_url = ''
    end_message_success = 'añadida'
    movimiento = CorreccionStock
    movimiento_field = 'correccionStock'
    list_view = CorreccionStockListView
    artiulo_model = Articulo







