from django.urls import path
from . import views

urlpatterns = [
    path("register_customer/", views.register_customer, name="register-customer"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
]
