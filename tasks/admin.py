from django.contrib import admin
from .models import Task

@admin.register(Task)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at', 'deadline', 'status')