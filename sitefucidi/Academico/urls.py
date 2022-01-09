from django.urls import path
from .views import CprograLista, CprograNuevo, CprogramaEditar, CprogramaEliminar, CMateriaLista, CMateriaNuevo, \
    CMateriaEditar, CMateriaEliminar, EliminarPrograma, pdfMalla_view, pdfMateria_view, cAgregarValor, \
    CestudianteNotasView, CestudianteNotasMateriasView, CeditarNotaEstudiante, pdfNotasR_view, CModalReportes, \
    CModalReportesA, pdfAprobadoReprobado_view, CProgramaNuevoModal, CprogramaEditarModal

urlpatterns = [
    path('listar_programa/', CprograLista, name='Listar'),
    path('nuevo_programa/', CprograNuevo, name='Nuevo'),
    path('nuevo_programa1/', CProgramaNuevoModal, name='Nuevo1'), # Ejecuta la Modal con Respuesta JSON
    #path('editar/(?P<id_programa>\d+)/', CprogramaEditar, name='Editar'),
    path('editar/<int:id_programa>/', CprogramaEditar, name='Editar'),
    path('editar1/<int:id_programa>/', CprogramaEditarModal, name='Editar2'),
    #path('eliminar/(?P<id_programa>\d+)/', CprogramaEliminar, name='Eliminar'),
    path('eliminar/<int:id_programa>/', CprogramaEliminar, name='Eliminar'),
    #path('eliminar2/(?P<pk>\d+)/$', EliminarPrograma.as_view(), name='Eliminar2'),

    path('materias/', CMateriaLista, name='ListarMaterias'),
    # path('nueva_Materia/(?P<cd_programa>\d+)/', CMateriaNuevo, name='NuevaMateria'),
    path('nueva_Materia/<int:cd_programa>/', CMateriaNuevo, name='NuevaMateria'),
    path('editar_Materia/(?P<id_materia>\d+)/', CMateriaEditar, name='EditarMateria'),  # Editar Materia
    # path('eliminar_Materia/(?P<id_materia>\d+)/', CMateriaEliminar, name='EliminarMateria'),  # Eliminar Materia
    path('eliminar_Materia/<str:id_materia>/', CMateriaEliminar, name='EliminarMateria'),  # Eliminar Materia
    # path('programa/(?P<cd_programa>\d+)/$', cAgregarValor, name='Valores'),
    path('programa/(<int:cd_programa>/$', cAgregarValor, name='Valores'),

    path('notas/estudiantes/lista/', CestudianteNotasView, name="NotasListaEstudiante"),
    path('notas/estudiantes/lista/materias/(?P<id_est>\d+)/', CestudianteNotasMateriasView,
         name='NotasListaEstudianteMateria'),  # Materia Estudiante Notas
    path('notas/estudiantes/editar/nota/(?P<id_nota>\d+)/', CeditarNotaEstudiante, name='NotasEditar'),
    # path('notas/reporte/estudios/(?P<pk>\d+)/',pdfREporte_view.as_view(),name='ReporteEStudios'),
    path('notas/reporte/estudios/(?P<id_per>\d+)/', CModalReportes, name='ReporteEStudios'),

    # Reportes

    path('notas/reporte/certificado/estudios/(?P<pk>\d+)/(?P<cp>\d+)/', pdfNotasR_view.as_view(),
         name='ReporteEStudios1'),
    path('notas/reporte/aprobados/estudios/(?P<pk>\d+)/(?P<cp>\d+)/', pdfAprobadoReprobado_view.as_view(),
         name='AprobadoReporteEStudios'),

    path('generar/pdf', pdfMalla_view.as_view(), name='reporte_malla'),
    # path('generar_programa/pdf/(?P<pk>\d+)/', pdfMateria_view.as_view(), name='ReportePrograma'),  # Eliminar Materia
    path('generar_programa/pdf/<int:pk>/', pdfMateria_view.as_view(), name='ReportePrograma'),  # Eliminar Materia
    #path('generar/(?P<pk>\d+)/', CModalReportesA, name='xd'),
    path('generar/<int:pk>/', CModalReportesA, name='xd'),

    # path('generar/pdf', render_pdf, name='reporte_malla'),

]
