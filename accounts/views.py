from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from issues.models import Issue
from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("admin-portal-dashboard" if request.user.is_staff else "dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. You can now sign in.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("admin-portal-dashboard" if request.user.is_staff else "dashboard")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_short_name() or user.username}.")
            return redirect("admin-portal-dashboard" if user.is_staff else "dashboard")

        error = "The username or password is incorrect."

    return render(request, "accounts/login.html", {"error": error})


@login_required
def dashboard(request):
    resident_issues = Issue.objects.filter(user=request.user)
    pending = resident_issues.filter(status="Pending").count()
    in_progress = resident_issues.filter(status="In Progress").count()
    resolved = resident_issues.filter(status="Resolved").count()

    context = {
        "total_issues": resident_issues.count(),
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "recent_issues": resident_issues.order_by("-created_at")[:5],
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
def profile(request):
    resident_issues = Issue.objects.filter(user=request.user)
    context = {
        "total_issues": resident_issues.count(),
        "pending": resident_issues.filter(status="Pending").count(),
        "in_progress": resident_issues.filter(status="In Progress").count(),
        "resolved": resident_issues.filter(status="Resolved").count(),
    }
    return render(request, "accounts/profile.html", context)


@login_required
@require_POST
def logout_user(request):
    logout(request)
    messages.success(request, "You have signed out safely.")
    return redirect("login")
