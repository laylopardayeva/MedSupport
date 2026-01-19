from django.urls import path
from . import views

urlpatterns = [
    path("apply/", views.nurse_apply, name="nurse_apply"),
    path("success/", views.success, name="jobs_success"),
    path("feedback/", views.feedback, name="nurse_feedback"),
]