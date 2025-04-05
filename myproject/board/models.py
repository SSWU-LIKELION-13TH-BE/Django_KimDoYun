from django.db import models
from django.conf import settings


class Post(models. Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to= 'post_images/', blank=True, null=True)
    tech_stack = models.CharField(max_length=200)
    github_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.title