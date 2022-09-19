import calendar
import datetime
import itertools
from collections import deque
from .models import MasterShift, PersonalShift, ShiftTable
from top.models import User


class BaseCalendarMixin:
    first_weekday = 0  # 0は月曜から、1は火曜から。6なら日曜日からになります。お望みなら、継承したビューで指定してください。
    week_names = ['月', '火', '水', '木', '金', '土', '日']  # これは、月曜日から書くことを想定します。['Mon', 'Tue'...

    def setup_calendar(self):
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names


class MonthCalendarMixin(BaseCalendarMixin):
    def get_previous_month(self, date):
        """前月を返す"""
        if date.month == 1:
            return date.replace(year=date.year - 1, month=12, day=1)
        else:
            return date.replace(month=date.month - 1, day=1)

    def get_next_month(self, date):
        """次月を返す"""
        if date.month == 12:
            return date.replace(year=date.year + 1, month=1, day=1)
        else:
            return date.replace(month=date.month + 1, day=1)

    def get_month_days(self, date):
        """その月の全ての日を返す"""
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self):
        """現在の月を返す"""
        self.setup_calendar()
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
            print('kwargsもyもmもあったので正常ッピ', month)
        else:
            month = datetime.date.today().replace(day=1)
            print("kwargsはあるけどyかmがありませんので", month)
        return month

    def get_month_calendar(self):
        """月間カレンダー情報の入った辞書を返す"""
        # self.setup_calendar()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_previous_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data


class MonthWithShiftsMixin(MonthCalendarMixin):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_month_schedules(self, start, end, days):
        # shifts = {2022-9-19:[AMのシフト, PMのシフト], 2022-9-20:[AMのシフト, PMのシフト], .... }
        shifts = {day: [MasterShift.objects.filter(date__range=(start, end)).filter(date=day.strftime('%Y-%m-%d'))] for week in days for day in week}
        size = len(shifts)
        return [{key: shifts[key] for key in itertools.islice(shifts, i, i + 7)} for i in range(0, size, 7)]

    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_context['shifts'] = self.get_month_schedules(month_first, month_last, month_days)
        return calendar_context


class TableGeneratorMixin(MonthWithShiftsMixin):
    def is_generated(self, date):
        """views.EmployerはTemplateViewより先にTableGeneratorMixinが継承されるので、
        このクラスのコードが実行されるときにはまだkwargsがなく、参照できないため、
        get_current_monthは使わず、メソッドにdate引数を設けるべし"""
        if ShiftTable.objects.filter(year=date.year).filter(month=date.month).exists():
            print('テーブルがあります')
            return True
        print('テーブルがありません')
        return False

    def generate(self, date):
        if not self.is_generated(date):
            ShiftTable.objects.create(year=date.year, month=date.month)
            generated_table = ShiftTable.objects.get(year=date.year, month=date.month)
            print(self.get_month_days(date))
            for week in self.get_month_days(date):
                print('week', week)
                for day in week:
                    print('day', day)
                    if date.month == day.month:
                        MasterShift.objects.create(shift_table=generated_table, date=day, is_am=True, required=False)
                        MasterShift.objects.create(shift_table=generated_table, date=day, is_am=False, required=True)
                        for user in User.objects.filter(is_employer=False):
                            for master in MasterShift.objects.filter(date=day):
                                PersonalShift.objects.create(master=master, owner=user)
