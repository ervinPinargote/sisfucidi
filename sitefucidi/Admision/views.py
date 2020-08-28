from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import admisioneForm, PersonaForm, ExpereciaForm, TrasfondoForm, estudiosForm, recomendacionesForm
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
        form =  self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)
        form4 = self.four_form_class(request.POST)
        form5 = self.five_form_class(request.POST)
        form6 = self.six_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)

            solicitud.ci = form2.save()
            solicitud.id_ex = form3.save()
            solicitud.id_tra = form4.save()
            solicitud.save()
            form.save_m2m()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3 = form3,form4 = form4,form5 = form5,form6 = form6 ))