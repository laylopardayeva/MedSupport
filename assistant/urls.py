from django.urls import path
from .views import assistant_page

urlpatterns = [
    path("", assistant_page, name="assistant_page"),
]