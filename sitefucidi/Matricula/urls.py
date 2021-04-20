from django.urls import path

from .views import MatriculasList, CAdmisionListaEstudiante, cMatricula, MatriculaFicha, pdfMatricula_view

urlpatterns = [
    path('matriculas/', MatriculasList.as_view(), name='MatriculasList'),
    path('matriculas/adm/est/', CAdmisionListaEstudiante, name='ListAdm'),
    path('matricula/estudiante/(?P<id_adm>\d+)/$', cMatricula, name="Matricula"),
    path('matricula/estudiante/ficha/(?P<pk>\d+)/$', MatriculaFicha.as_view(), name="MatriculaFicha"),


    # Reportes URLS

    path('matricula/pdf/(?P<pk>\d+)/',pdfMatricula_view.as_view(),name='ReporteMatricula'),
]