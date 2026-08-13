from django.urls import path
from .views import (
    # login_view,
    logout_view,
    manager_dashboard,
    employee_dashboard,
    post_login_redirect
)
from django.contrib.auth import views as auth_views

urlpatterns = [
path('login/', auth_views.LoginView.as_view(), name='login'),   # no template_name → uses default registration/login.html
path('logout/', logout_view, name='logout'),
path('post-login/', post_login_redirect, name='post_login_redirect'),
]