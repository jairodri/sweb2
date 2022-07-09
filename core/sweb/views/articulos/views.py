from django.http import JsonResponse
from django.urls import reverse_lazy
from decouple import config
from django.views.generic.detail import BaseDetailView
from reportlab.lib.colors import HexColor

from core.sweb.forms import ArticuloForm, TasaForm
from core.sweb.models import Articulo, UnidadMedida, CodigoAproPieza, PrecioTarifa, CodigoIva, CodigoContable, Tasa, TasaCodigo, Cliente, FamiliaMarketing
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.sweb.mixins import BasicCreateView, BasicUpdateView, BasicDeleteView, BasicListView, BasicDetailView
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors


class ArticuloListView(BasicListView, ListView):
    folder = 'articulos'
    model = Articulo
    template_name = f'{folder}/list.html'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itasas_url'] = reverse_lazy(f'sweb:{self.folder}_itasas')
        return context


class ArticuloCreateView(BasicCreateView, CreateView):
    folder = 'articulos'
    model = Articulo
    form_class = ArticuloForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'añadido'

    def get_initial(self):
        # valores por defecto
        unidadMedida = UnidadMedida.objects.get(codigo='1').id
        codAproPieza = CodigoAproPieza.objects.get(codigo='X').id
        ivaPieza = CodigoIva.objects.get(codigo='02').id
        codigoContable = CodigoContable.objects.get(codigo='01').id
        fechaAlta = datetime.now()
        # codigoApro = DescuentoRecambios.objects.filter(tipo='1', codpieza='?')
        # codigoUrgte = DescuentoRecambios.objects.filter(tipo='2', codpieza='?')
        # codigoPromo = DescuentoRecambios.objects.filter(tipo='3', codpieza='?')

        initial = {
            'existencias': 0,
            'tarifa': 0.00,
            'stockSeguridad': 0,
            'puntoPedido': 0,
            'stockMinimo': 0,
            'unidadCompra': 1,
            'unidadVenta': 1,
            'unidadStock': 1,
            'multiplo': 1,
            'codigoObsoleto': '0',
            'unidadMedida': unidadMedida,
            'codAproPieza': codAproPieza,
            'ivaPieza': ivaPieza,
            'codigoContable': codigoContable,
            'fechaAlta': fechaAlta,
            # 'codigoApro': [],
            # 'codigoUrgte': codigoUrgte,
            # 'codigoPromo': codigoPromo,
        }
        return initial

    # redefinimos el post para las operaciones con ajax
    def post(self, request, *args, **kwargs):
        # print(f'post: {request.POST}')
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'listprecios':
                action = request.POST['action']
                if action == 'searchdata_s':
                    datos = self.datatables_server(PrecioTarifa, request, modal=True)
                else:
                    return super().post(request, *args, **kwargs)
            elif tipo_ == 'formbase':
                action2 = request.POST['action2']
                if action2 == 'select2':
                    term = request.POST['term']
                    field = request.POST['field']
                    datos = []
                    if field == 'proveedor':
                        proveedores = Cliente.to_search_select(Cliente, term)
                        for i in proveedores:
                            datos.append(i.to_list_select())
                    elif field == 'familiaMarketing':
                        fmarketing = FamiliaMarketing.to_search_select(FamiliaMarketing, term)
                        for i in fmarketing:
                            datos.append(i.to_list_select())
                else:
                    return super().post(request, *args, **kwargs)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    # en este caso la info de defclien
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['defclien'] = config('DEFCLIEN')
        # print(context)
        return context


