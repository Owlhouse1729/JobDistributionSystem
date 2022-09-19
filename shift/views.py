from django.shortcuts import render, redirect
from django.views.generic import *
from top.models import User
from top.mixins import OnlyEmployerMixin
from .models import MasterShift, PersonalShift
from .mixins import MonthWithShiftsMixin, TableGeneratorMixin


class Index(MonthWithShiftsMixin, TemplateView):
    template_name = 'shift/index.html'
    model = MasterShift
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class Employer(OnlyEmployerMixin, MonthWithShiftsMixin, TableGeneratorMixin, TemplateView):
    model = User
    template_name = 'shift/employer.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        if request.POST.get('generate'):
            super().generate()
        return redirect('shift:employer')


class Employee(TemplateView):
    template_name = "shift/employee.html"

