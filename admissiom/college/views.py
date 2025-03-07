from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, "Registration successful. Welcome!")
            return redirect("http://127.0.0.1:8000/college/dashboard/")  # Corrected redirect
    else:
        form = RegisterForm()
    
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":  # Simplified condition
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        next_url = request.GET.get("next", "dashboard")  # Default redirect to dashboard

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("http://127.0.0.1:8000/college/dashboard/")  # Redirect to intended page or dashboard
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


@login_required
def dashboard(request):
    return render(request, 'college/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect("http://127.0.0.1:8000/college/")  # Redirect to login after logout
