from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Order
import stripe
import json

# Stripe secret key from settings
stripe.api_key = settings.STRIPE_SECRET_KEY


# --------------------------
# REGISTER USER
# --------------------------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "User already exists"})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("home")

    return render(request, "register.html")


# --------------------------
# LOGIN USER
# --------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# --------------------------
# HOME (Checkout Page)
# --------------------------
@login_required(login_url="login")
def home(request):

    if request.method == "POST":
        qty1 = int(request.POST.get("p1", 0))
        qty2 = int(request.POST.get("p2", 0))
        qty3 = int(request.POST.get("p3", 0))

        line_items = []
        order_total = 0

        if qty1 > 0:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Product A"},
                    "unit_amount": 1000,
                },
                "quantity": qty1,
            })
            order_total += qty1 * 10

        if qty2 > 0:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Product B"},
                    "unit_amount": 2000,
                },
                "quantity": qty2,
            })
            order_total += qty2 * 20

        if qty3 > 0:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Product C"},
                    "unit_amount": 3000,
                },
                "quantity": qty3,
            })
            order_total += qty3 * 30

        if not line_items:
            return redirect("home")

        # Create order = pending
        order = Order.objects.create(
            user=request.user,
            amount=order_total,
            status="pending"
        )

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://127.0.0.1:8000/success/",
            cancel_url="http://127.0.0.1:8000/",
            metadata={"order_id": order.id},
        )

        return redirect(session.url)

    # GET request
    orders = Order.objects.filter(user=request.user).order_by("-id")
    products = [
        {"name": "Product A", "price": 10},
        {"name": "Product B", "price": 20},
        {"name": "Product C", "price": 30},
    ]

    return render(request, "home.html", {"products": products, "orders": orders})


# --------------------------
# SUCCESS PAGE
# --------------------------
@login_required(login_url="login")
def success(request):
    return render(request, "success.html")


# --------------------------
# STRIPE WEBHOOK
# --------------------------
@csrf_exempt
def stripe_webhook(request):
    payload = request.body.decode("utf-8")
    sig_header = request.headers.get("STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session["metadata"]["order_id"]

        Order.objects.filter(id=order_id).update(status="paid")

    return HttpResponse(status=200)
