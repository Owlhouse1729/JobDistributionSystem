from django.shortcuts import render
from django.views.generic import *
from .models import MasterShift, PersonalShift


class Index(TemplateView):
    template_name = 'shift/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        master = MasterShift.objects.all().first()
        personal = PersonalShift.objects.filter(master=master).filter(is_wanted=True)
        context['master_shift'] = master
        context['personal_shifts'] = personal
        return context


class Employer(TemplateView):
    template_name = 'shift/employer.html'


class Employee(TemplateView):
    template_name = "shift/employee.html"

