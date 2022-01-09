import decimal
import datetime
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from xhtml2pdf import pisa

from .forms import PagosForm, DetallesPagosForm, FormMateriaPago
from .models import Pago, detalle_pagos, materia_recibir

from Academico.models import Materia, CnotasEstudiante


# Create your views here.


class PagosMatriculaList(LoginRequiredMixin,ListView):
    model = Pago
    template_name = 'gestion_pagos/pagos_matricula.html'

    def get_context_data(self, **kwargs):
        pagos = Pago.objects.all().filter(cod_pago__contains='PAM')
        context = super(PagosMatriculaList, self).get_context_data(**kwargs)
        context['matriculas'] = pagos
        context['Titulo'] = "Pagos Matricula"
        return context


# Generación de vista de Agregar Pagos a la ficha de matricula
def cAgregarValor(request, id_pago):
    valores = detalle_pagos.objects.all().filter(pago_id=id_pago).order_by(
        '-id')  # valores que se han ingresado en la tabla de pagos
    pago_datos = Pago.objects.get(id=id_pago)
    valCancelado = 0.00
    for i in valores:
        valCancelado = decimal.Decimal(valCancelado) + i.valor_cancelado

    Saldo_adeudado = pago_datos.valor_pagar - decimal.Decimal(valCancelado)
    mensaje = "Error"
    if request.method == 'POST':
        saldopendiente = request.POST.get("Valor_pendiente")
        valpagado = request.POST.get("valor_cancelado")
        form = DetallesPagosForm(request.POST, request.FILES)
        if form.is_valid():
            if form.save():
                Pago.objects.filter(pk=pago_datos.id).update(valor_pagado=valCancelado+decimal.Decimal(valpagado))
                if (float(saldopendiente) <= 0):
                    Pago.objects.filter(pk=pago_datos.id).update(estado=True)
                mensaje = "Guardado con exito"
        return redirect('pago:PagoLista')
    else:
        form = DetallesPagosForm()
    contexto = {'form': form, 'Valores': valores, 'mensaje': mensaje, 'id': id_pago, 'pgd': pago_datos,
                'saldo': Saldo_adeudado}
    return render(request, 'gestion_pagos/ModalAgregarPago.html', contexto)


# Creacion del menu de pagos
class PagosColegiaturaList(LoginRequiredMixin,ListView):
    model = Pago
    template_name = 'gestion_pagos/colegiatura/Pagos_Colegiatura.html'

    def get_context_data(self, **kwargs):
        pagos = Pago.objects.all().filter(cod_pago__contains='PAC')
        matpgos = materia_recibir.objects.all()
        context = super(PagosColegiaturaList, self).get_context_data(**kwargs)
        context['pagos'] = pagos
        context['matpgos'] = matpgos
        context['Titulo'] = "Pagos Colegiatura"
        return context


class PagosColegiaturaEstudHabilList(ListView):
    model = Pago
    template_name = 'gestion_pagos/colegiatura/pago_gen_matricula.html'

    def get_context_data(self, **kwargs):
        pagos = Pago.objects.all().filter(cod_pago__contains='PAM')
        context = super(PagosColegiaturaEstudHabilList, self).get_context_data(**kwargs)
        context['pagos'] = pagos
        context['Titulo'] = "Estudiantes Habilitados para pago"
        return context


