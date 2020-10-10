from django.contrib import admin
from .models import Persona, Requisito, Experencia_espiritual, Trasfondo_eclesiastico, estudios_realizado, \
    recomendaciones, admisione, asignacionMaterias


# Register your models here.

@admin.register(Persona)
class cPersona(admin.ModelAdmin):
    list_display = ("nombre","apellido","ciudad",'correo','tipo')
    search_fields = ('nombre','ci',)


@admin.register(Requisito)
class cRequisito(admin.ModelAdmin):
    list

@admin.register(Experencia_espiritual)
class cExperiecia(admin.ModelAdmin):
    list

@admin.register(Trasfondo_eclesiastico)
class cTransfondo(admin.ModelAdmin):
    list

@admin.register(estudios_realizado)
class cEstudios(admin.ModelAdmin):
    list

@admin.register(recomendaciones)
class cEstudios(admin.ModelAdmin):
     list

@admin.register(admisione)
class cEstudios(admin.ModelAdmin):
     list

@admin.register(asignacionMaterias)
class cAsignarMaterias(admin.ModelAdmin):
     list
