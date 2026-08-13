from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.employee_dashboard, name='home'),
    path('dashboard/', views.employee_dashboard, name='dashboard'),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='employee_side/Login.html'), name='login'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/in-progress/', views.mark_task_in_progress, name='mark_task_in_progress'),
    path('task/<int:task_id>/complete/', views.mark_task_complete, name='mark_task_complete'),
    path('history/', views.completed_tasks_history, name='history'),
]