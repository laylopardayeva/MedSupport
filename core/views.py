from django.shortcuts import render, redirect
from .models import ChatMessage
import random


# ---------- HOME PAGE ----------
def home(request):
    return render(request, "base.html")


# ---------- AI ASSISTANT ----------
def ai_assistant(request):
    if request.method == "POST":
        user_text = request.POST.get("message", "").strip()
        if user_text:
            ChatMessage.objects.create(role="user", text=user_text)

            history = list(ChatMessage.objects.all().order_by("-created_at")[:8])
            history.reverse()

            reply = generate_ai_reply(user_text, history)
            ChatMessage.objects.create(role="assistant", text=reply)

        return redirect("/ai/")

    messages = ChatMessage.objects.all().order_by("created_at")
    return render(request, "ai/page.html", {"messages": messages})


def generate_ai_reply(user_text: str, history) -> str:
    t = user_text.lower()

    def has_any(words):
        return any(w in t for w in words)

    def pick(options):
        return random.choice(options)

    def last_user_messages(n=3):
        msgs = [m.text.lower() for m in history if m.role == "user"]
        return msgs[-n:]

    recent_users = " ".join(last_user_messages(3))

    emergency_signs = [
        "chest pain", "can't breathe", "cannot breathe", "difficulty breathing",
        "severe bleeding", "unconscious", "fainted", "stroke", "seizure",
        "blue lips", "heart attack"
    ]
    if any(s in t for s in emergency_signs):
        return (
            "This sounds serious. Use **SOS Emergency** now.\n"
            "If you can, also call your local emergency number.\n"
            "Tell me: are you alone right now?"
        )

    if has_any(["medicine", "drug", "tablet", "pill", "pharmacy", "buy", "order"]):
        return pick([
            "You can order medicine in the **Pharmacy** section. Which medicine name do you need?",
            "Use **Pharmacy** to order meds. If you don’t know the exact name, describe what it’s for.",
            "Pharmacy can deliver in the demo. Tell me the medicine name + dosage (if you know it)."
        ])

    if has_any(["nurse", "visit", "home", "injection", "iv", "drip"]):
        return pick([
            "You can request a home visit in **Call Nurse**. What symptoms do you have?",
            "Use **Call Nurse** for a visit. What’s the main problem right now?",
            "Call Nurse is best if you need help at home. What’s your address + symptoms?"
        ])

    if has_any(["sos", "emergency", "ambulance"]):
        return pick([
            "If it’s urgent, tap **SOS Emergency**. If not urgent, describe symptoms and I’ll guide you.",
            "Use **SOS Emergency** only for urgent cases. What’s happening right now?",
        ])

    if has_any(["fever", "temperature", "hot", "chills"]):
        base = pick([
            "Fever usually means your body is fighting something.",
            "A fever can come from infection, inflammation, or dehydration.",
            "Let’s treat this like a simple fever first."
        ])
        q = pick([
            "What’s your temperature (°C) if you know it?",
            "How many days has the fever been there?",
            "Any cough, sore throat, or body aches?"
        ])
        return f"{base}\n{q}\nIf it’s very high or you feel worse quickly, consider **Call Nurse**."

    if has_any(["headache", "migraine"]):
        base = pick([
            "Headaches are often dehydration + stress + lack of sleep.",
            "Most headaches are not dangerous, but we should check a few things.",
            "Let’s narrow it down."
        ])
        q = pick([
            "Is it one-sided or all over?",
            "Any vision changes or nausea?",
            "Did you drink enough water today?"
        ])
        return f"{base}\n{q}\nIf it’s sudden/worst-ever, consider **SOS**."

    if "fever" in recent_users and has_any(["yes", "no", "day", "days", "38", "39", "40"]):
        return pick([
            "Thanks. Rest + fluids is a good start. If it lasts more than 2–3 days or goes above 39°C, **Call Nurse**.",
            "Got it. Monitor temperature. If you feel worse fast or fever is high, **Call Nurse**.",
            "Okay. If you also have breathing issues or confusion, use **SOS**."
        ])

    return pick([
        "Tell me your main symptom and how long it has been happening.",
        "How long has this been happening?",
        "Describe your symptoms + your age (approx) and I’ll guide you.",
        "What is the most worrying symptom right now?"
    ])
import requests

import requests
import time

def nearby_hospitals(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    hospitals = []
    error = None

    if not lat or not lng:
        error = "Location not provided. Please allow GPS."
        return render(request, "nearby/hospitals.html", {"hospitals": hospitals, "error": error})

    # Smaller radius + limit results -> much fewer timeouts
    query = f"""
    [out:json][timeout:10];
    (
      node["amenity"="hospital"](around:3000,{lat},{lng});
      way["amenity"="hospital"](around:3000,{lat},{lng});
      relation["amenity"="hospital"](around:3000,{lat},{lng});
    );
    out center 15;
    """

    # Overpass servers (fallback)
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.openstreetmap.ru/api/interpreter",
    ]

    last_err = None

    for url in endpoints:
        for attempt in range(2):  # retry each endpoint once
            try:
                r = requests.post(
                    url,
                    data={"data": query},
                    headers={"User-Agent": "MedSupport-Demo/1.0 (student project)"},
                    timeout=15,
                )
                r.raise_for_status()
                data = r.json()

                for el in data.get("elements", []):
                    tags = el.get("tags", {})
                    name = tags.get("name", "Unnamed hospital")

                    hlat = el.get("lat") or (el.get("center") or {}).get("lat")
                    hlng = el.get("lon") or (el.get("center") or {}).get("lon")

                    if hlat and hlng:
                        hospitals.append({
                            "name": name,
                            "lat": hlat,
                            "lng": hlng,
                            "address": ", ".join(filter(None, [
                                tags.get("addr:street"),
                                tags.get("addr:housenumber"),
                                tags.get("addr:city"),
                            ])) or tags.get("operator") or "",
                        })

                if hospitals:
                    return render(request, "nearby/hospitals.html", {"hospitals": hospitals, "error": None})

                # If request succeeded but empty list, still show it (no error)
                return render(request, "nearby/hospitals.html", {"hospitals": hospitals, "error": "No hospitals found nearby (demo)."})

            except Exception as e:
                last_err = f"{url} failed: {e}"
                time.sleep(1)

    error = f"Overpass is busy right now (demo). Try again in 1–2 minutes. Last error: {last_err}"
    return render(request, "nearby/hospitals.html", {"hospitals": [], "error": error})

def static_map(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    if not lat or not lng:
        return render(request, "map/static.html", {
            "error": "Location not provided"
        })

    return render(request, "map/static.html", {
        "lat": lat,
        "lng": lng
    })