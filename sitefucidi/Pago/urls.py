from django.urls import path

from .views import PagosMatriculaList, cAgregarValor

urlpatterns = [
    path('lista/', PagosMatriculaList.as_view(), name='PagoLista'),
    path('detalle/pagos/(?P<id_pago>\d+)/$', cAgregarValor, name='PagoDetalle'),
]