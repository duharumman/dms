from django.db import models

from user.models import User, AdminUser

class Status(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    IN_PROGRESS = 'In Progress', 'In Progress'
    COMPLETED = 'Completed', 'Completed'


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    deadline = models.DateTimeField()  
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    min_users = models.IntegerField()

class Book(models.Model):
    assigned_by = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='assigned_books')
    users = models.ManyToManyField(User, related_name='books')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='books')
   

