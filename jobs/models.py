from django.db import models
from django.contrib.auth.models import User

class NurseProfile(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=120)

    certification = models.CharField(max_length=150, blank=True)  # ✅ NEW (demo text)
    skills = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.status})"


class NurseFeedback(models.Model):
    nurse = models.ForeignKey(NurseProfile, on_delete=models.CASCADE, related_name="feedbacks")
    client_name = models.CharField(max_length=120, default="Anonymous")
    rating = models.PositiveIntegerField(default=5)  # 1..5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nurse.full_name} ★{self.rating}"
