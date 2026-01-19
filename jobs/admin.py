from django.contrib import admin
from .models import NurseProfile, NurseFeedback

@admin.register(NurseProfile)
class NurseProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "city", "certification", "status", "created_at")
    list_filter = ("status", "city")
    search_fields = ("full_name", "phone", "city", "certification", "skills")

@admin.register(NurseFeedback)
class NurseFeedbackAdmin(admin.ModelAdmin):
    list_display = ("nurse", "rating", "client_name", "created_at")
    list_filter = ("rating",)
    search_fields = ("nurse__full_name", "client_name", "comment")
