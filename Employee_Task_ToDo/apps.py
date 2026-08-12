from django.apps import AppConfig


class EmployeeTaskTodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Employee_Task_ToDo'

    def ready(self):
        import Employee_Task_ToDo.models
