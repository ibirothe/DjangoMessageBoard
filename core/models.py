from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    text = models.CharField(max_length=200)
    author = models.CharField(max_length=50, blank=True, default="Anonymous")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_messages")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.author or 'Anonymous'}: {self.text[:30]}"