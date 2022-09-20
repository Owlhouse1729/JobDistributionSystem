from django.shortcuts import render, redirect
from django.views.generic import *
from top.models import User
from top.mixins import OnlyEmployerMixin
from .models import MasterShift, PersonalShift, ShiftTable
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


class Employer(OnlyEmployerMixin, TableGeneratorMixin, TemplateView):
    template_name = 'shift/employer.html'
    model = User
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        context.update({
            'generate_status': self.is_generated(self.get_current_month())
        })
        return context

    """def get(self, request, *args, **kwargs):
        params = {'kwargs': {'year': 2002, 'month': 1}}
        return render(request, template_name=self.template_name, context=params)"""

    def post(self, request, *args, **kwargs):
        print('request', request.POST)
        print('kwargs', kwargs)
        if request.POST.get('generate'):
            self.generate(self.get_current_month())
        elif request.POST.get('allot'):
            self.allot(ShiftTable.objects.get(year=self.get_current_month().year,
                                              month=self.get_current_month().month))
        return redirect('shift:employer', year=self.get_current_month().year, month=self.get_current_month().month)


class Employee(TemplateView):
    template_name = "shift/employee.html"

