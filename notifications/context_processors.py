from .models import Notification


def unread_notifications(request):
    """Expose the signed-in user's unread notification count to templates."""
    if not request.user.is_authenticated:
        return {"unread_notifications": 0}

    return {
        "unread_notifications": Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).count()
    }
