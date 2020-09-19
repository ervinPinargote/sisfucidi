from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
# Create your views here.
from .forms import ProgramaNuevo, ProgramaEditar, MateriaNuevo
from .models import Programa, Materia


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
     return render(request,'academia/nuevo.html',{'form':form,'codigo':codigo, 'mensaje':mensaje})

def CprogramaEditar(request, id_programa):
    program = Programa.objects.get(id=id_programa)
    if (request.method == 'GET'):
        form = ProgramaEditar(instance = program)
    else:
        form = ProgramaEditar(request.POST, instance= program)
        if form.is_valid():
            form.save()
        return redirect('academia:Listar') # Redirijo a la Listar que es Principal en el funcionalidad
    return render(request,'academia/nuevo.html',{'form':form}) # Usamos el mismo Formulario para un nuevo Programa


class EliminarPrograma(DeleteView):
    model = Programa   # AKI SE COLOCA EL NOMBRE DEL MODELO
    template_name = 'academia/Eliminar.html'
    success_url = reverse_lazy('academia:Listar')


def CprogramaEliminar(request, id_programa):
    program = Programa.objects.get(id=id_programa)
    if (request.method == 'POST'):
        program.delete()
        return redirect('academia:Listar') # Redirijo a la Listar que es Principal e
    return render(request,'academia/eliminar.html',{'programa':program}) # Usamos el mismo For


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
def CMateriaNuevo(request):
    if request.method == 'POST': # preguntamos si es un metodo POST.
        form = MateriaNuevo(request.POST) # Instaciomos el  formulario creado
        if form.is_valid():
            form.save()
        return redirect('academia:ListarMaterias')
    else:
        form = MateriaNuevo()
    return render(request, 'academia/materias/nuevomat.html', {'form': form})

# funcion para editar una materia....
def CMateriaEditar(request, id_materia):
    materia = Materia.objects.get(cod_materia=id_materia)  # comparacion donde se verifica el Id que vamos a editar.
    if (request.method == 'GET'):
        form = MateriaNuevo(instance = materia) # Se puede crear un nuevo formulario para bloquear campos que sean no editables.
    else:
        form = MateriaNuevo(request.POST, instance= materia)
        if form.is_valid():
            form.save()
        return redirect('academia:ListarMaterias') # Redirijo a la Listar que es Principal en el funcionalidad
    return render(request,'academia/materias/nuevomat.html',{'form':form}) # Usamos el mismo Formulario para un nuevo Programa

# funcion que permite eliminar una materia
def CMateriaEliminar(request, id_materia):
    materia = Materia.objects.get(cod_materia=id_materia)
    if (request.method == 'POST'):
        materia.delete()
        return redirect('academia:ListarMaterias') # Redirijo a la Listar que es Principal en la funcionalidad
    return render(request,'academia/materias/eliminar.html',{'materia':materia}) # enviamos el contexto que es la materia a elminar.