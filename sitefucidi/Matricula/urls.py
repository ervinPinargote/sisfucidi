from django.urls import path

from .views import MatriculasList, CAdmisionListaEstudiante

urlpatterns = [
    path('matriculas/', MatriculasList.as_view(), name='MatriculasList'),
    path('matriculas/adm/est/', CAdmisionListaEstudiante, name='ListAdm'),
]