class ArticuloUpdateView(BasicUpdateView, UpdateView):
    folder = 'articulos'
    model = Articulo
    form_class = ArticuloForm
    template_name = f'{folder}/create.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    formTasa = TasaForm()
    end_message_success = 'modificado'

    def get_initial(self):

        # Inicializamos el campo del form de tasa con filtrando por código contable
        codcontable = self.get_object().codigoContable
        self.formTasa.fields['codigoTasa'].queryset = TasaCodigo.objects.filter(codcontable=codcontable)

        initial = {
            'funcionCitroen': self.get_object().codigoFuncion,
        }
        return initial

    # redefinimos el post para las operaciones con ajax
    def post(self, request, *args, **kwargs):
        # print(request.POST)
        datos = {}
        try:
            tipo_ = request.POST['tipo_']
            if tipo_ == 'formtasa':
                pk = kwargs['pk']
                action2 = request.POST['action2']
                if action2 == 'inittasa':
                    try:
                        tasa = Tasa.objects.get(referencia=pk)
                        datos = {
                            'denominacion': tasa.denominacion,
                            'precio': tasa.precio,
                            'descuento': tasa.descuento,
                            'nuevo': False,
                        }
                    except Exception as exc:
                        codigo = request.POST['codigoContable']
                        denominacion = ''
                        if codigo == '03':
                            try:
                                tasaCodigo = TasaCodigo.objects.get(codcontable__codigo__iexact=codigo)
                                denominacion = tasaCodigo.descripcion
                            except Exception as e:
                                print('Error en acceso a TasaCodigo')
                        datos = {
                            'denominacion': denominacion,
                            'precio': 0,
                            'descuento': None,
                            'nuevo': True,
                        }
                elif action2 == 'edittasa':
                    denominacion = request.POST['denominacion']
                    precio = request.POST['precio']
                    descuento = request.POST['descuento']
                    # print(f'{denominacion} - {precio} - {descuento}')
                    try:
                        tasa = Tasa.objects.get(referencia=pk)
                    except Exception as exc:
                        tasa = Tasa()
                        articulo = Articulo.objects.get(id=pk)
                        tasa.referencia = articulo
                    tasa.denominacion = denominacion
                    tasa.precio = float(precio)
                    if descuento.strip() == '':
                        descuento = None
                    else:
                        descuento = float(descuento)
                    tasa.descuento = descuento
                    tasa.save()
                    datos = {
                        'message': 'Tasa actualizada'
                    }
                elif action2 == 'dltetasa':
                    datos = {}
                    try:
                        tasa = Tasa.objects.get(referencia=pk)
                        tasa.delete()
                    except Exception as exc:
                        # print('Error al borrar Tasa')
                        datos['error'] = 'Error al borrar Tasa'
            elif tipo_ == 'formbase':
                action2 = request.POST['action2']
                if action2 == 'select2':
                    term = request.POST['term']
                    field = request.POST['field']
                    datos = []
                    if field == 'proveedor':
                        proveedores = Cliente.to_search_select(Cliente, term)
                        for i in proveedores:
                            datos.append(i.to_list_select())
                    elif field == 'familiaMarketing':
                        fmarketing = FamiliaMarketing.to_search_select(FamiliaMarketing, term)
                        for i in fmarketing:
                            datos.append(i.to_list_select())
                else:
                    return super().post(request, *args, **kwargs)
            else:
                return super().post(request, *args, **kwargs)
        except Exception as e:
            datos = {
                'error': str(e)
            }
        return JsonResponse(datos, safe=False)

    # sobreescribimos el método get_context_data para añadir info al contexto
    # en este caso la info de defclien
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['defclien'] = config('DEFCLIEN')
        context['formtasa'] = self.formTasa
        return context


class ArticuloDeleteView(BasicDeleteView, DeleteView):
    folder = 'articulos'
    model = Articulo
    template_name = f'{folder}/delete.html'
    success_url = reverse_lazy(f'sweb:{folder}_list')
    end_message_success = 'eliminado'
    start_message_error = 'No se puede borrar este'
    end_message_error = 'porque está siendo utilizado en otra tabla'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            precioTarifa = PrecioTarifa.objects.get(referencia=self.object.referencia)
            precioTarifa = precioTarifa.to_list()
        except Exception as ex:
            precioTarifa = None

        context['precioTarifa'] = precioTarifa
        context['defclien'] = config('DEFCLIEN')
        return context

    def form_valid(self, form):
        # print(f'ArticuloDeleteView')
        # Validaciones a realizar antes de eliminar el artículo
        articulo = self.get_object()
        hay_error = False
        if articulo.bloqueo:
            messages.error(self.request, 'Artículo pendiente de inventario')
            hay_error = True
        if articulo.existencias != 0:
            messages.error(self.request, 'Artículo con existencias')
            hay_error = True
        if articulo.pedidosPendientes != 0:
            messages.error(self.request, 'Artículo con pedidos pendientes')
            hay_error = True
        articulos = Articulo.objects.filter(nuevaReferencia=articulo.referencia)
        if articulos.count() > 0:
            messages.error(self.request, f'Artículo está como "Ref. que la sustituye" en: {articulos[0].referencia}')
            hay_error = True
        if hay_error:
            return self.render_to_response(context=self.get_context_data())
        else:
            return super().form_valid(form)


