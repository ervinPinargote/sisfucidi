from django.contrib import admin
from .models import Matricula

# Register your models here.
@admin.register(Matricula)
class cMatricula(admin.ModelAdmin):
    list_display = ('cod_matricula',)
#    fields = (('cod_matricula','cod_programa'),"ci","fecha_matricula","nivel","modalidad")
#    search_fields = ('cod_matricula',)
#    raw_id_fields = ('ci',)
#@admin.register(Matricula_Pago)
#class cMatricula_Pago(admin.ModelAdmin):
 #   list_display = ("id", "id_matricula")
