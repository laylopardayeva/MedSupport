from django.urls import path
from .views import nurse_page

urlpatterns = [
    path("", nurse_page, name="nurse_page"),
]