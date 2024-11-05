

from django.contrib.auth.models import User
from django.db import models
from datetime import date, time


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    execution_date = models.DateField()  # Nuevo campo para la fecha en la que se debe realizar la tarea
    start_time = models.TimeField()  # Nuevo campo para la hora de inicio
    end_time = models.TimeField()  # Nuevo campo para la hora de fin con valor predeterminado

    def __str__(self):
        return f"{self.title} - {self.id}"

class TaskAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.task.title}"


class PersonalTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    execution_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

