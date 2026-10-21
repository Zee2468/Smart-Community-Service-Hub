from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from issues.models import Issue
from notifications.models import Notification

def home(request):

    unread_notifications = 0

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    context = {
        "total_issues": Issue.objects.count(),
        "pending": Issue.objects.filter(
            status="Pending"
        ).count(),
        "in_progress": Issue.objects.filter(
            status="In Progress"
        ).count(),
        "resolved": Issue.objects.filter(
            status="Resolved"
        ).count(),
        "unread_notifications": unread_notifications,
    }

    return render(
        request,
        "dashboard/home.html",
        context
    )



@staff_member_required(login_url="login")
def admin_dashboard(request):
    """Keep the legacy URL working while using the dedicated admin workspace."""
    return redirect("admin-portal-dashboard")


def services(request):

    return render(
        request,
        "dashboard/services.html"
    )

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # You can later save to the database
        # or send an email here.

        messages.success(
            request,
            "Thank you! Your message has been sent successfully."
        )

        return redirect("contact")

    return render(
        request,
        "dashboard/contact.html"
    )

def about(request):
    return render(request, "dashboard/about.html")