from django.shortcuts import render
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