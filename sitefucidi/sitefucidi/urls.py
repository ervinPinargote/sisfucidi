"""sitefucidi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador/', admin.site.urls,name='login'),
    path('', LoginView.as_view(template_name='usuarios/index.html'), name="Menu"),
    path('salir/', LogoutView.as_view(template_name='usuarios/index.html'), name="logout"),
    path('Menu', include('administrador.urls')),
    path('profile/', include(('administrador.urls', 'prof'), namespace='prof'),name='prof'),
    path('academia/', include(('Academico.urls', 'academia'), namespace='academia'),name='academia'),
    path('admision/', include(('Admision.urls', 'admision'), namespace='admision'),name='admision'),# incluimos las urls de admision para generar el sistema
    path('matricula/', include(('Matricula.urls', 'matricula'), namespace='matricula'), name='matricula'), # incluimos las urls de admision para generar el sistema
    path('pagos/', include(('Pago.urls', 'pago'), namespace='pago'), name='pago'), # incluimos las urls de admision para generar el sistema

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
