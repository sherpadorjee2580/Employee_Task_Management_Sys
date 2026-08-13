from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Task


# ---------- EMPLOYEE SIDE ----------

@login_required
def employee_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')

    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    context = {
        'tasks': tasks,
        'total_count': Task.objects.filter(assigned_to=request.user).count(),
        'pending_count': Task.objects.filter(assigned_to=request.user, status='pending').count(),
        'in_progress_count': Task.objects.filter(assigned_to=request.user, status='in_progress').count(),
        'completed_count': Task.objects.filter(assigned_to=request.user, status='completed').count(),
    }
    return render(request, 'employee_side/dashboard.html', context)


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    return render(request, 'employee_side/task_detail.html', {'task': task})


@login_required
def mark_task_in_progress(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        task.status = 'in_progress'
        task.save()
        messages.success(request, f'Task "{task.title}" marked as In Progress.')
    return redirect('employee:task_detail', task_id=task.id)


@login_required
def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        messages.success(request, f'Task "{task.title}" marked as Completed!')
    return redirect('employee:dashboard')


@login_required
def completed_tasks_history(request):
    tasks = Task.objects.filter(
        assigned_to=request.user, status='completed'
    ).order_by('-completed_at')
    return render(request, 'employee_side/history.html', {'tasks': tasks})