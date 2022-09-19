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
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        """月間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
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
        """それぞれの日とスケジュールを返す"""
        """lookup = {
            # '例えば、date__range: (1日, 31日)'を動的に作る
            '{}__range'.format(self.date_field): (start, end)
        }
        # 例えば、Schedule.objects.filter(date__range=(1日, 31日)) になる
        queryset = self.MasterShift.objects.filter(**lookup)

        # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for week in days for day in week}
        for schedule in queryset:
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)

        # day_schedules辞書を、周毎に分割する。[{1日: 1日のスケジュール...}, {8日: 8日のスケジュール...}, ...]
        # 7個ずつ取り出して分割しています。
        size = len(day_schedules)
        return [{key: day_schedules[key] for key in itertools.islice(day_schedules, i, i+7)} for i in range(0, size, 7)]
        """
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
        for week_day_shifts in (calendar_context['shifts']):
            print(week_day_shifts)
            for day, week_shift in week_day_shifts.items():
                print(' ', day)
                for shift in week_shift:
                    print('  ', shift)
                    for master_shift in shift:
                        print('    ', master_shift.worker.username)
        return calendar_context


class TableGeneratorMixin(MonthCalendarMixin):
    def is_generated(self):
        self.year = super().get_current_month().year
        self.month = super().get_current_month().month
        if ShiftTable.objects.filter(year=self.year).filter(month=self.month):
            return True
        return False

    def generate(self):
        if not self.is_generated():
            ShiftTable.objects.create(year=self.year, month=self.month)
            generated_table = ShiftTable.objects.get(year=self.year, month=self.month)
            for week in super().get_month_days(super().get_current_month()):
                for day in week:
                    MasterShift.objects.create(shift_table=generated_table, date=day, is_am=True)
                    MasterShift.objects.create(shift_table=generated_table, date=day, is_am=False)
                    for user in User.objects.filter(is_employer=False):
                        for master in MasterShift.objects.filter(date=day):
                            PersonalShift.objects.create(master=master, owner=user)



