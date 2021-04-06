from django.urls import path

from . import views
from .views import CAdmisionLista, AdmisionCreate, DocenteList, DocenteUpdate, CMateriasAsignadasDocente, \
    DocenteAgregar, DocenteEliminar, CMateriasAsignarRegitro, CMateriasAsignadasUpdate, EstudianteList, \
    EstudianteUpdate, EstudianteAgregar, EstudianteEliminar, CAdmisionListaEstudiante, cAdmisionNuevaEstudiante, \
    cAgregarDatosEstudiosRealizados, cAdmisionUpdateEstudiante

urlpatterns = [


    path('admision/',CAdmisionLista,name='Listar' ),
    path('nueva/',AdmisionCreate.as_view(),name ='Nueva'),


    path('docentes/',DocenteList.as_view(),name='ListarDocente'),
    path('docentes/agregar/',DocenteAgregar.as_view(),name='NuevoDocente'),
    path('docentes/editar/(?P<pk>\d+)/$',DocenteUpdate.as_view(),name="EditarDocente"),
    path('docentes/eliminar/(?P<pk>\d+)/$',DocenteEliminar.as_view(),name="EliminarDocente"),

    path('docentes/Materias/(?P<id_docente>\d+)/$',CMateriasAsignadasDocente,name="ListaMateriasDocente"),
    path('docentes/Materias/Asignar/(?P<id_docente>\d+)/$', CMateriasAsignarRegitro, name="AsignarMateriasDocente"),
    path('docentes/Materias/Editar/(?P<pk>\d+)/$', CMateriasAsignadasUpdate,name="UpdateMateriasDocente"),


    path('estudiantes/(?P<slug>\d+)/$',EstudianteList.as_view(),name='ListarEstudiante'),
    path('estudiantes/agregar/', EstudianteAgregar.as_view(), name='NuevoEstudiante'),
    path('estudiantes/editar/(?P<pk>\d+)/$',EstudianteUpdate.as_view(),name="EditarEstudiante"),
    path('estudiantes/eliminar/(?P<pk>\d+)/$',EstudianteEliminar.as_view(),name="EliminarEstudiante"),

    path('estudiantes/admisiones/(?P<id_estu>\d+)/$',CAdmisionListaEstudiante,name="ListaAdmisionesEstudiante"),
    path('estudiantes/admisiones/nueva/(?P<id_estu>\d+)/$',cAdmisionNuevaEstudiante,name="NuevaAdmisionesEstudiante"),
    path('estudiantes/admisiones/editar/(?P<pk>\d+)/$',cAdmisionUpdateEstudiante,name="EditarAdmision"),



    #AREA COMUN PARA DATOS DE ADMISION INTRUCTORES Y ESTUDIANTES.
    path('estudiosRealizados/(?P<id_persona>\d+)/$',cAgregarDatosEstudiosRealizados,name="EstudiosRealizados")


    #path('nuevo_programa/',CprograNuevo,name='Nuevo' ),
    #path('editar/(?P<id_programa>\d+)/',CprogramaEditar,name='Editar'),
    #path('eliminar/(?P<id_programa>\d+)/',CprogramaEliminar,name='Eliminar'),
    #path('materias/',CMateriaLista,name='ListarMaterias' ),
    #path('nueva_Materia/',CMateriaNuevo,name='NuevaMateria' ),
    #path('editar_Materia/(?P<id_materia>\d+)/',CMateriaEditar,name='EditarMateria'), #Editar Materia
    #path('eliminar_Materia/(?P<id_materia>\d+)/',CMateriaEliminar,name='EliminarMateria'), #Eliminar Materia
]