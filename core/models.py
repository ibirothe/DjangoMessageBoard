from django.db import models

class Message(models.Model):
    text = models.CharField(max_length=200)
    author = models.CharField(max_length=50, blank=True, default="Anonymous")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author or 'Anonymous'}: {self.text[:30]}"