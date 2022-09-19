from django.urls import path
from . import views

app_name = 'shift'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<int:year>/<int:month>', views.Index.as_view(), name='index'),
    path('employer', views.Employer.as_view(), name='employer'),
    path('employee', views.Employee.as_view(), name='employee'),
]
