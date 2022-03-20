from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.sweb.forms import DescuentoRecambiosForm
from core.sweb.models import DescuentoRecambios
from core.sweb.mixins import DescuentoRecambiosListView, DescuentoRecambiosCreateView, DescuentoRecambiosUpdateView, \
    DescuentoRecambiosDeleteView


class DescuentoRecambiosVentasListView(DescuentoRecambiosListView, ListView):
    tipo = '0'
    folder = 'descuentosrec'
    subfolder = 'dtoventas'
    model_verbose_plural = 'Descuentos Ventas'
    model_verbose_name = 'Descuento Ventas'
    model = DescuentoRecambios
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'codpieza', 'descuento']


class DescuentoRecambiosVentasCreateView(DescuentoRecambiosCreateView, CreateView):
    tipo = '0'
    folder = 'descuentosrec'
    subfolder = 'dtoventas'
    model_verbose_plural = 'Descuentos Ventas'
    model_verbose_name = 'Descuento Ventas'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'añadido'


class DescuentoRecambiosVentasUpdateView(DescuentoRecambiosUpdateView, UpdateView):
    tipo = '0'
    folder = 'descuentosrec'
    subfolder = 'dtoventas'
    model_verbose_plural = 'Descuentos Ventas'
    model_verbose_name = 'Descuento Ventas'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'modificado'


class DescuentoRecambiosVentasDeleteView(DescuentoRecambiosDeleteView, DeleteView):
    tipo = '0'
    folder = 'descuentosrec'
    subfolder = 'dtoventas'
    model_verbose_plural = 'Descuentos Ventas'
    model_verbose_name = 'Descuento Ventas'
    model = DescuentoRecambios
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class DescuentoRecambiosPedidosAproListView(DescuentoRecambiosListView, ListView):
    tipo = '1'
    folder = 'descuentosrec'
    subfolder = 'dtopedapro'
    model_verbose_plural = 'Descuentos Pedidos Aprovisionamiento'
    model_verbose_name = 'Descuento Pedido Aprovisionamiento'
    model = DescuentoRecambios
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'codpieza', 'descuento']


class DescuentoRecambiosPedidosAproCreateView(DescuentoRecambiosCreateView, CreateView):
    tipo = '1'
    folder = 'descuentosrec'
    subfolder = 'dtopedapro'
    model_verbose_plural = 'Descuentos Pedidos Aprovisionamiento'
    model_verbose_name = 'Descuento Pedido Aprovisionamiento'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'añadido'


class DescuentoRecambiosPedidosAproUpdateView(DescuentoRecambiosUpdateView, UpdateView):
    tipo = '1'
    folder = 'descuentosrec'
    subfolder = 'dtopedapro'
    model_verbose_plural = 'Descuentos Pedidos Aprovisionamiento'
    model_verbose_name = 'Descuento Pedido Aprovisionamiento'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'modificado'


class DescuentoRecambiosPedidosAproDeleteView(DescuentoRecambiosDeleteView, DeleteView):
    tipo = '1'
    folder = 'descuentosrec'
    subfolder = 'dtopedapro'
    model_verbose_plural = 'Descuentos Pedidos Aprovisionamiento'
    model_verbose_name = 'Descuento Pedido Aprovisionamiento'
    model = DescuentoRecambios
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class DescuentoRecambiosPedidosUrgtesListView(DescuentoRecambiosListView, ListView):
    tipo = '2'
    folder = 'descuentosrec'
    subfolder = 'dtopedurgte'
    model_verbose_plural = 'Descuentos Pedidos Urgentes'
    model_verbose_name = 'Descuento Pedido Urgente'
    model = DescuentoRecambios
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'codpieza', 'descuento']


class DescuentoRecambiosPedidosUrgtesCreateView(DescuentoRecambiosCreateView, CreateView):
    tipo = '2'
    folder = 'descuentosrec'
    subfolder = 'dtopedurgte'
    model_verbose_plural = 'Descuentos Pedidos Urgentes'
    model_verbose_name = 'Descuento Pedido Urgente'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'añadido'


class DescuentoRecambiosPedidosUrgtesUpdateView(DescuentoRecambiosUpdateView, UpdateView):
    tipo = '2'
    folder = 'descuentosrec'
    subfolder = 'dtopedurgte'
    model_verbose_plural = 'Descuentos Pedidos Urgentes'
    model_verbose_name = 'Descuento Pedido Urgente'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'modificado'


