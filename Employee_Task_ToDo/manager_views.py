from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q

from .decorators import manager_required
from .models import Task
from .manager_forms import TaskForm


@manager_required
def manager_dashboard(request):
    """
    The dashboard IS the task list: stat cards on top, then every task
    (with assigned employee + status) below, filterable by employee/status.
    """
    all_tasks = Task.objects.all()

    tasks = Task.objects.select_related('assigned_to', 'assigned_by').all().order_by('-created_at')

    status = request.GET.get('status')
    employee_id = request.GET.get('employee')
    search = request.GET.get('q')

    if status in ('pending', 'completed'):
        tasks = tasks.filter(status=status)
    if employee_id:
        tasks = tasks.filter(assigned_to_id=employee_id)
    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))

    employees = User.objects.filter(profile__role='employee').order_by('username')

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
            return redirect('manager_dashboard')
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
            return redirect('manager_dashboard')
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
        return redirect('manager_dashboard')
    return render(request, 'manager/task_confirm_delete.html', {'task': task})


@manager_required
def employee_list(request):
    employees = User.objects.filter(profile__role='employee').annotate(
        total_tasks=Count('tasks_assigned'),
        pending_tasks=Count('tasks_assigned', filter=Q(tasks_assigned__status='pending')),
        completed_tasks=Count('tasks_assigned', filter=Q(tasks_assigned__status='completed')),
    ).order_by('username')
    return render(request, 'manager/employee_list.html', {'employees': employees})