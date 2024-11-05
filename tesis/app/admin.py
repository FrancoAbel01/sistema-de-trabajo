from django.contrib import admin
from .models import Task, TaskAssignment, PersonalTask

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_by', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['created_by', 'created_at']

class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'assigned_at']
    search_fields = ['user__username', 'task__title']
    list_filter = ['user', 'task', 'assigned_at']

class PersonalTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskAssignment, TaskAssignmentAdmin)
admin.site.register(PersonalTask, PersonalTaskAdmin)

