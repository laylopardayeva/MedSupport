from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import NurseProfile, NurseFeedback


def jobs_home(request):
    return render(request, "jobs/home.html")


def success(request):
    return render(request, "jobs/success.html")


def nurse_apply(request):
    # For demo: allow anyone (no login required)
    if request.method != "POST":
        return redirect("/")

    full_name = request.POST.get("full_name", "").strip()
    phone = request.POST.get("phone", "").strip()
    city = request.POST.get("city", "").strip()
    certification = request.POST.get("certification", "").strip()
    skills = request.POST.get("skills", "").strip()

    if not full_name or not phone or not city or not certification or not skills:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"ok": False, "message": "Please fill all fields."}, status=400)
        return redirect("/")

    # Save (no user needed for demo)
    profile = NurseProfile.objects.create(
        full_name=full_name,
        phone=phone,
        city=city,
        certification=certification,
        skills=skills,
        status="pending",
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "ok": True,
            "message": "✅ Your submission was accepted successfully. Please wait — we will contact you.",
            "id": profile.id
        })

    return redirect("/jobs/success/")


def feedback(request):
    nurses = NurseProfile.objects.filter(status="approved").order_by("full_name")

    if request.method == "POST":
        nurse_id = request.POST.get("nurse_id")
        client_name = (request.POST.get("client_name", "").strip() or "Anonymous")
        rating = int(request.POST.get("rating") or 5)
        comment = request.POST.get("comment", "").strip()

        nurse = NurseProfile.objects.filter(id=nurse_id, status="approved").first()
        if nurse:
            NurseFeedback.objects.create(
                nurse=nurse,
                client_name=client_name,
                rating=rating,
                comment=comment,
            )
            return render(request, "jobs/feedback_done.html", {"nurse": nurse})

    return render(request, "jobs/feedback.html", {"nurses": nurses})