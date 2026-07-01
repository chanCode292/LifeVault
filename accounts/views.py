from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def home(request):
    return redirect("login")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid username or password."

    return render(request, "login.html", {
        "error": error
    })


@login_required(login_url="login")
def dashboard(request):

    return render(request, "dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")