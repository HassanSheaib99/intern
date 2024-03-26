# urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import register_employee

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register_employee, name='register_employee'),
    path('check_in/', views.check_in, name='check_in'),
    path('check_out/', views.check_out, name='check_out'),
    path('mark_off_day/', views.mark_off_day, name='mark_off_day'),
    path('update_info/', views.update_info, name='update_info'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Add this URL pattern for custom logout
]
