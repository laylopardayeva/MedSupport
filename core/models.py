from django.db import models

class ChatMessage(models.Model):
    role = models.CharField(max_length=20, default="user")  # user | assistant
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.text[:30]}"
