from django.urls import path
from .views import sos_page

urlpatterns = [
    path("", sos_page, name="sos_page"),
]