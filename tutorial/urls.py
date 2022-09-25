from django.urls import path
from . import views

app_name = 'tutorial'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('employer', views.Employer.as_view(), name='employer'),
    path('employee', views.Employee.as_view(), name='employee')
]
