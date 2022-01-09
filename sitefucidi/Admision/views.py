import os
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse, resolve
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from xhtml2pdf import pisa

from .forms import admisioneForm, PersonaForm, ExpereciaForm, TrasfondoForm, estudiosForm, recomendacionesForm, \
    AsignacionMaterias
from .models import admisione, estudios_realizado, Persona, asignacionMaterias, Experencia_espiritual, \
    Trasfondo_eclesiastico

# Create your views here.
# funcion que permite listar las materias del programa academico
from Academico.models import Programa


@login_required
def CAdmisionLista(request):
    adm = admisione.objects.all()
    ac = 0
    ne = 0
    # n= mat.count()
    # for i in mat:
    #    if (i.estado == True):
    #        ac = ac +1
    #    else:
    #        ne=ne+1
    contexto = {'admisiones': adm, 'pvigentes': ac, 'nvigentes': ne}
    return render(request, 'admision/admision.html', contexto)


class AdmisionCreate(CreateView):
    model = admisione
    template_name = 'admision/nuevo_form.html'
    form_class = admisioneForm  # primer Formulario Principal.
    second_form_class = PersonaForm  # Formulario Persona.
    third_form_class = ExpereciaForm  # formulario de Experiecia de Espiritual.
    four_form_class = TrasfondoForm  # formulario de Transfondo.
    five_form_class = estudiosForm  # formularios de Estudios.
    six_form_class = recomendacionesForm  # formulario de recomendaciones.
    success_url = reverse_lazy('admision:Listar')

    def get_context_data(self, **kwargs):  # se añaden al contexto los siguientes formularios en orden.
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
        form = self.form_class(request.POST)  # FORMULARIO SOLICITUD
        form2 = self.second_form_class(request.POST)  # FORMULARIO PERSONA
        form3 = self.third_form_class(request.POST)  # FORMULARIO EXPERIENCIA ESPIRITUAL
        form4 = self.four_form_class(request.POST)  # FORMULARIO TRANSFONDO ECLESIASTICO
        form5 = self.five_form_class(request.POST)  # FORMULARIO ESTUDIOS REALIZADOS
        form6 = self.six_form_class(request.POST)  # FORMULARIO RECOMENDACIONES.
        if form.is_valid() and form2.is_valid():
            pers = form2.save(commit=False)
            estud = form5.save(commit=False)
            solicitud = form.save(commit=False)

            solicitud.ci = form2.save()  # GUARDO PRIMERO EL FORMULARIO PERSONA Y ASIGNO EL ID DE CEDULA AL FORMULARIO SOLICITUD
            solicitud.id_ex = form3.save()  # GUARDO PRIMERO LA EXPERIENCIA ESPIRIRTUAL Y ASIGONO SU ID.
            solicitud.id_tra = form4.save()  # GUARDO EL TRANSFONDO ECLESIASTICO PARA PASAR SU ID.
            # PROCESO PARA GUARDAR ESTUDIOS REALIZADOS

            estudios = estudios_realizado.objects.create(tipo_est=estud.tipo_est, fecha_ini=estud.fecha_ini,
                                                         fecha_fin=estud.fecha_fin, institucion=estud.institucion,
                                                         graduacion=estud.graduacion,
                                                         ci=pers)  # creamos el obejeto estudios 2.
            # solicitud.id_estudios.add(estudios)
            solicitud.save()  # aki se guarda la solicitud.
            solicitud.id_estudios.add(
                estudios)  # permite guardar una instancia del modelo  Formularios de Estudio al modelo ADMISION MANYTOMANY.
            form.save_m2m()  # PERMITE GUARDAR CAMPO MANY TO MANY.

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6))


class DocenteList(LoginRequiredMixin, ListView):
    model = Persona
    template_name = 'admision/Instructor/instructor.html'

    def get_context_data(self, **kwargs):
        docente = Persona.objects.all().filter(tipo="Instructor")
        ac = 0
        ne = 0
        for i in docente:
            if (i.estado == "Activo"):
                ac = ac + 1
            else:
                ne = ne + 1
        context = super(DocenteList, self).get_context_data(**kwargs)
        context['ActivosD'] = ac
        context['InactivosD'] = ne
        context['Titulo'] = "LISTADO DE INSTRUCTORES"
        return context

    def get_queryset(self):  # intervenimos en el metodo QUERY SET
        queryset = super(DocenteList, self).get_queryset()
        return queryset.filter(tipo="Instructor")  # Filtro para Listar solo los Instructores


class DocenteUpdate(UpdateView):
    model = Persona
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


class DocenteEliminar(DeleteView):  # Eliminar un Docente
    model = Persona
    template_name = 'admision/Instructor/eliminar.html'
    success_url = reverse_lazy('admision:ListarDocente')


