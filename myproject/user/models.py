from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=15, unique=True)
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions=models.ManyToManyField(Permission, related_name="customeuser_permissions_set",blank=True)

class GuestBook(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guestbooks')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='written_guestbooks')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
