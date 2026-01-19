from django.urls import path
from .views import pharmacy_page

urlpatterns = [
    path("", pharmacy_page, name="pharmacy_page"),
]