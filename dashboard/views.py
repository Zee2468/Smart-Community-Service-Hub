from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from issues.models import Issue
from notifications.models import Notification
from events.models import Event
from opportunities.models import Opportunity

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



@staff_member_required
def admin_dashboard(request):

    context = {

        "users": User.objects.count(),

        "issues": Issue.objects.count(),

        "events": Event.objects.count(),

        "opportunities": Opportunity.objects.count(),

        "pending": Issue.objects.filter(
            status="Pending"
        ).count(),

        "progress": Issue.objects.filter(
            status="In Progress"
        ).count(),

        "resolved": Issue.objects.filter(
            status="Resolved"
        ).count(),

        "recent_issues": Issue.objects.order_by("-created_at")[:5],

        "recent_events": Event.objects.order_by("-created_at")[:5],

    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context
    )



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