# Generación de vista de Agregar Pagos de Colegiatura
def cAgregarPago(request, id_pago):
    pago_datos = Pago.objects.get(id=id_pago)  # primero obtengo los datos del pago.
    tipodematricula = pago_datos.cod_matricula.modalidad  # Obtengo cual fue la modalidad de la matricula
    id_prog = pago_datos.cod_matricula.admision_id.Programa.id  # id del programa para mostrar las materias
    materias = Materia.objects.all().filter(cod_programa=id_prog)
    mensaje = "Error"
    idpago = None
    obpago = Pago.objects.all().order_by('-id')[:1]
    for i in obpago:
        idpago = i.id + 1
    # verificamos idPago
    codigoP = " "
    if idpago == None:
        idpago = Pago.objects.all().count() + 1
    if idpago >= 10 and idpago <= 99:
        codigoP = "PAC-0" + str(idpago)
    else:
        if idpago > 99:
            codigoP = "PAC-" + str(idpago)
        else:
            codigoP = "PAC-00" + str(idpago)
    if request.method == 'POST':
        form = PagosForm(request.POST)
        if form.is_valid():
            if form.save():
                np = Pago.objects.get(id=idpago)
                mt = Materia.objects.get(cod_materia=request.POST.get("materia_asignada"))
                OpagoMateria = materia_recibir(fecha=request.POST.get("fecha_generacion"), materia_asignada=mt,
                                               pago_id=np)
                OpagoMateria.save()  # Se genera la materia recibir del estudiante.
                # proceso generar notas y asistencia del estudiante
                OnotasAc = CnotasEstudiante(fecha_subir_nota=request.POST.get("fecha_generacion"), notaestudiante=-1.00,
                                            asitencia=0, id_pago_materia=np)
                OnotasAc.save()
                msg = "Se Registro con exito el pago de colegiatura " + request.POST.get("cod_pago")
            return JsonResponse({'content': {'message': msg, 'color': 'success', }})
        else:
            msg = "Se genero un error al generar el pago de colegiatura " + request.POST.get(
                "cod_pago") + "Al parecer este pago ya existe.!"
            return JsonResponse({'content': {'message': msg, 'color': 'danger', }})
    else:
        form = PagosForm()
        form2 = FormMateriaPago()
        contexto = {'form': form, 'tipoM': tipodematricula, 'mensaje': mensaje, 'id': id_pago, 'pgd': pago_datos,
                    'materias': materias, 'form2': form2, 'codigo': codigoP}
    return render(request, 'gestion_pagos/colegiatura/modal_form_pago.html', contexto)


# Generación de vista de Agregar Pagos de Colegiatura
def cFichaPago(request, id_pago):
    detallemateria = materia_recibir.objects.get(id=id_pago)  # obtengo el obejecto al cual hago referencia
    pago_datos = Pago.objects.get(id=detallemateria.pago_id.id)  # primero obtengo los datos del pago.
    tipodematricula = pago_datos.cod_matricula.modalidad  # Obtengo cual fue la modalidad de la matricula
    id_prog = pago_datos.cod_matricula.admision_id.Programa.id  # id del programa para mostrar las materias
    materias = Materia.objects.all().filter(cod_programa=id_prog)
    mensaje = "Error"
    if request.method == 'POST':
        form = PagosForm(request.POST)
        if form.is_valid():
            if form.save():
                msg = "Se Registro con exito el pago de colegiatura " + request.POST.get("cod_pago")
            return JsonResponse({'content': {'message': msg, 'color': 'success', }})
        else:
            msg = "Se genero un error al generar el pago de colegiatura " + request.POST.get(
                "cod_pago") + "Al parecer este pago ya existe.!"
            return JsonResponse({'content': {'message': msg, 'color': 'danger', }})
    else:
        form = PagosForm()
        form2 = FormMateriaPago()
        contexto = {'form': form, 'tipoM': tipodematricula, 'mensaje': mensaje, 'id': id_pago, 'pgd': pago_datos,
                    'materias': materias, 'form2': form2, 'codigo': mensaje, 'detM': detallemateria}
    return render(request, 'gestion_pagos/colegiatura/fichaPago.html', contexto)


# REPORTES PDF DE PAGOS
class pdfPagoMatricula_view(LoginRequiredMixin, View):
    def link_callback(self, uri, rel):
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri
        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        id_pago = self.kwargs['pk']
        valores = detalle_pagos.objects.all().filter(pago_id=id_pago).order_by(
            'id')  # valores que se han ingresado en la tabla de pagos
        pago_datos = Pago.objects.get(id=id_pago)
        valCancelado = 0.00
        for i in valores:
            valCancelado = decimal.Decimal(valCancelado) + i.valor_cancelado
        Saldo_adeudado = pago_datos.valor_pagar - decimal.Decimal(valCancelado)

        user = User.objects.get(
            username=self.request.user)  # envia el usuario que esta en la logueado en la aplicacion.
        template_path = 'gestion_pagos/Reportes/PagoMatricua.html'
        fecha = datetime.date.today()
        context = {'tittle': 'Orden Pago :', 'pago': pago_datos,
                   'valores': valores,
                   'codigo': pago_datos.cod_matricula.admision_id.ci.ci,
                   'icon': '{}{}'.format(settings.MEDIA_URL, 'logo13.png'),
                   'date': fecha,
                   'valorCancelado': valCancelado,
                   'ValorAdeudado': Saldo_adeudado,
                   'usuario': user
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + pago_datos.cod_matricula.admision_id.ci.ci + ".pdf"
        template = get_template(template_path)
        html = template.render(context)
        if request.POST.get('show_html', ''):
            response['Content-Type'] = 'application/text'
            response['Content-Disposition'] = 'attachment; filename="ABC.txt"'
            response.write(html)
        else:
            pisaStatus = pisa.CreatePDF(
                html.encode("UTF-8"), dest=response, link_callback=self.link_callback)
            if pisaStatus.err:
                return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisaStatus.err, html))
        return response


