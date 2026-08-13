from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, related_name='tasks_assigned', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, related_name='tasks_created', on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def mark_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} → {self.assigned_to.username} [{self.status}]"