from django.db import models

class SOSRequest(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("dispatched", "Dispatched"),
        ("resolved", "Resolved"),
        ("canceled", "Canceled"),
    ]

    patient_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)

    # GPS location (you’ll fill this from frontend later)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    message = models.TextField(blank=True)  # optional: “I need help”
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOS {self.patient_name} ({self.status})"
