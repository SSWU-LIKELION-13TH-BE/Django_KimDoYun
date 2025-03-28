from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    userid = models.CharField(max_length=15, unique=True)
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions=models.ManyToManyField(Permission, related_name="customeuser_permissions_set",blank=True)