from django.shortcuts import render

# Create your views here.
from .models import Matricula
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from Admision.models import admisione


class MatriculasList(ListView):
    model = Matricula
    template_name = 'matriculas/matriculas.html'
    def get_context_data(self, **kwargs):
        matriculas = Matricula.objects.all()
        ac = 0
        ne = 0
        context= super(MatriculasList, self).get_context_data(**kwargs)
        context['matriculas'] = matriculas
        context['Titulo'] = "LISTADO DE MATRICULAS"
        return context

def CAdmisionListaEstudiante(request):

    adm = admisione.objects.all() # obtengo las admisiones de un estudiante...
    ac = 0 # contador para ver estudiantes con matricula
    ne = 0 # contador para ver estudiantes sin matriucla
    contexto = {'pvigentes':ac,'nvigentes':ne,'Titulo':'Estudiantes para Matricula', 'admisiones':adm}
    return render(request,'matriculas/generarMatricula.html',contexto)