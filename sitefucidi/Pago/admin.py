from django.contrib import admin
from .models import Pago
# Register your models here.
@admin.register(Pago)
class cPago(admin.ModelAdmin):
    list_display = ("cod_matricula","cod_pago",'descripcion','obervaciones','fecha_generacion','valor_pagar','estado')
    search_fields = ("cod_pago",)
    raw_id_fields = ('cod_matricula',)
    fields = (('cod_matricula'), "cod_pago",'descripcion','obervaciones','fecha_generacion')
    #fields = ('image_tag',)
    #readonly_fields = ('image_tag',)