class DescuentoRecambiosPedidosUrgtesDeleteView(DescuentoRecambiosDeleteView, DeleteView):
    tipo = '2'
    folder = 'descuentosrec'
    subfolder = 'dtopedurgte'
    model_verbose_plural = 'Descuentos Pedidos Urgentes'
    model_verbose_name = 'Descuento Pedido Urgente'
    model = DescuentoRecambios
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class DescuentoRecambiosPedidosCampnaListView(DescuentoRecambiosListView, ListView):
    tipo = '3'
    folder = 'descuentosrec'
    subfolder = 'dtopedcamp'
    model_verbose_plural = 'Descuentos Pedidos Campañas'
    model_verbose_name = 'Descuento Pedido Campaña'
    model = DescuentoRecambios
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'codpieza', 'descuento']


class DescuentoRecambiosPedidosCampnaCreateView(DescuentoRecambiosCreateView, CreateView):
    tipo = '3'
    folder = 'descuentosrec'
    subfolder = 'dtopedcamp'
    model_verbose_plural = 'Descuentos Pedidos Campañas'
    model_verbose_name = 'Descuento Pedido Campaña'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'añadido'


class DescuentoRecambiosPedidosCampnaUpdateView(DescuentoRecambiosUpdateView, UpdateView):
    tipo = '3'
    folder = 'descuentosrec'
    subfolder = 'dtopedcamp'
    model_verbose_plural = 'Descuentos Pedidos Campañas'
    model_verbose_name = 'Descuento Pedido Campaña'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'modificado'


class DescuentoRecambiosPedidosCampnaDeleteView(DescuentoRecambiosDeleteView, DeleteView):
    tipo = '3'
    folder = 'descuentosrec'
    subfolder = 'dtopedcamp'
    model_verbose_plural = 'Descuentos Pedidos Campañas'
    model_verbose_name = 'Descuento Pedido Campaña'
    model = DescuentoRecambios
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class DescuentoRecambiosVentasCampnaListView(DescuentoRecambiosListView, ListView):
    tipo = '4'
    folder = 'descuentosrec'
    subfolder = 'dtovtacamp'
    model_verbose_plural = 'Descuentos Ventas Campañas'
    model_verbose_name = 'Descuento Venta Campaña'
    model = DescuentoRecambios
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'codpieza', 'descuento']


class DescuentoRecambiosVentasCampnaCreateView(DescuentoRecambiosCreateView, CreateView):
    tipo = '4'
    folder = 'descuentosrec'
    subfolder = 'dtovtacamp'
    model_verbose_plural = 'Descuentos Ventas Campañas'
    model_verbose_name = 'Descuento Venta Campaña'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'añadido'


class DescuentoRecambiosVentasCampnaUpdateView(DescuentoRecambiosUpdateView, UpdateView):
    tipo = '4'
    folder = 'descuentosrec'
    subfolder = 'dtovtacamp'
    model_verbose_plural = 'Descuentos Ventas Campañas'
    model_verbose_name = 'Descuento Venta Campaña'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'modificado'


class DescuentoRecambiosVentasCampnaDeleteView(DescuentoRecambiosDeleteView, DeleteView):
    tipo = '4'
    folder = 'descuentosrec'
    subfolder = 'dtovtacamp'
    model_verbose_plural = 'Descuentos Ventas Campañas'
    model_verbose_name = 'Descuento Venta Campaña'
    model = DescuentoRecambios
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'


class DescuentoRecambiosPiezasGarantiaListView(DescuentoRecambiosListView, ListView):
    tipo = '5'
    folder = 'descuentosrec'
    subfolder = 'dtopzagar'
    model_verbose_plural = 'Descuentos Piezas Garantías'
    model_verbose_name = 'Descuento Pieza Garantía'
    model = DescuentoRecambios
    template_name = f'{folder}/list.html'
    list_values = ['id', 'codigo', 'codpieza', 'descuento']


class DescuentoRecambiosPiezasGarantiaCreateView(DescuentoRecambiosCreateView, CreateView):
    tipo = '5'
    folder = 'descuentosrec'
    subfolder = 'dtopzagar'
    model_verbose_plural = 'Descuentos Piezas Garantías'
    model_verbose_name = 'Descuento Pieza Garantía'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'añadido'


class DescuentoRecambiosPiezasGarantiaUpdateView(DescuentoRecambiosUpdateView, UpdateView):
    tipo = '5'
    folder = 'descuentosrec'
    subfolder = 'dtopzagar'
    model_verbose_plural = 'Descuentos Piezas Garantías'
    model_verbose_name = 'Descuento Pieza Garantía'
    model = DescuentoRecambios
    form_class = DescuentoRecambiosForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'modificado'


class DescuentoRecambiosPiezasGarantiaDeleteView(DescuentoRecambiosDeleteView, DeleteView):
    tipo = '5'
    folder = 'descuentosrec'
    subfolder = 'dtopzagar'
    model_verbose_plural = 'Descuentos Piezas Garantías'
    model_verbose_name = 'Descuento Pieza Garantía'
    model = DescuentoRecambios
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{subfolder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'

