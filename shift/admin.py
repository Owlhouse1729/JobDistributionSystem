from django.contrib import admin
from .models import MasterShift, PersonalShift, ShiftTable

# Register your models here.
admin.site.register(MasterShift)
admin.site.register(PersonalShift)
admin.site.register(ShiftTable)
