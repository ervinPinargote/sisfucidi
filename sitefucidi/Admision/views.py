
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse, resolve
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .forms import admisioneForm, PersonaForm, ExpereciaForm, TrasfondoForm, estudiosForm, recomendacionesForm, \
    AsignacionMaterias
from .models import admisione, estudios_realizado, Persona, asignacionMaterias


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

class AdmisionCreate(CreateView):
    model = admisione
    template_name = 'admision/nuevo_form.html'
    form_class = admisioneForm  # primer Formulario Principal.
    second_form_class = PersonaForm # Formulario Persona.
    third_form_class = ExpereciaForm # formulario de Experiecia de Espiritual.
    four_form_class = TrasfondoForm # formulario de Transfondo.
    five_form_class = estudiosForm # formularios de Estudios.
    six_form_class =  recomendacionesForm # formulario de recomendaciones.
    success_url = reverse_lazy('admision:Listar')

    def get_context_data(self, **kwargs): # se añaden al contexto los siguientes formularios en orden.
        context = super(AdmisionCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)
        if 'form4' not in context:
            context['form4'] = self.four_form_class(self.request.GET)
        if 'form5' not in context:
            context['form5'] = self.five_form_class(self.request.GET)
        if 'form6' not in context:
            context['form6'] = self.six_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form =  self.form_class(request.POST) #FORMULARIO SOLICITUD
        form2 = self.second_form_class(request.POST)# FORMULARIO PERSONA
        form3 = self.third_form_class(request.POST)# FORMULARIO EXPERIENCIA ESPIRITUAL
        form4 = self.four_form_class(request.POST)# FORMULARIO TRANSFONDO ECLESIASTICO
        form5 = self.five_form_class(request.POST)# FORMULARIO ESTUDIOS REALIZADOS
        form6 = self.six_form_class(request.POST)# FORMULARIO RECOMENDACIONES.
        if form.is_valid() and form2.is_valid():
            pers = form2.save(commit=False)
            estud = form5.save(commit=False)
            solicitud = form.save(commit=False)

            solicitud.ci = form2.save() #GUARDO PRIMERO EL FORMULARIO PERSONA Y ASIGNO EL ID DE CEDULA AL FORMULARIO SOLICITUD
            solicitud.id_ex = form3.save() # GUARDO PRIMERO LA EXPERIENCIA ESPIRIRTUAL Y ASIGONO SU ID.
            solicitud.id_tra = form4.save() # GUARDO EL TRANSFONDO ECLESIASTICO PARA PASAR SU ID.
            # PROCESO PARA GUARDAR ESTUDIOS REALIZADOS

            estudios = estudios_realizado.objects.create(tipo_est=estud.tipo_est,fecha_ini=estud.fecha_ini,fecha_fin=estud.fecha_fin,institucion=estud.institucion,graduacion=estud.graduacion,ci=pers) # creamos el obejeto estudios 2.
            #solicitud.id_estudios.add(estudios)
            solicitud.save() # aki se guarda la solicitud.
            solicitud.id_estudios.add(estudios) # permite guardar una instancia del modelo  Formularios de Estudio al modelo ADMISION MANYTOMANY.
            form.save_m2m() # PERMITE GUARDAR CAMPO MANY TO MANY.

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3 = form3,form4 = form4,form5 = form5,form6 = form6 ))

class DocenteList(ListView):
    model = Persona
    template_name = 'admision/Instructor/instructor.html'
    def get_context_data(self, **kwargs):
        docente = Persona.objects.all().filter(tipo="Instructor")
        ac = 0
        ne = 0
        for i in docente:
            if (i.estado== "Activo"):
                ac = ac + 1
            else:
                ne = ne + 1
        context= super(DocenteList, self).get_context_data(**kwargs)
        context['ActivosD'] = ac
        context['InactivosD'] = ne
        context['Titulo'] = "LISTADO DE INSTRUCTORES"
        return context

    def get_queryset(self):    #intervenimos en el metodo QUERY SET
       queryset = super(DocenteList, self).get_queryset()
       return queryset.filter(tipo="Instructor") # Filtro para Listar solo los Instructores

class DocenteUpdate(UpdateView):
    model=Persona
    form_class = PersonaForm
    template_name = 'admision/Instructor/EditarDocente.html'
    success_url = reverse_lazy('admision:ListarDocente')
    def get_context_data(self, **kwargs):
        context = super(DocenteUpdate, self).get_context_data(**kwargs)
        context['Titulo'] = "Editar"
        return context

