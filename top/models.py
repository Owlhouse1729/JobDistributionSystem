from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# ユーザー
class User(AbstractUser):
    is_employer = models.BooleanField(default=False)