class pdfEstadoPagoMatricula_view(LoginRequiredMixin, View):
    def link_callback(self, uri, rel):
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri
        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        valpago=0
        salPendiente=0
        tipo_reporte = self.kwargs['pk']
        if (tipo_reporte == "R1"):
            pagos = Pago.objects.all().filter(cod_pago__contains='PAM', estado=True)
            pago_estado = 'Pago Completo'
            name_report = 'Reporte de estudiantes con '
            tipo = True
            for pag in pagos:
                valpago = valpago + pag.valor_pagar
                salPendiente = salPendiente + (pag.valor_pagar-pag.valor_pagado)
        else:
            pagos = Pago.objects.all().filter(cod_pago__contains='PAM', estado=False)
            pago_estado = 'Pago Incompleto'
            name_report = 'Reporte de estudiantes con '
            tipo = False
            for pag in pagos:
                valpago = valpago + pag.valor_pagar # valor a cobrar en total
                salPendiente = salPendiente + (pag.valor_pagar-pag.valor_pagado)
        user = User.objects.get(
            username=self.request.user)  # envia el usuario que esta en la logueado en la aplicacion.
        template_path = 'gestion_pagos/Reportes/ReporteGeneral.html'
        fecha = datetime.date.today()
        context = {'tittle': 'Reporte de pagos de matricula',
                   'valores': pagos,
                   'codigo': pago_estado,
                   'icon': '{}{}'.format(settings.MEDIA_URL, 'logo13.png'),
                   'date': fecha,
                   'tipo':tipo,
                   'valorCancelado': valpago,
                   'ValorAdeudado': salPendiente,
                   'usuario': user
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + name_report + pago_estado + ".pdf"
        template = get_template(template_path)
        html = template.render(context)
        if request.POST.get('show_html', ''):
            response['Content-Type'] = 'application/text'
            response['Content-Disposition'] = 'attachment; filename="ABC.txt"'
            response.write(html)
        else:
            pisaStatus = pisa.CreatePDF(
                html.encode("UTF-8"), dest=response, link_callback=self.link_callback)
            if pisaStatus.err:
                return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisaStatus.err, html))
        return response


class pdfEstadoPagoMatricula_view1(ListView):
    model = Pago
    template_name = 'gestion_pagos/Reportes/ModalSelectReporte.html'


# REPORTES PDF DE COMPROBANTE DE COLEGIATURA
class pdfPagoColegiatura_view(LoginRequiredMixin, View):
    def link_callback(self, uri, rel):
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri
        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        id_pago = self.kwargs['pk']
        valoresMAT = materia_recibir.objects.all().filter(pago_id=id_pago).order_by(
            'id')  # valores que se han ingresado en la tabla de pagos
        pago_datos = Pago.objects.get(id=id_pago)
        valCancelado = 0.00
        # for i in valores:
        #    valCancelado = decimal.Decimal(valCancelado) + i.valor_cancelado
        # Saldo_adeudado = pago_datos.valor_pagar - decimal.Decimal(valCancelado)

        user = User.objects.get(
            username=self.request.user)  # envia el usuario que esta en la logueado en la aplicacion.
        template_path = 'gestion_pagos/Reportes/PagoColegiatura.html'
        fecha = datetime.date.today()
        context = {'tittle': 'Orden Pago :', 'pago': pago_datos,
                   'valores': valoresMAT,
                   'codigo': pago_datos.cod_matricula.admision_id.ci.ci,
                   'icon': '{}{}'.format(settings.MEDIA_URL, 'logo13.png'),
                   'date': fecha,
                   'valorCancelado': pago_datos.valor_pagar,
                   'ValorAdeudado': pago_datos.valor_pagado - pago_datos.valor_pagar,
                   'usuario': user
                   }
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename=' + 'Colegiatura-' + pago_datos.cod_matricula.admision_id.ci.ci + ".pdf"
        template = get_template(template_path)
        html = template.render(context)
        if request.POST.get('show_html', ''):
            response['Content-Type'] = 'application/text'
            response['Content-Disposition'] = 'attachment; filename="ABC.txt"'
            response.write(html)
        else:
            pisaStatus = pisa.CreatePDF(
                html.encode("UTF-8"), dest=response, link_callback=self.link_callback)
            if pisaStatus.err:
                return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisaStatus.err, html))
        return response