@login_required
def CMateriasAsignadasDocente(request, id_docente):  # USO UNA FUNCION POR QUE PERMITE AGREGAR AGURMENTOS
    materias = asignacionMaterias.objects.all().filter(instructor=id_docente)
    doc = Persona.objects.all().filter(
        ci=id_docente)  # envio al Docente para accerder A sus Atributos u poder realizazr una nueva
    for i in doc:
        doc = i
    contexto = {'materiasAsig': materias, 'TituloFuncionalidad': "Materias Asignadas", 'Docente': doc}
    return render(request, 'admision/Instructor/Listado_materias_asignadas.html',
                  contexto)  # Usamos el mismo Formulario para un nuevo Programa


@login_required
def CMateriasAsignarRegitro(request, id_docente):
    doc = Persona.objects.get(ci=id_docente)
    your_params = {
        'id_docente': id_docente
    }
    if request.method == 'POST':  # preguntamos si es un metodo POST.
        form = AsignacionMaterias(request.POST)  # Instaciomos el  formulario creado
        if form.is_valid():
            form.save()
        return redirect(
            reverse('admision:ListaMateriasDocente', kwargs=your_params))  ## RETROCEDER UNA LISTA CON PARAMETROS
    else:
        form = AsignacionMaterias()
    contexto = {'form': form, 'doc': doc, 'Titulo': 'Asignar Materias'}
    return render(request, 'admision/Instructor/Asignar_materias.html', contexto)


@login_required
def CMateriasAsignadasUpdate(request, pk):
    asignado = asignacionMaterias.objects.get(id=pk)  # comparacion donde se verifica el Id que vamos a editar.
    docente = asignado.instructor  # Accemos al objeto instructor que contiene los datos de la persona.
    your_params = {
        'id_docente': asignado.instructor.ci
    }
    if (request.method == 'GET'):
        form = AsignacionMaterias(
            instance=asignado)  # Se puede crear un nuevo formulario para bloquear campos que sean no editables.
    else:
        form = AsignacionMaterias(request.POST, instance=asignado)
        if form.is_valid():
            form.save()
        return redirect(reverse('admision:ListaMateriasDocente',
                                kwargs=your_params))  # Redirijo a la Listar que es Principal en el funcionalidad
    contexto = {'form': form, 'doc': docente, 'Titulo': 'Actualizar Materias'}
    return render(request, 'admision/Instructor/Asignar_materias.html', contexto)


class EstudianteList(LoginRequiredMixin, ListView):
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


