from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import dashboardview, editarInformacionUsuari

urlpatterns = [
    path('', dashboardview.as_view(), name='Menu'),
    path('/profile', editarInformacionUsuari, name='edit'),
]