class ArticuloDetailView(BasicDetailView, DetailView):
    folder = 'articulos'
    model = Articulo
    template_name = f'{folder}/detail.html'

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            precioTarifa = PrecioTarifa.objects.get(referencia=self.object.referencia)
            precioTarifa = precioTarifa.to_list()
        except Exception as ex:
            precioTarifa = None

        tasa = None
        codigocont = self.object.codigoContable.codigo
        if codigocont == '02' or codigocont == '03':
            try:
                tasa = Tasa.objects.get(referencia=self.object.id)
                tasa = tasa.to_list()
            except Exception as ex:
                tasa = None

        context['precioTarifa'] = precioTarifa
        context['tasa'] = tasa
        context['defclien'] = config('DEFCLIEN')

        # Gestionamos los botones de Anterior y Siguiente teniendo en cuenta las distintas posibilidades de orderación
        # print(self.request.session.get('search'))
        # print(self.request.session.get('order_col_name'))
        order_col_name = self.request.session.get('order_col_name')
        if order_col_name == 'referencia':
            filtro_prev = self.get_queryset().filter(Q(referencia__lt=self.object.referencia)).order_by('-referencia')
            filtro_next = self.get_queryset().filter(Q(referencia__gt=self.object.referencia)).order_by('referencia')
        elif order_col_name == '-referencia':
            filtro_prev = self.get_queryset().filter(Q(referencia__gt=self.object.referencia)).order_by('referencia')
            filtro_next = self.get_queryset().filter(Q(referencia__lt=self.object.referencia)).order_by('-referencia')
        elif order_col_name == 'descripcion':
            filtro_prev = self.get_queryset().filter((Q(descripcion__lt=self.object.descripcion)) | (Q(descripcion__exact=self.object.descripcion) & Q(pk__lt=self.object.pk))).order_by('-descripcion', '-id')
            filtro_next = self.get_queryset().filter((Q(descripcion__gt=self.object.descripcion)) | (Q(descripcion__exact=self.object.descripcion) & Q(pk__gt=self.object.pk))).order_by('descripcion', 'id')
        elif order_col_name == '-descripcion':
            filtro_prev = self.get_queryset().filter((Q(descripcion__gt=self.object.descripcion)) | (Q(descripcion__exact=self.object.descripcion) & Q(pk__lt=self.object.pk))).order_by('descripcion', '-id')
            filtro_next = self.get_queryset().filter((Q(descripcion__lt=self.object.descripcion)) | (Q(descripcion__exact=self.object.descripcion) & Q(pk__gt=self.object.pk))).order_by('-descripcion', 'id')
        elif order_col_name == 'existencias':
            filtro_prev = self.get_queryset().filter((Q(existencias__lt=self.object.existencias)) | (Q(existencias__exact=self.object.existencias) & Q(pk__lt=self.object.pk))).order_by('-existencias', '-id')
            filtro_next = self.get_queryset().filter((Q(existencias__gt=self.object.existencias)) | (Q(existencias__exact=self.object.existencias) & Q(pk__gt=self.object.pk))).order_by('existencias', 'id')
        elif order_col_name == '-existencias':
            filtro_prev = self.get_queryset().filter((Q(existencias__gt=self.object.existencias)) | (Q(existencias__exact=self.object.existencias) & Q(pk__lt=self.object.pk))).order_by('existencias', '-id')
            filtro_next = self.get_queryset().filter((Q(existencias__lt=self.object.existencias)) | (Q(existencias__exact=self.object.existencias) & Q(pk__gt=self.object.pk))).order_by('-existencias', 'id')
        elif order_col_name == 'tarifa':
            filtro_prev = self.get_queryset().filter((Q(tarifa__lt=self.object.tarifa)) | (Q(tarifa__exact=self.object.tarifa) & Q(pk__lt=self.object.pk))).order_by('-tarifa', '-id')
            filtro_next = self.get_queryset().filter((Q(tarifa__gt=self.object.tarifa)) | (Q(tarifa__exact=self.object.tarifa) & Q(pk__gt=self.object.pk))).order_by('tarifa', 'id')
        elif order_col_name == '-tarifa':
            filtro_prev = self.get_queryset().filter((Q(tarifa__gt=self.object.tarifa)) | (Q(tarifa__exact=self.object.tarifa) & Q(pk__gt=self.object.pk))).order_by('tarifa', '-id')
            filtro_next = self.get_queryset().filter((Q(tarifa__lt=self.object.tarifa)) | (Q(tarifa__exact=self.object.tarifa) & Q(pk__gt=self.object.pk))).order_by('-tarifa', 'id')

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


