from django.urls import path
from .views import home, ai_assistant, nearby_hospitals

urlpatterns = [
    path("", home, name="home"),
    path("ai/", ai_assistant, name="ai"),
    path("nearby/hospitals/", nearby_hospitals, name="nearby_hospitals"),
]