from django.urls import path
from .views import (
    login_view,
    logout_view,
    manager_dashboard,
    employee_dashboard,
)

urlpatterns = [
    path("login/", login_view, name="login"),
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