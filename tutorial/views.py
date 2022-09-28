from django.shortcuts import render, redirect
from django.views.generic import *
from top.models import User
from top.mixins import OnlyEmployerMixin
# Create your views here.


class Index(TemplateView):
    template_name = 'tutorial/index.html'

    def get(self, request, *args, **kwargs):
        if not User.is_employer:
            return redirect('tutorial:employee')
        return redirect('tutorial:employer')


class Employer(OnlyEmployerMixin, TemplateView):
    template_name = 'tutorial/employer.html'
    model = User


class Employee(TemplateView):
    template_name = 'tutorial/employee.html'
