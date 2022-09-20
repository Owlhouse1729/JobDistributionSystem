from django.db import models
from top.models import User


class ShiftTable(models.Model):  # 追加
    year = models.IntegerField()
    month = models.IntegerField()

    def __str__(self):
        return f'table {self.year}/{self.month}'


# シフト
class MasterShift(models.Model):
    shift_table = models.ForeignKey(ShiftTable, on_delete=models.CASCADE, null=True, blank=True)  # 追加
    date = models.DateField()
    is_am = models.BooleanField()
    required = models.BooleanField()
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.is_am:
            return f'{self.date}_AM master'
        else:
            return f'{self.date}_PM master'


# 従業員の希望
class PersonalShift(models.Model):
    master = models.ForeignKey(MasterShift, on_delete=models.CASCADE)
    is_wanted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_of')

    def __str__(self):
        if self.master.is_am:
            return f'{self.master.date}_AM of {self.owner.username}'
        else:
            return f'{self.master.date}_PM of {self.owner.username}'


class MonthlyWorker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift_number = models.IntegerField(default=0)
    table = models.ForeignKey(ShiftTable, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} of {self.month.year}/{self.month.month}'