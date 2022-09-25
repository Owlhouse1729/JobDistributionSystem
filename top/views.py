from django.shortcuts import render, redirect
from django.views.generic import *
from django.contrib.auth.views import LoginView, LogoutView
from .form import LoginForm, RegisterForm
from django.urls import reverse_lazy
from .models import User
from .mixins import OnlyEmployerMixin
from shift.models import MasterShift, PersonalShift


# Create your views here.


class Index(View):
    def get(self, request):
        return redirect('shift:index')


class Login(LoginView):
    template_name = 'top/login.html'
    form_class = LoginForm


class Logout(LogoutView):
    template_name = 'top/logout.html'


class Register(CreateView):
    template_name = 'top/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        for master in MasterShift.objects.all():
            PersonalShift.objects.create(master=master, owner=user)
        return redirect('top:edit')


class Edit(OnlyEmployerMixin, TemplateView):
    model = User
    template_name = 'top/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = User.objects.filter(is_employer=False)
        context['employers'] = User.objects.filter(is_employer=True)
        return context


class Update(OnlyEmployerMixin, UpdateView):
    model = User
    template_name = 'top/update.html'
    fields = ['username', 'is_employer']
    success_url = reverse_lazy('top:edit')


class Delete(OnlyEmployerMixin, DeleteView):
    template_name = 'top/delete.html'
    model = User
    success_url = reverse_lazy('top:edit')


