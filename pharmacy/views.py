from decimal import Decimal
from django.shortcuts import render
from .models import Pharmacy, Medicine, Order, OrderItem

def _ensure_demo_data():
    if Pharmacy.objects.exists():
        return False

    p1 = Pharmacy.objects.create(name="MedSupport Pharmacy", address="Demo street 1", phone="+998 90 000 00 00")
    p2 = Pharmacy.objects.create(name="GreenCare Pharmacy", address="Demo street 12", phone="+998 91 111 11 11")
    p3 = Pharmacy.objects.create(name="CityMed Pharmacy", address="Demo street 25", phone="+998 93 222 22 22")

    def add_meds(ph):
        Medicine.objects.create(pharmacy=ph, name="Paracetamol 500mg", price=Decimal("12000.00"), in_stock=True)
        Medicine.objects.create(pharmacy=ph, name="Ibuprofen 200mg", price=Decimal("18000.00"), in_stock=True)
        Medicine.objects.create(pharmacy=ph, name="Vitamin C", price=Decimal("15000.00"), in_stock=True)
        Medicine.objects.create(pharmacy=ph, name="Cough Syrup", price=Decimal("22000.00"), in_stock=True)

    add_meds(p1); add_meds(p2); add_meds(p3)
    return True

def pharmacy_page(request):
    no_data = _ensure_demo_data()

    pharmacies = list(Pharmacy.objects.all().order_by("name"))
    selected_pharmacy_id = pharmacies[0].id if pharmacies else None

    # Keep selected pharmacy on POST refresh (dropdown onchange)
    if request.method == "POST" and request.POST.get("pharmacy_id"):
        try:
            selected_pharmacy_id = int(request.POST.get("pharmacy_id"))
        except ValueError:
            pass

    medicines = list(Medicine.objects.filter(pharmacy_id=selected_pharmacy_id).order_by("name"))

    saved = False
    order_id = None
    eta_text = None
    total_str = None
    latitude = None
    longitude = None

    if request.method == "POST" and request.POST.get("action") == "order":
        pharmacy_id = selected_pharmacy_id
        customer_name = request.POST.get("customer_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        # Location from browser
        latitude = request.POST.get("latitude") or ""
        longitude = request.POST.get("longitude") or ""

        # If location exists, append into address (no DB changes needed)
        if latitude and longitude:
            address = f"{address} (GPS: {latitude}, {longitude})"

        selected_ids = request.POST.getlist("medicine_ids")
        selected_meds = Medicine.objects.filter(id__in=selected_ids, pharmacy_id=pharmacy_id, in_stock=True)

        delivery_fee = Decimal("0.00")
        subtotal = Decimal("0.00")

        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            address=address,
            pharmacy_id=pharmacy_id,
            delivery_fee=delivery_fee,
            total=Decimal("0.00"),
            status="new",
        )

        # Custom medicine
        custom_name = request.POST.get("custom_medicine", "").strip()
        custom_qty_raw = request.POST.get("custom_qty", "1")

        if custom_name:
            try:
                custom_qty = int(custom_qty_raw)
            except ValueError:
                custom_qty = 1
            custom_qty = max(custom_qty, 1)

            ph = Pharmacy.objects.get(id=pharmacy_id)
            custom_med, _ = Medicine.objects.get_or_create(
                pharmacy=ph,
                name=f"Custom: {custom_name}",
                defaults={"price": Decimal("0.00"), "in_stock": True},
            )

            OrderItem.objects.create(
                order=order,
                medicine=custom_med,
                qty=custom_qty,
                unit_price=Decimal("0.00"),
            )

        # Normal medicines
        for med in selected_meds:
            qty_raw = request.POST.get(f"qty_{med.id}", "1")
            try:
                qty = int(qty_raw)
            except ValueError:
                qty = 1
            qty = max(qty, 1)

            unit_price = med.price
            subtotal += unit_price * qty

            OrderItem.objects.create(
                order=order,
                medicine=med,
                qty=qty,
                unit_price=unit_price,
            )

        total = subtotal + delivery_fee
        order.total = total
        order.save(update_fields=["total"])

        saved = True
        order_id = order.id
        eta_text = "30–45 minutes"
        total_str = f"{total}"

    return render(request, "pharmacy/page.html", {
        "pharmacies": pharmacies,
        "selected_pharmacy_id": selected_pharmacy_id,
        "medicines": medicines,
        "no_data": no_data,
        "saved": saved,
        "order_id": order_id,
        "eta_text": eta_text,
        "total": total_str,
        "latitude": latitude,
        "longitude": longitude,
    })
