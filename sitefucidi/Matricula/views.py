
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.functional import empty
from django.views import View
from xhtml2pdf import pisa

from .forms import cMatriculaForm
from .models import Matricula
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from Admision.models import admisione
from Academico.models import Materia

import os
from django.conf import settings


class MatriculasList(ListView):
    model = Matricula
    template_name = 'matriculas/matriculas.html'
    def get_context_data(self, **kwargs):
        matriculas = Matricula.objects.all()
        ac = 0
        ne = 0
        context= super(MatriculasList, self).get_context_data(**kwargs)
        context['matriculas'] = matriculas
        context['Titulo'] = "Matrículas"
        return context

def CAdmisionListaEstudiante(request):

    adm = admisione.objects.all() # obtengo las admisiones de un estudiante...
    ac = 0 # contador para ver estudiantes con matricula
    ne = 0 # contador para ver estudiantes sin matriucla
    contexto = {'pvigentes':ac,'nvigentes':ne,'Titulo':'Estudiantes para Matricula', 'admisiones':adm}
    return render(request,'matriculas/generarMatricula.html',contexto)


def cMatricula(request,id_adm):
    adm = admisione.objects.get(id=id_adm)  # Datos de la Admision a Generar Matricula
    materias = Materia.objects.all().filter(cod_programa=adm.Programa.id)
    materiasMatriculdas = Matricula.objects.all().filter(admision_id = adm.id)
    #entry_list = list(Materia.objects.all().filter(cod_programa=adm.Programa.id)) #MATERIAS PROGRAMA ACADEMICO
    #persona = Persona.objects.get(ci=id_persona)
    #entry_list3=[]
    #entry_list1 = list(Matricula.objects.all().filter(admision_id = adm.id).values_list('materias',flat=True)) #Materias que ha tomado
    #for i in entry_list:
    #    for j in  entry_list1:
    #       a = i.cod_materia
    #        if i.cod_materia == j:
    #            if i not in entry_list3:
    #              entry_list3.append(i)
    if request.method == 'POST':
        form = cMatriculaForm(request.POST)
        if form.is_valid():
            admisionEs = form.save(commit=False)
            admisionEs.save()
            form.save_m2m()
        return redirect('matricula:MatriculasList')
    else:
        form = cMatriculaForm()
    contexto = {'form': form, 'admision': adm, 'materias':materias, 'Matriculas':materiasMatriculdas}
    return render(request, 'matriculas/FormMatriculacion.html', contexto)

class MatriculaFicha(UpdateView):
    model=Matricula
    form_class = cMatriculaForm
    template_name = 'matriculas/FichaMatricula.html'
    success_url = reverse_lazy('matricula:MatriculasList')
    def get_context_data(self, **kwargs):
        idM = self.kwargs.get('pk', None)
        mate = Matricula.objects.get(cod_matricula = idM)
        admision = admisione.objects.get(id=mate.admision_id.id)
        context = super(MatriculaFicha, self).get_context_data(**kwargs)
        context['Titulo'] = "Ficha Matricula"
        context['admision'] =admision
        context['matricula'] = mate
        return context

class pdfMatricula_view(LoginRequiredMixin,View):
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
        matricula = Matricula.objects.get(pk=self.kwargs['pk'])
        user = User.objects.get(username=self.request.user) # envia el usuario que esta en la logueado en la aplicacion.
        template_path = 'matriculas/Reportes/Matricula.html'
        fecha= datetime.date.today()
        context = {'tittle': 'Reporte de Matricula :','matricula':matricula ,
                   'codigo': matricula.admision_id.ci.ci,
                   'icon':'{}{}'.format(settings.MEDIA_URL, 'logo13.png'),
                   'date':fecha,
                   'usuario':user
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+matricula.admision_id.ci.ci+".pdf"
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