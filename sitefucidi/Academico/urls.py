from django.urls import path
from .views import CprograLista, CprograNuevo, CprogramaEditar, CprogramaEliminar, CMateriaLista, CMateriaNuevo, \
    CMateriaEditar, CMateriaEliminar, EliminarPrograma

urlpatterns = [
    path('listar_programa/',CprograLista,name='Listar' ),
    path('nuevo_programa/',CprograNuevo,name='Nuevo' ),
    path('editar/(?P<id_programa>\d+)/',CprogramaEditar,name='Editar'),
    path('eliminar/(?P<id_programa>\d+)/',CprogramaEliminar,name='Eliminar'),
    path('eliminar2/(?P<pk>\d+)/$',EliminarPrograma.as_view(),name='Eliminar2'),


    path('materias/',CMateriaLista,name='ListarMaterias' ),
    path('nueva_Materia/',CMateriaNuevo,name='NuevaMateria' ),
    path('editar_Materia/(?P<id_materia>\d+)/',CMateriaEditar,name='EditarMateria'), #Editar Materia
    path('eliminar_Materia/(?P<id_materia>\d+)/',CMateriaEliminar,name='EliminarMateria'), #Eliminar Materia
]