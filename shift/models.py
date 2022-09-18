from django.db import models
from top.models import User


# シフト
class MasterShift(models.Model):
    date = models.DateField()
    is_am = models.BooleanField()
    required = models.BooleanField()
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


# 従業員の希望
class PersonalShift(models.Model):
    master = models.ForeignKey(MasterShift, on_delete=models.CASCADE)
    is_wanted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
