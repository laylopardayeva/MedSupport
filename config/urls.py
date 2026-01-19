from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("core.urls")),
    path("nurse/", include("nurse.urls")),
    path("sos/", include("sos.urls")),
    path("pharmacy/", include("pharmacy.urls")),
    path("jobs/", include("jobs.urls")),
]
