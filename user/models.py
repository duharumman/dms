from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    USER = "USER", 'user'

class AdminUser(AbstractUser):
    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    @property
    def is_admin(self):
        return self.role == self.base_role

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class User(AdminUser):
    base_role = Role.USER

    @property
    def is_user(self):
        return self.role == self.base_role
    
    class Meta:
        proxy = True 