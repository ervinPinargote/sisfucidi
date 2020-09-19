from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import admisioneForm, PersonaForm, ExpereciaForm, TrasfondoForm, estudiosForm, recomendacionesForm
from .models import admisione, estudios_realizado


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