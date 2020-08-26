from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
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