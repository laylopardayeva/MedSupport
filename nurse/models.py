from django.db import models

class NurseRequest(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("accepted", "Accepted"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    patient_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    symptoms_text = models.TextField()
    address = models.CharField(max_length=255)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} ({self.status})"
