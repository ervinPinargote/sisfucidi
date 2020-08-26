from django.contrib import admin
from .models import Pago
# Register your models here.
@admin.register(Pago)
class cPago(admin.ModelAdmin):
    list_display = ("cod_matricula","estudiante","cod_pago",'Descripcion','obervaciones','valor_pagar','Valor_pagado','estado')
    search_fields = ("cod_pago",)
    raw_id_fields = ('cod_matricula','estudiante',)
    fields = (('cod_matricula', 'estudiante'), "cod_pago",'Descripcion','obervaciones',('valor_pagar','Valor_pagado'),'evidencia',('fecha_pago','estado'))
    #fields = ('image_tag',)
    #readonly_fields = ('image_tag',)