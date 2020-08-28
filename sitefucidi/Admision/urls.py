from django.urls import path
from .views import CAdmisionLista, AdmisionCreate

urlpatterns = [
    path('admision/',CAdmisionLista,name='Listar' ),
    path('nueva/',AdmisionCreate.as_view(),name ='Nueva'),

    #path('nuevo_programa/',CprograNuevo,name='Nuevo' ),
    #path('editar/(?P<id_programa>\d+)/',CprogramaEditar,name='Editar'),
    #path('eliminar/(?P<id_programa>\d+)/',CprogramaEliminar,name='Eliminar'),

    #path('materias/',CMateriaLista,name='ListarMaterias' ),
    #path('nueva_Materia/',CMateriaNuevo,name='NuevaMateria' ),
    #path('editar_Materia/(?P<id_materia>\d+)/',CMateriaEditar,name='EditarMateria'), #Editar Materia
    #path('eliminar_Materia/(?P<id_materia>\d+)/',CMateriaEliminar,name='EliminarMateria'), #Eliminar Materia
]