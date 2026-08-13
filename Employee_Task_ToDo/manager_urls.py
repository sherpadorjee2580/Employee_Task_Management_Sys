from django.urls import path
from . import manager_views as views

urlpatterns = [
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/tasks/create/', views.task_create, name='manager_task_create'),
    path('manager/tasks/<int:pk>/', views.task_detail, name='manager_task_detail'),
    path('manager/tasks/<int:pk>/edit/', views.task_update, name='manager_task_update'),
    path('manager/tasks/<int:pk>/delete/', views.task_delete, name='manager_task_delete'),
    path('manager/employees/', views.employee_list, name='manager_employee_list'),
]