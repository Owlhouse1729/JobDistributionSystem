from django.urls import path
from . import views

app_name = 'top'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('edit', views.Edit.as_view(), name='edit'),
    path('register', views.Register.as_view(), name='register'),
    path('update/<int:pk>', views.Update.as_view(), name='update'),
    path('delete/<int:pk>', views.Delete.as_view(), name='delete'),
]
