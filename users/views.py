from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterCustomerForm, ProfileForm


# register a customer
def register_customer(request):
    if request.method == "POST":
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.save()
            messages.info(
                request,
                "Your account has been sucessfully registered. Please login to continue",
            )
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong. Please check form input")
            return redirect("register-customer")
    else:
        form = RegisterCustomerForm()
        context = {"form": form}
        return render(request, "users/register_customer.html", context)


# login a user
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.info(request, "Login sucessful. Please enjoy your session")
            return redirect("dashboard")
        else:
            messages.warning(request, "Username or Password not correct")
            return redirect("login")
    else:
        return render(request, "users/login.html")


# logout a user
def logout_user(request):
    logout(request)
    messages.info(request, "Your session has ended. Please log in to continue")
    return redirect("login")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})
