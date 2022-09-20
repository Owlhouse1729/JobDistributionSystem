from django.urls import path
from . import views

app_name = 'shift'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<int:year>/<int:month>', views.Index.as_view(), name='index'),
    path('employer', views.Employer.as_view(), name='employer'),
    path('assign', views.EmployerAssign.as_view(), name='assign'),
    path('assign/<int:year>/<int:month>', views.EmployerAssign.as_view(), name='assign'),
    path('employer/<int:year>/<int:month>', views.Employer.as_view(), name='employer'),
    path('employee', views.Employee.as_view(), name='employee'),
    path('employee/<int:year>/<int:month>', views.Employee.as_view(), name='employee'),
]