class EstudianteUpdate(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'admision/estudiantes/EditarEstudiante.html'
    success_url = reverse_lazy('admision:ListarEstudiante', kwargs={'slug': '1'})

    def get_context_data(self, **kwargs):
        context = super(EstudianteUpdate, self).get_context_data(**kwargs)
        context['Titulo'] = "Editar"
        return context


class EstudianteAgregar(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'admision/estudiantes/NuevoEstudiante.html'
    success_url = reverse_lazy('admision:ListarEstudiante', kwargs={'slug': '1'})

    def get_context_data(self, **kwargs):
        context = super(EstudianteAgregar, self).get_context_data(**kwargs)
        context['Titulo'] = "Agregar"
        return context


class EstudianteEliminar(DeleteView):  # Eliminar un Docente
    model = Persona
    template_name = 'admision/estudiantes/Eliminar.html'
    success_url = reverse_lazy('admision:ListarEstudiante', kwargs={'slug': '1'})


@login_required
def CAdmisionListaEstudiante(request, id_estu):
    adm = admisione.objects.all().filter(ci=id_estu)  # obtengo las admisiones de un estudiante...
    Pers = Persona.objects.get(ci=id_estu)
    ac = 0
    ne = 0
    contexto = {'admisiones': adm, 'pvigentes': ac, 'nvigentes': ne, 'Titulo': 'Admisiones', 'estu': Pers}
    return render(request, 'admision/estudiantes/AdmisionesEstudiantes.html', contexto)


@login_required
def cAdmisionNuevaEstudiante(request, id_estu):
    # self.object = self.get_object
    estu = Persona.objects.get(ci=id_estu)  # obtnenemos al estudainte que se genera la admision
    your_params = {
        'id_estu': estu.ci
    }
    # verificar si existen admisiones
    admEs = admisione.objects.all().filter(ci=id_estu)  # obtengo las admisiones de un estudiante...
    idEb = None
    idTB = None
    for i in admEs:
        idEb = i.id_ex.id
        idTB = i.id_tra.id
    exp = None
    expO = None
    trans = None
    transO = None

    if idEb is not None:
        expO = Experencia_espiritual.objects.get(id=idEb)
        exp = ExpereciaForm(instance=expO)
    else:
        exp = ExpereciaForm(request.POST)
    if idTB is not None:
        transO = Trasfondo_eclesiastico.objects.get(id=idTB)
        trans = TrasfondoForm(instance=transO)
    else:
        trans = TrasfondoForm(request.POST)
    form2 = ExpereciaForm(request.POST)
    form4 = TrasfondoForm(request.POST)
    if request.method == 'POST':  # preguntamos si es un metodo POST.
        form = admisioneForm(request.POST)  # Instaciomos el  formulario Admisiones
        if form.is_valid():
            admisionEs = form.save(commit=False)
            admisionEs.ci = estu
            if expO is not None:
                admisionEs.id_ex = expO
            else:
                admisionEs.id_ex = form2.save()

            if transO is not None:
                admisionEs.id_tra = transO
            else:
                admisionEs.id_tra = form4.save()
            # admisionEs.id_ex = form2.save()   # SE GUARDA LA EXPERIENCIA
            # admisionEs.id_tra = form4.save()  # GUARDO EL TRANSFONDO ECLESIASTICO PARA PASAR SU ID.
            admisionEs.save()
            form.save_m2m()  # PERMITE GUARDAR CAMPO MANY TO MANY.
        return redirect(
            reverse('admision:ListaAdmisionesEstudiante', kwargs=your_params))  ## RETROCEDER UNA LISTA CON PARAMETROS
    else:
        form = admisioneForm()
        form2 = ExpereciaForm()
    contexto = {'form': form, 'form2': exp, 'form4': trans, 'doc': estu, 'Titulo': 'Admision'}
    return render(request, 'admision/estudiantes/Nueva_Admision.html', contexto)


@login_required
def cAdmisionUpdateEstudiante(request, pk):
    programas = Programa.objects.all
    adm = admisione.objects.get(id=pk)
    estu = Persona.objects.get(ci=adm.ci)
    exp = Experencia_espiritual.objects.get(id=adm.id_ex.id)
    tra = Trasfondo_eclesiastico.objects.get(id=adm.id_tra.id)
    your_params = {
        'id_estu': estu.ci
    }
    if request.method == 'GET':  # preguntamos si es un metodo POST.
        form = admisioneForm(instance=adm)  # Instaciomos el  formulario Admisiones
        form2 = ExpereciaForm(instance=exp)
        form4 = TrasfondoForm(instance=tra)

    else:
        form = admisioneForm(request.POST, instance=adm)
        form2 = ExpereciaForm(request.POST, instance=exp)
        form4 = TrasfondoForm(request.POST, instance=tra)
        if form.is_valid() and form2.is_valid() and form4.is_valid():
            form.save()
            form2.save()
            form4.save()
        return redirect(
            reverse('admision:ListaAdmisionesEstudiante', kwargs=your_params))  ## RETROCEDER UNA LISTA CON PARAMETROS
    contexto = {'form': form, 'form2': form2, 'form4': form4, 'admision': adm, 'Titulo': 'Actualizar información',
                'programas': programas}
    return render(request, 'admision/estudiantes/Editar_Admision.html', contexto)


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


@login_required
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
            return redirect('admision:ListarEstudiante', 1)
        else:
            return redirect('admision:ListarDocente')
    else:
        form = estudiosForm()
    contexto = {'form': form, 'Estudios': estudiosRealizado, 'mensaje': mensaje, 'persona': persona}
    return render(request, 'admision/comun/Agregar_Estudios.html', contexto)


class EstudianteSolicitud(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'admision/solicitud/Solicitud.html'
    success_url = reverse_lazy('admision:ListarEstudiante', kwargs={'slug': '1'})

    def get_context_data(self, **kwargs):
        context = super(EstudianteSolicitud, self).get_context_data(**kwargs)
        context['Titulo'] = "Solicitud de Admision"
        return context


def editPerfil(request):
    profile = request.user.profile
    usuario = profile


#GENERAR REPORTE DE FICHA ACADEMICA

class FichaAdmisionPDF_view(LoginRequiredMixin, View):
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
        #matricula = Matricula.objects.get(pk=self.kwargs['pk'])
        admision = admisione.objects.get(pk=self.kwargs['pk']) #obtener la admission.
        estudios = estudios_realizado.objects.all().filter(ci=admision.ci.ci)
        #user = User.objects.get(
        #    username=self.request.user)  # envia el usuario que esta en la logueado en la aplicacion.
        template_path = 'admision/AdmisionFichaPDF.html'
        fecha = datetime.date.today()
        context = {'tittle': 'Solicitud de Admision: ', 'admision': admision,
                   'codigo': admision.codigoAdmision,
                   'icon': '{}{}'.format(settings.MEDIA_URL, 'logo13.png'),
                   'estudios': estudios,
                   'date': fecha
                   #'usuario': user
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + admision.codigoAdmision + ".pdf"
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


class AdmisionElimnarView(DeleteView):  # Eliminar un Docente
    model = admisione
    template_name = 'admision/EliminarAdmision.html'
    success_url = reverse_lazy('admision:ListarDocente')
    def get_context_data(self, **kwargs):
        context = super(AdmisionElimnarView, self).get_context_data(**kwargs)
        admision = admisione.objects.get(pk=self.kwargs['pk'])
        context['adm'] = admision
        return context