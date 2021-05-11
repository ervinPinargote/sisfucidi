import datetime
import json
from sys import path

import uri as uri
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.serializers import serialize

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView
# Create your views here.


from .forms import ProgramaNuevo, ProgramaEditar, MateriaNuevo, MateriaEditar, ValoresMatriculaForm
from .models import Programa, Materia, Valor_matricula

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User

from .utils import render_to_pdf


def CprograLista(request):
    program = Programa.objects.all()
    ac = 0
    ne = 0
    n= program.count()
    for i in program:
        if (i.vigencia==True):
            ac = ac +1
        else:
           ne = ne +1
    contexto = {'programas':program,'pvigentes':ac,'nvigentes':ne}
    return render(request,'academia/listar_programas.html',contexto)

def CprograNuevo(request):

     codigo = Programa.objects.last() # se obtiene el ultimo registro de la BD
     mensaje = "asjkajks"
     if request.method == 'POST':
         form = ProgramaNuevo(request.POST)
         if form.is_valid():
             if form.save()==True:
                 mensaje = "Exitoso"
             else:
                 mensaje = "Error al Guardar datos"
         return redirect('academia:Listar')
     else:
         form = ProgramaNuevo()
     return render(request,'academia/nuevo.html',{'form':form,'codigo':codigo, 'mensaje':mensaje, 'title':"Agregar"})

def CprogramaEditar(request, id_programa):
    program = Programa.objects.get(id=id_programa)
    if (request.method == 'GET'):
        form = ProgramaEditar(instance = program)
    else:
        form = ProgramaEditar(request.POST, instance= program)
        if form.is_valid():
            form.save()
        return redirect('academia:Listar') # Redirijo a la Listar que es Principal en el funcionalidad
    return render(request,'academia/nuevo.html',{'form':form,'title':"Editar"}) # Usamos el mismo Formulario para un nuevo Programa


class EliminarPrograma(DeleteView):
    model = Programa   # AKI SE COLOCA EL NOMBRE DEL MODELO
    template_name = 'academia/Eliminar.html'
    success_url = reverse_lazy('academia:Listar')

def CprogramaEliminar(request, id_programa):
    program = Programa.objects.get(id=id_programa)
    if (request.method == 'POST'):
        program.delete()
        return redirect('academia:Listar') # Redirijo a la Listar que es Principal e
    return render(request,'academia/Eliminar.html',{'programa':program}) # Usamos el mismo For

# funcion que permite listar las materias del programa academico
def CMateriaLista(request):
    mat = Materia.objects.all()
    ac = 0
    ne = 0
    n= mat.count()
    for i in mat:
        if (i.estado == True):
            ac = ac +1
        else:
            ne=ne+1
    contexto = {'materias':mat,'pvigentes':ac,'nvigentes':ne}
    return render(request,'academia/materias/materias.html',contexto)

# funcion que permite Registrar una nueva materia
def CMateriaNuevo(request,cd_programa):
    global materiaRegistrada
    materias = Materia.objects.all().filter(cod_programa = cd_programa)
    num=Materia.objects.all().count() + 1 #Genero el nuevo Indice
    error =""
    if request.method == 'POST': # preguntamos si es un metodo POST.
        form = MateriaNuevo(request.POST) # Instaciomos el  formulario creado
        if form.is_valid():
            if form.save():
                error = "Se Registro Materia "+ request.POST.get("nombre_materia")
                nuevo_id = int(request.POST.get("materia_id")) + 1
                materiasF1 = Materia.objects.filter(cod_programa=cd_programa).order_by('-materia_id')[:1]
                materiasF = serializers.serialize('json', materiasF1)
                #prices_json = serialize('json', materiasF)
                for i in materiasF1:
                    materiaRegistrada= {'id':i.materia_id,'cod_materia':i.cod_materia,'nombre_materia':i.nombre_materia,'valorP':i.valor_presencial,'valorO':i.valor_online,}
            return JsonResponse({'content': {'message': error,'color':'success', 'materias':materiasF,'nuevo_id':nuevo_id,'materiaRegistrada':materiaRegistrada,}})
        else :
            error = "Se genero un erro al guardar "+ request.POST.get("nombre_materia") + "Al parecer esta materia ya existe.!"
            return JsonResponse({'content': {'message': error, 'color':'danger','nuevo_id':request.POST.get("materia_id"),}})
    else:
        form = MateriaNuevo()
    return render(request, 'academia/materias/AgregarMateriasModal.html', {'form': form, 'title':"Agregar", 'programa':cd_programa , 'materias':materias,'ID':num})


# funcion para editar una materia....
def CMateriaEditar(request, id_materia):
    materia = Materia.objects.get(cod_materia=id_materia)  # comparacion donde se verifica el Id que vamos a editar.
    if (request.method == 'GET'):
        form =  MateriaEditar(instance = materia) # Se puede crear un nuevo formulario para bloquear campos que sean no editables.
    else:
        form = MateriaNuevo(request.POST, instance= materia)
        if form.is_valid():
            form.save()
        return redirect('academia:ListarMaterias') # Redirijo a la Listar que es Principal en el funcionalidad
    return render(request,'academia/materias/nuevomat.html',{'form':form,'edit':1,'title':"Editar"}) # Usamos el mismo Formulario para un nuevo Programa

# funcion que permite eliminar una materia
def CMateriaEliminar(request, id_materia):
    materia = Materia.objects.get(cod_materia=id_materia)
    if (request.method == 'POST'):
        materia.delete()
        return redirect('academia:ListarMaterias') # Redirijo a la Listar que es Principal en la funcionalidad
    return render(request,'academia/materias/Eliminar.html',{'materia':materia}) # enviamos el contexto que es la materia a elminar.


#Generación de vista de Agregar Valor de Programa Academico
def cAgregarValor(request, cd_programa):
    valores =Valor_matricula.objects.all().filter(cod_programa = cd_programa).order_by('-fecha').order_by('-id')# valores que se han ingresado en la tabla de matriculas
    mensaje = "Error"
    if request.method == 'POST':
        form = ValoresMatriculaForm(request.POST)
        if form.is_valid():
             if form.save()==True:
                 mensaje = "Guardado con exito"
        return redirect('academia:Listar')
    else:
        form = ValoresMatriculaForm()
    contexto = {'form': form, 'Valores': valores, 'mensaje': mensaje,'programa':cd_programa}
    return render(request, 'academia/Valor_Matricula.html', contexto)




# Generacion de Reportes
class pdfMalla_view(View):
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
        mat = Materia.objects.all()
        program = Programa.objects.all()
        user = User.objects.get(username=self.request.user)  # envia el usuario que esta en la logueado en la aplicacion.
        template_path = 'academia/Reportes/Reporte.html'
        fecha= datetime.date.today()
        context = {'tittle': 'Programas de Estudios','programas':program , 'c':mat,
                   'icon':'{}{}'.format(settings.MEDIA_URL, 'logo13.png'),
                   'date':fecha,
                   'usuario': user
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
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

class pdfMateria_view(LoginRequiredMixin,View):
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
        mat = Materia.objects.all().order_by('nivel')
        program = Programa.objects.get(pk=self.kwargs['pk'])
        user = User.objects.get(username=self.request.user) # envia el usuario que esta en la logueado en la aplicacion.
        template_path = 'academia/Reportes/ReportePrograma.html'
        fecha= datetime.date.today()
        context = {'tittle': program.nombre_programa,'programa':program , 'mat':mat,
                   'icon':'{}{}'.format(settings.MEDIA_URL, 'logo13.png'),
                   'date':fecha,
                   'usuario':user
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+program.nombre_programa+".pdf"
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