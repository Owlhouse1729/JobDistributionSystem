from django.db import models
from top.models import User


class ShiftTable(models.Model):  # 追加
    year = models.IntegerField()
    month = models.IntegerField()


# シフト
class MasterShift(models.Model):
    shift_table = models.ForeignKey(ShiftTable, on_delete=models.CASCADE, null=True, blank=True)  # 追加
    date = models.DateField()
    is_am = models.BooleanField()
    required = models.BooleanField()
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


# 従業員の希望
class PersonalShift(models.Model):
    master = models.ForeignKey(MasterShift, on_delete=models.CASCADE)
    is_wanted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_of')

