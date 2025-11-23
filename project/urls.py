from django.contrib import admin
from django.urls import path
from shop.views import home, register, login_view, success, stripe_webhook

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("success/", success, name="success"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
    path("admin/", admin.site.urls),
]
