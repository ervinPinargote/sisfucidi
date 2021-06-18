from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('', request.path))
    return render(request, 'usuarios/panel_usuarios.html', {})


class dashboardview(TemplateView, LoginRequiredMixin):
    login_url = '/login/'
    template_name = "usuarios/panel_usuarios.html"


def editarInformacionUsuari(request):
    profile = request.user
    id = profile.id
    username = request.POST.get("username")
    mail = request.POST.get("email1")
    nombre = request.POST.get("first_name")
    apellido = request.POST.get("last_name")
    if User.objects.filter(pk=id).update(username=username, email=mail, first_name=nombre, last_name=apellido):
        msg = "Se actualizo correctamen su informacion Personal."
        return JsonResponse({'content': {'message': msg, 'color': 'success', }})
    else:
        msg = "No se pudo actualizar correctamente su información Personal."
        return JsonResponse({'content': {'message': msg, 'color': 'danger', }})
