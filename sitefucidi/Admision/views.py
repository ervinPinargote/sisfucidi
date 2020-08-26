from django.shortcuts import render
from .models import admisione
# Create your views here.
# funcion que permite listar las materias del programa academico



def CAdmisionLista(request):
    adm = admisione.objects.all()
    ac = 0
    ne = 0
   # n= mat.count()
   #for i in mat:
    #    if (i.estado == True):
    #        ac = ac +1
    #    else:
    #        ne=ne+1
    contexto = {'admisiones':adm,'pvigentes':ac,'nvigentes':ne}
    return render(request,'admision/admision.html',contexto)