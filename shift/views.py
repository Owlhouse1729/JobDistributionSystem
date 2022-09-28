from django.shortcuts import render, redirect
from django.views.generic import *
from top.models import User
from top.mixins import OnlyEmployerMixin
from .models import MasterShift, ShiftTable, PersonalShift
from .mixins import MonthWithShiftsMixin, TableGeneratorMixin


class Index(MonthWithShiftsMixin, TemplateView):
    template_name = 'shift/index2.html'
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
        calendar_context['generate_status'] = self.is_generated(self.get_current_month())

        year = self.get_current_month().year
        month = self.get_current_month().month
        if ShiftTable.objects.filter(year=year, month=month):
            table = ShiftTable.objects.get(year=year, month=month)
        else:
            table = None
        # 自分のPersonalShiftのis_wantedが全てFalseであるようなUser
        # 残骸: User.objects.filter(owner_of=PersonalShift.objects.filter(master__shift_table=table, is_wanted=True))
        non_submitted_users = []
        for user in User.objects.filter(is_employer=False):
            if table:
                if not PersonalShift.objects.filter(master__shift_table=table, owner=user, submitted=True):
                    non_submitted_users.append(user)
        calendar_context['non_submitted_users'] = non_submitted_users

        context.update(calendar_context)
        return context

    def post(self, request, *args, **kwargs):
        year = self.get_current_month().year
        month = self.get_current_month().month
        print('request', request.POST)
        if request.POST.get('generate'):
            self.generate(self.get_current_month())
        elif request.POST.get('allot'):
            self.allot(ShiftTable.objects.get(year=year, month=month))
        elif request.POST.get('confirm'):
            # 現在のシフトテーブル上で、requiredなMasterShiftのpkを取得
            master_shifts = MasterShift.objects.filter(required=True, shift_table__month=month, shift_table__year=year)
            # マスターシフトのpkについてのループ
            print('confirmed!')
            for master_shift in master_shifts:
                # confirmやcsrfトークンの除外 --> employeeのusernameが出る
                assigned = request.POST.get(str(master_shift.pk))
                if assigned:
                    if assigned != 'not_selected':
                        master_shift.worker = User.objects.get(id=int(assigned))
                        print(f'{master_shift} のシフトに {User.objects.get(id=int(assigned))} を割り当てました')
                    else:
                        master_shift.worker = None
                    master_shift.save()
        return redirect('shift:employer', year=year, month=month)


class EmployerAssign(Employer):
    template_name = 'shift/employer_assign.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        print('request', request.POST)
        year = self.get_current_month().year
        month = self.get_current_month().month
        if request.POST.get('confirm'):
            pk_list = [int(pk) for pk in request.POST.getlist('check[]')]
            master_shifts = MasterShift.objects.filter(shift_table__year=year, shift_table__month=month)
            for master_shift in master_shifts:
                if master_shift.pk in pk_list:
                    master_shift.required = True
                else:
                    master_shift.required = False
                master_shift.save()
        elif request.POST.get('generate'):
            self.generate(self.get_current_month())
            return redirect('shift:assign', year=year, month=month)
        return redirect('shift:index', year=year, month=month)


class Employee(Index):
    template_name = 'shift/employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        context.update({
            'personal_shifts': PersonalShift.objects.filter(owner=self.request.user),
            'generate_status': self.is_generated(self.get_current_month())
        })
        return context

    def post(self, request, *args, **kwargs):
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
                personal_shift.submitted = True
                personal_shift.save()
            return redirect('shift:index', year=self.get_current_month().year, month=self.get_current_month().month)
        return redirect('shift:employee', year=self.get_current_month().year, month=self.get_current_month().month)


