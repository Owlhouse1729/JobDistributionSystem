from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.views import LoginView, LogoutView
from .form import LoginForm


# Create your views here.


class Index(TemplateView):
    template_name = 'top/index.html'


class Login(LoginView):
    template_name = 'top/login.html'
    form_class = LoginForm


class Logout(LogoutView):
    template_name = 'top/logout.html'

