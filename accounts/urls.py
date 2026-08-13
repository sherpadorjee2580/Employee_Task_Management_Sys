from django.urls import path
from .views import (
    # login_view,
    logout_view,
    manager_dashboard,
    employee_dashboard,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("logout/", logout_view, name="logout"),

    path(
        "manager/",
        manager_dashboard,
        name="manager_dashboard"
    ),

    path(
        "employee/",
        employee_dashboard,
        name="employee_dashboard"
    ),
]