class ArticuloInformeTasasView(BaseDetailView):

    folder = 'articulos'

    def get(self, request, *args, **kwargs):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setTitle('Informe de Tasas')
        p.setAuthor('SirioWeb')
        p.setSubject('Informe de Tasas')

        width_page, height_page = A4
        print(f'width_page: {width_page} - height_page {height_page}')
        margen_ancho = 30
        end_header = height_page*0.8

        # for font in p.getAvailableFonts():
        #     print(font)

        styles = getSampleStyleSheet()
        # print(styles.byName)

        # Header
        p.setLineWidth(.3)

        papp = '<font name=helvetica size=14 color="#007bff"><b>Sirio</b>Web</font>'
        para = Paragraph(papp, style=styles["Normal"])
        para.wrapOn(p, width_page, height_page)
        para.drawOn(p, margen_ancho, 800)

        # p.setFont('Helvetica-Bold', 20)
        # p.drawString(margen_ancho, 800, 'Sirio')
        # p.setFont('Helvetica', 20)
        # p.drawString(margen_ancho+45, 800, 'Web')

        p.setFont('Helvetica', 12)
        p.drawString(480, 800, '21/05/2022')
        p.drawString(margen_ancho, 780, config('DEFEMPRE'))

        config('DEFCLIEN')
        p.setFont('Helvetica', 12)
        p.drawString(margen_ancho, end_header+9, 'Informe de Tasas')

        # p.line(margen_ancho, end_header, width_page-margen_ancho, end_header)

        # Table

        # styleBH = styles['Normal']
        # styleBH.alignment = TA_LEFT
        # styleBH.fontSize = 10
        # styleBH.color

        tblstyle = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(0x007bff)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONT', (0, 1), (-1, -1), 'Helvetica'),
            # ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ])

        # referencia = Paragraph('Referencia')
        referencia = Paragraph('<font name=helvetica size=10 color=white><b>Referencia</b></font>')
        # denominacion = Paragraph('Denominación', styleBH)
        denominacion = Paragraph('<font name=helvetica size=10 color=white><b>Denominación</b></font>')
        pvp = Paragraph('<font name=helvetica size=10 color=white><b>P.V.P.</b></font>')
        dto = Paragraph('<font name=helvetica size=10 color=white><b>Dto.</b></font>')

        data = []
        data.append([referencia, denominacion, pvp, dto])

        # Table body
        # styleN = styles['BodyText']
        # styleN.alignment = TA_LEFT
        # styleN.fontSize = 8

        high = 650
        for tasa in Tasa.objects.all():
            this_tasa = [tasa.referencia.referencia, tasa.denominacion, tasa.precio, tasa.descuento]
            data.append(this_tasa)
            high -= 18

        tabla = Table(data, colWidths=[4*cm, 8*cm, 3*cm, 3*cm], style=tblstyle)
        # table.setStyle(tblstyle)
        tabla.wrapOn(p, width_page, height_page)
        tabla.drawOn(p, margen_ancho, high)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='infTasas.pdf')
