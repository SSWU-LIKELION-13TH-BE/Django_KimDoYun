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

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

def __str__(self):
    return  f"Comment by {self.user.nickname} on {self.post.title}"
