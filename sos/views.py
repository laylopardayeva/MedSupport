from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from .models import SOSRequest

def sos_page(request):
    saved = False
    request_id = None
    eta_text = None

    if request.method == "POST":
        obj = SOSRequest.objects.create(
            patient_name=request.POST.get("patient_name", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            message=request.POST.get("message", "").strip(),
            status="open",
            # latitude/longitude stay null for now (demo)
        )

        saved = True
        request_id = obj.id
        eta_text = "5–10 minutes"

    return render(request, "sos/page.html", {
        "saved": saved,
        "request_id": request_id,
        "eta_text": eta_text,
    })
