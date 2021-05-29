import decimal
import datetime
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from xhtml2pdf import pisa

from .forms import DetallesPagosForm
from .models import Pago, detalle_pagos


# Create your views here.
class PagosMatriculaList(ListView):
    model = Pago
    template_name = 'gestion_pagos/pagos_matricula.html'
    def get_context_data(self, **kwargs):
        pagos = Pago.objects.all()
        context= super(PagosMatriculaList, self).get_context_data(**kwargs)
        context['matriculas'] = pagos
        context['Titulo'] = "Pagos Matricula"
        return context

#Generación de vista de Agregar Pagos a la ficha de matricula
def cAgregarValor(request, id_pago):
    valores =detalle_pagos.objects.all().filter(pago_id = id_pago).order_by('-id')# valores que se han ingresado en la tabla de pagos
    pago_datos = Pago.objects.get(id=id_pago)
    valCancelado = 0.00
    for i in valores:
         valCancelado = decimal.Decimal(valCancelado) + i.valor_cancelado

    Saldo_adeudado = pago_datos.valor_pagar - decimal.Decimal(valCancelado)
    mensaje = "Error"
    if request.method == 'POST':
        form = DetallesPagosForm(request.POST,request.FILES)
        if form.is_valid():
             if form.save()==True:
                 mensaje = "Guardado con exito"
        return redirect('pago:PagoLista')
    else:
        form = DetallesPagosForm()
    contexto = {'form': form, 'Valores': valores, 'mensaje': mensaje,'id':id_pago, 'pgd':pago_datos, 'saldo':Saldo_adeudado}
    return render(request, 'gestion_pagos/ModalAgregarPago.html', contexto)



# REPORTES PDF DE PAGOS
class pdfPagoMatricula_view(LoginRequiredMixin,View):
    def link_callback(self,uri,rel):
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

    def get(self, request,*args,**kwargs):
        id_pago = self.kwargs['pk']
        valores = detalle_pagos.objects.all().filter(pago_id=id_pago).order_by('id')  # valores que se han ingresado en la tabla de pagos
        pago_datos = Pago.objects.get(id=id_pago)
        valCancelado = 0.00
        for i in valores:
            valCancelado = decimal.Decimal(valCancelado) + i.valor_cancelado
        Saldo_adeudado = pago_datos.valor_pagar - decimal.Decimal(valCancelado)

        user = User.objects.get(username=self.request.user) # envia el usuario que esta en la logueado en la aplicacion.
        template_path = 'gestion_pagos/Reportes/PagoMatricua.html'
        fecha= datetime.date.today()
        context = {'tittle': 'Orden Pago :','pago':pago_datos ,
                   'valores':valores,
                   'codigo': pago_datos.cod_matricula.admision_id.ci.ci,
                   'icon':'{}{}'.format(settings.MEDIA_URL, 'logo13.png'),
                   'date':fecha,
                   'valorCancelado':valCancelado,
                   'ValorAdeudado':Saldo_adeudado,
                   'usuario':user
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+pago_datos.cod_matricula.admision_id.ci.ci+".pdf"
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
                return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisaStatus.err,  html))
        return response