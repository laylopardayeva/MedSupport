from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from .models import NurseRequest

def nurse_page(request):
    saved = False
    request_id = None
    eta_text = None

    if request.method == "POST":
        # schedule automatically: now + 30 minutes (demo)
        scheduled_time = timezone.now() + timedelta(minutes=30)

        obj = NurseRequest.objects.create(
            patient_name=request.POST.get("patient_name", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            symptoms_text=request.POST.get("symptoms_text", "").strip(),
            address=request.POST.get("address", "").strip(),
            scheduled_time=scheduled_time,
            status="open",
        )

        saved = True
        request_id = obj.id
        eta_text = "20–30 minutes"

    return render(request, "nurse/page.html", {
        "saved": saved,
        "request_id": request_id,
        "eta_text": eta_text,
    })
