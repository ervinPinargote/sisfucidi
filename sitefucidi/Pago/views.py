import decimal

from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

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
    valores =detalle_pagos.objects.all().filter(pago_id = id_pago).order_by('-id')# valores que se han ingresado en la tabla de matriculas
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