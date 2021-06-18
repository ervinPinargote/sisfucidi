from django.urls import path

from .views import PagosMatriculaList, cAgregarValor, pdfPagoMatricula_view, PagosColegiaturaList, \
    PagosColegiaturaEstudHabilList, cAgregarPago, cFichaPago, pdfEstadoPagoMatricula_view, pdfEstadoPagoMatricula_view1, \
    pdfPagoColegiatura_view

urlpatterns = [
    path('lista/', PagosMatriculaList.as_view(), name='PagoLista'),
    path('detalle/pagos/(?P<id_pago>\d+)/$', cAgregarValor, name='PagoDetalle'),

    path('pago/matricula/pdf/(?P<pk>\d+)/', pdfPagoMatricula_view.as_view(), name='ReportePagoMatricula'),

    path('reportes/(?P<pk>\d+)/', pdfEstadoPagoMatricula_view.as_view(), name='ReporteGeneralPago'),

    path('pago/matricula/pdf/reporte/pago1/', pdfEstadoPagoMatricula_view1.as_view(), name='ReporteGeneralPago1'),
    #creacion de urls para pagos de colegiatura

    path('lista_pc/', PagosColegiaturaList.as_view(), name='PagoListaColegiatura'),
    path('lista_est_pc/', PagosColegiaturaEstudHabilList.as_view(), name='PagoEstudianteHabColegiatura'),
    path('agregar/pago/(?P<id_pago>\d+)/$', cAgregarPago, name='PagoColegiatura'),
    path('ficha/pago/(?P<id_pago>\d+)/$', cFichaPago, name='FichaPagoColegiatura'),
    path('pago/colegiatura/pdf/(?P<pk>\d+)/', pdfPagoColegiatura_view.as_view(), name='ReportePagoColegiatura'),


]