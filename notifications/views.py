from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    unread_count = notifications.filter(
        is_read=False
    ).count()

    context = {
        "notifications": notifications,
        "unread_count": unread_count,
    }

    return render(
        request,
        "notifications/notification_list.html",
        context
    )


@login_required
def mark_as_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect("notifications")