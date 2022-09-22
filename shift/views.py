from django.shortcuts import render, redirect
from django.views.generic import *
from top.models import User
from top.mixins import OnlyEmployerMixin
from .models import MasterShift, ShiftTable, PersonalShift
from .mixins import MonthWithShiftsMixin, TableGeneratorMixin


class Index(MonthWithShiftsMixin, TemplateView):
    template_name = 'shift/index.html'
    model = MasterShift
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        context.update({
            'user': self.request.user
        })
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
            'generate_status': self.is_generated(self.get_current_month()),
        })
        return context

    def post(self, request, *args, **kwargs):
        print('request', request.POST)
        print('kwargs', kwargs)
        if request.POST.get('generate'):
            self.generate(self.get_current_month())
        elif request.POST.get('allot'):
            self.allot(ShiftTable.objects.get(year=year, month=month))
        elif request.POST.get('confirm'):
            print('シフトの更新が行われました')
        return redirect('shift:employer', year=self.get_current_month().year, month=self.get_current_month().month)


class EmployerAssign(Employer):
    template_name = 'shift/employer_assign.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        print('request', request.POST)
        print('kwargs', kwargs)
        if request.POST.get('confirm'):
            print('employeeが必要なシフトの更新を行いました')
        return redirect('shift:assign', year=self.get_current_month().year, month=self.get_current_month().month)


class Employee(Index):
    template_name = 'shift/employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'personal_shifts': PersonalShift.objects.filter(owner=self.request.user)
        })
        return context

    def post(self, request, *args, **kwargs):
        print('request', request.POST)
        print('kwargs', kwargs)
        if request.POST.get('confirm'):
            # ログインしている人の、この月のテーブルのpersonal shift
            print([int(pk) for pk in self.request.POST.getlist('check[]')])
            for personal_shift in PersonalShift.objects.filter(owner=request.user,
                                                               master__shift_table__month=self.get_current_month().month,
                                                               master__shift_table__year=self.get_current_month().year):
                if personal_shift.pk in [int(pk) for pk in self.request.POST.getlist('check[]')]:
                    print('Trueにした:', personal_shift)
                    personal_shift.is_wanted = True
                else:
                    personal_shift.is_wanted = False
                    print('Falseにした:', personal_shift)
                personal_shift.save()
            return redirect('shift:index', year=self.get_current_month().year, month=self.get_current_month().month)
        return redirect('shift:employee', year=self.get_current_month().year, month=self.get_current_month().month)


"""class Debug(Employer):
    template_name = 'shift/debug.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'all_users': User.objects.all(),
            'selected_username': self.kwargs.get('selected_username'),
            'selected_userobject': User.objects.filter(username=self.kwargs.get('selected_username')).get(),
        })
        if PersonalShift.objects.filter(owner__username=self.kwargs.get('selected_username')):
            context.update({
                'personal_shifts': PersonalShift.objects.filter(owner__username=self.kwargs.get('selected_username'))
            })
        return context

    def post(self, request, *args, **kwargs):
        # print('request', request.POST)
        # print('kwargs', kwargs)
        selected_username = self.kwargs.get('selected_username')
        if request.POST.get('generate'):
            self.generate(self.get_current_month())
        elif request.POST.get('allot'):
            self.allot(ShiftTable.objects.get(year=self.get_current_month().year,
                                              month=self.get_current_month().month))
        elif request.POST.get('employer_confirm'):
            for personal_shift in PersonalShift.objects.filter(owner=selected_username,
                                                               master__shift_table__month=self.get_current_month().month,
                                                               master__shift_table__year=self.get_current_month().year):
                if personal_shift.pk in [int(pk) for pk in self.request.POST.getlist('check[]')]:
                    print('Trueにした:', personal_shift)
                    personal_shift.is_wanted = True
                else:
                    personal_shift.is_wanted = False
                    print('Falseにした:', personal_shift)
                personal_shift.save()
        elif request.POST.get('employee_confirm'):
            # ログインしている人の、この月のテーブルのpersonal shift
            print([int(pk) for pk in self.request.POST.getlist('check[]')])
            for personal_shift in PersonalShift.objects.filter(owner=request.user,
                                                               master__shift_table__month=self.get_current_month().month,
                                                               master__shift_table__year=self.get_current_month().year):
                if personal_shift.pk in [int(pk) for pk in self.request.POST.getlist('check[]')]:
                    print('Trueにした:', personal_shift)
                    personal_shift.is_wanted = True
                else:
                    personal_shift.is_wanted = False
                    print('Falseにした:', personal_shift)
                personal_shift.save()
        elif request.POST.get('select_user'):
            print(username for username in self.request.POST.getlist('user[]'))
            selected_username = self.request.POST.getlist('user[]')[0]
            return redirect('shift:debug', selected_username=selected_username, year=self.get_current_month().year, month=self.get_current_month().month)
        return redirect('shift:debug', selected_username=selected_username, year=self.get_current_month().year, month=self.get_current_month().month)
"""