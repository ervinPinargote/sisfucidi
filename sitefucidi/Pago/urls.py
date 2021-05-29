from django.urls import path

from .views import PagosMatriculaList, cAgregarValor, pdfPagoMatricula_view

urlpatterns = [
    path('lista/', PagosMatriculaList.as_view(), name='PagoLista'),
    path('detalle/pagos/(?P<id_pago>\d+)/$', cAgregarValor, name='PagoDetalle'),

    path('pago/matricula/pdf/(?P<pk>\d+)/',pdfPagoMatricula_view.as_view(),name='ReportePagoMatricula'),
]