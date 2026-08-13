from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Count, Q

from .decorators import manager_required
from .models import Task
from .manager_forms import TaskForm, EmployeeCreationForm


@manager_required
def manager_dashboard(request):
    """
    The dashboard IS the task list: stat cards on top, then every task
    (with assigned employee + status) below, filterable by employee/status.
    """
    all_tasks = Task.objects.all()

    tasks = Task.objects.select_related('assigned_to', 'assigned_by').all().order_by('-created_at')

    status = request.GET.get('status')
    employee_id = request.GET.get('Employee')
    search = request.GET.get('q')

    if status in ('pending', 'in_progress', 'completed'):
        tasks = tasks.filter(status=status)
    if employee_id:
        tasks = tasks.filter(assigned_to_id=employee_id)
    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))

    # ✅ Fixed: Changed 'employee' to 'Employee'
    employees = User.objects.filter(groups__name='Employee').order_by('username')

    context = {
        'total_tasks': all_tasks.count(),
        'pending_count': all_tasks.filter(status='pending').count(),
        'completed_count': all_tasks.filter(status='completed').count(),
        'employee_count': employees.count(),
        'tasks': tasks,
        'employees': employees,
        'current_status': status or '',
        'current_employee': employee_id or '',
        'search': search or '',
    }
    return render(request, 'manager/dashboard.html', context)


@manager_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'manager/task_detail.html', {'task': task})


@manager_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" assigned to {task.assigned_to.username}.')
            return redirect('/manager/')
    else:
        form = TaskForm()
    return render(request, 'manager/task_form.html', {'form': form, 'title': 'Assign New Task'})


@manager_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated.')
            return redirect('/manager/')
    else:
        form = TaskForm(instance=task)
    return render(request, 'manager/task_form.html', {'form': form, 'title': 'Edit Task', 'task': task})


@manager_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted.')
        return redirect('/manager')
    return render(request, 'manager/task_confirm_delete.html', {'task': task})


@manager_required
def employee_list(request):
    # ✅ Fixed: Changed 'employee' to 'Employee'
    employees = User.objects.filter(groups__name='Employee').annotate(
        total_tasks=Count('tasks_assigned'),
        pending_tasks=Count('tasks_assigned', filter=Q(tasks_assigned__status='pending')),
        completed_tasks=Count('tasks_assigned', filter=Q(tasks_assigned__status='completed')),
    ).order_by('username')
    return render(request, 'manager/employee_list.html', {'employees': employees})


@manager_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Automatically assign user to the 'Employee' group
            employee_group, _ = Group.objects.get_or_create(name='Employee')
            user.groups.add(employee_group)

            messages.success(request, f"Employee '{user.username}' created successfully!")
            return redirect('employee:manager_employee_list')
    else:
        form = EmployeeCreationForm()

    return render(request, 'manager/add_employee.html', {'form': form})