class DocenteAgregar(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'admision/Instructor/NuevoDocente.html'
    success_url = reverse_lazy('admision:ListarDocente')

    def get_context_data(self, **kwargs):
        context = super(DocenteAgregar, self).get_context_data(**kwargs)
        context['Titulo'] = "Agregar"
        return context

class DocenteEliminar(DeleteView): # Eliminar un Docente
    model = Persona
    template_name = 'admision/Instructor/eliminar.html'
    success_url = reverse_lazy('admision:ListarDocente')

def CMateriasAsignadasDocente(request, id_docente): # USO UNA FUNCION POR QUE PERMITE AGREGAR AGURMENTOS
    materias = asignacionMaterias.objects.all().filter(instructor=id_docente)
    doc = Persona.objects.all().filter(ci=id_docente) #envio al Docente para accerder A sus Atributos u poder realizazr una nueva
    for i in doc:
        doc = i
    contexto = {'materiasAsig': materias, 'TituloFuncionalidad': "Materias Asignadas", 'Docente': doc}
    return render(request,'admision/Instructor/Listado_materias_asignadas.html',contexto) # Usamos el mismo Formulario para un nuevo Programa

def CMateriasAsignarRegitro(request,id_docente):
    doc = Persona.objects.get(ci=id_docente)
    your_params = {
        'id_docente': id_docente
    }
    if request.method == 'POST': # preguntamos si es un metodo POST.
        form = AsignacionMaterias(request.POST) # Instaciomos el  formulario creado
        if form.is_valid():
            form.save()
        return redirect(reverse('admision:ListaMateriasDocente',kwargs=your_params)) ## RETROCEDER UNA LISTA CON PARAMETROS
    else:
        form = AsignacionMaterias()
    contexto = {'form':form,'doc':doc,'Titulo':'AGREGAR MATERIAS'}
    return render(request, 'admision/Instructor/Asignar_materias.html',contexto)

def CMateriasAsignadasUpdate(request,pk):
    asignado = asignacionMaterias.objects.get(id=pk)  # comparacion donde se verifica el Id que vamos a editar.
    docente = asignado.instructor #Accemos al objeto instructor que contiene los datos de la persona.
    your_params = {
        'id_docente': asignado.instructor.ci
    }
    if (request.method == 'GET'):
        form = AsignacionMaterias(instance=asignado)  # Se puede crear un nuevo formulario para bloquear campos que sean no editables.
    else:
        form = AsignacionMaterias(request.POST, instance=asignado)
        if form.is_valid():
            form.save()
        return redirect(reverse('admision:ListaMateriasDocente',kwargs=your_params))  # Redirijo a la Listar que es Principal en el funcionalidad
    contexto = {'form': form, 'doc': docente, 'Titulo': 'ACTUALIZAR MATERIAS'}
    return render(request, 'admision/Instructor/Asignar_materias.html', contexto)


class EstudianteList(ListView):
    model = Persona
    template_name = 'admision/estudiantes/estudiante.html'
    def get_context_data(self, **kwargs):
        docente = Persona.objects.all().filter(tipo="Estudiante")
        ac = 0
        ne = 0
        for i in docente:
            if (i.estado== "Activo"):
                ac = ac + 1
            else:
                ne = ne + 1
        context= super(EstudianteList, self).get_context_data(**kwargs)
        context['ActivosD'] = ac
        context['InactivosD'] = ne
        context['Titulo'] = "LISTADO DE ESTUDIANTES"
        return context

    def get_queryset(self):    #intervenimos en el metodo QUERY SET
       queryset = super(EstudianteList, self).get_queryset()
       factorb=self.kwargs.get('slug',None)
       EstadoBus = None
       if(factorb=='1'):
           EstadoBus = "Activo"
       else:
           EstadoBus = "Inactivo"
       return queryset.filter(tipo="Estudiante", estado=EstadoBus) # Filtro para Listar solo los Estudiantes.

class EstudianteUpdate(UpdateView):
    model=Persona
    form_class = PersonaForm
    template_name = 'admision/estudiantes/EditarEstudiante.html'
    success_url = reverse_lazy('admision:ListarEstudiante', kwargs={'slug':'1'})
    def get_context_data(self, **kwargs):
        context = super(EstudianteUpdate, self).get_context_data(**kwargs)
        context['Titulo'] = "Editar"
        return context

class EstudianteAgregar(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'admision/estudiantes/NuevoEstudiante.html'
    success_url = reverse_lazy('admision:ListarEstudiante',kwargs={'slug':'1'})

    def get_context_data(self, **kwargs):
        context = super(EstudianteAgregar, self).get_context_data(**kwargs)
        context['Titulo'] = "Agregar"
        return context

class EstudianteEliminar(DeleteView): # Eliminar un Docente
    model = Persona
    template_name = 'admision/estudiantes/Eliminar.html'
    success_url = reverse_lazy('admision:ListarEstudiante', kwargs={'slug':'1'})

def CAdmisionListaEstudiante(request, id_estu):
    adm = admisione.objects.all().filter(ci=id_estu) # obtengo las admisiones de un estudiante...
    Pers = Persona.objects.get(ci=id_estu)
    ac = 0
    ne = 0
    contexto = {'admisiones':adm,'pvigentes':ac,'nvigentes':ne,'Titulo':'Admisiones', 'estu':Pers}
    return render(request,'admision/estudiantes/AdmisionesEstudiantes.html',contexto)

def cAdmisionNuevaEstudiante(request, id_estu):
    #self.object = self.get_object
    estu = Persona.objects.get(ci=id_estu)  # obtnenemos al estudainte que se genera la admision
    your_params = {
        'id_estu': estu.ci
    }
    form2 = ExpereciaForm(request.POST)
    form4 = TrasfondoForm(request.POST)
    if request.method == 'POST':  # preguntamos si es un metodo POST.
        form = admisioneForm(request.POST)  # Instaciomos el  formulario Admisiones
        if form.is_valid():
            admisionEs = form.save(commit=False)
            admisionEs.ci = estu
            admisionEs.id_ex = form2.save()
            admisionEs.id_tra = form4.save()  # GUARDO EL TRANSFONDO ECLESIASTICO PARA PASAR SU ID.
            admisionEs.save()
            form.save_m2m()  # PERMITE GUARDAR CAMPO MANY TO MANY.
        return redirect(reverse('admision:ListaAdmisionesEstudiante', kwargs=your_params))  ## RETROCEDER UNA LISTA CON PARAMETROS
    else:
        form = admisioneForm()
        form2 = ExpereciaForm()
    contexto = {'form': form,'form2': form2,'form4': form4,'doc': estu, 'Titulo': 'Admision Nueva'}
    return render(request, 'admision/estudiantes/Nueva_Admision.html', contexto)


class EstudianteEstudiosList(ListView):
    model = Persona
    template_name = 'admision/estudiantes/estudiante.html'

    def get_context_data(self, **kwargs):
        docente = Persona.objects.all().filter(tipo="Estudiante")
        ac = 0
        ne = 0
        for i in docente:
            if (i.estado == "Activo"):
                ac = ac + 1
            else:
                ne = ne + 1
        context = super(EstudianteList, self).get_context_data(**kwargs)
        context['ActivosD'] = ac
        context['InactivosD'] = ne
        context['Titulo'] = "LISTADO DE ESTUDIANTES"
        return context

    def get_queryset(self):  # intervenimos en el metodo QUERY SET
        queryset = super(EstudianteList, self).get_queryset()
        factorb = self.kwargs.get('slug', None)
        EstadoBus = None
        if (factorb == '1'):
            EstadoBus = "Activo"
        else:
            EstadoBus = "Inactivo"
        return queryset.filter(tipo="Estudiante", estado=EstadoBus)  # Filtro para Listar solo los Estudiantes.


# AREA COMUN PARA DATOS DE INSTRUCTRES Y DOCENTES
def cAgregarDatosEstudiosRealizados(request, id_persona):
    estudiosRealizado = estudios_realizado.objects.all().filter(ci=id_persona)  # estudios realizados de una persona
    persona = Persona.objects.get(ci=id_persona)
    mensaje = "OK"
    if request.method == 'POST':
        form = estudiosForm(request.POST)
        if form.is_valid():
            if form.save() == True:
                mensaje = "Exitoso"
            else:
                mensaje = "Error al Guardar datos"

        if persona.tipo == "Estudiante":
            return redirect('admision:ListarEstudiante',1)
        else:
            return redirect('admision:ListarDocente')
    else:
        form = estudiosForm()
    contexto = {'form': form, 'Estudios': estudiosRealizado, 'mensaje': mensaje,'persona':persona}
    return render(request, 'admision/comun/Agregar_Estudios.html', contexto)
