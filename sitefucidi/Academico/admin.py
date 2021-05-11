from django.contrib import admin
from .models import Programa,Materia
# Register your models here.


@admin.register(Programa)
class cprograma(admin.ModelAdmin):
    list_display = ("cod_programa","nombre_programa","duracion","tipo_programa", "vigencia")
    search_fields = ('nombre_programa',)

@admin.register(Materia)
class cmateria(admin.ModelAdmin):


    list_display = ("cod_programa","nombre_materia","modalidad","duracion", "estado")
    search_fields = ('nombre_materia',)
