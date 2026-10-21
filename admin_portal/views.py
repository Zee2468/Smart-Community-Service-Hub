from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from events.models import Event
from issues.models import Issue
from notifications.models import Notification
from opportunities.models import Opportunity

User = get_user_model()


@staff_member_required(login_url="login")
def dashboard(request):
    context = {
        "users_count": User.objects.count(),
        "issues_count": Issue.objects.count(),
        "events_count": Event.objects.count(),
        "opportunities_count": Opportunity.objects.count(),
        "pending_count": Issue.objects.filter(status="Pending").count(),
        "progress_count": Issue.objects.filter(status="In Progress").count(),
        "resolved_count": Issue.objects.filter(status="Resolved").count(),
        "recent_issues": Issue.objects.select_related("user").order_by("-created_at")[:8],
        "recent_events": Event.objects.select_related("organizer").order_by("-event_date")[:5],
    }
    return render(request, "admin_portal/dashboard.html", context)


@staff_member_required(login_url="login")
def users(request):
    search = request.GET.get("search", "").strip()
    residents = User.objects.annotate(issue_count=Count("issue")).order_by("-date_joined")
    if search:
        residents = residents.filter(
            Q(username__icontains=search) | Q(email__icontains=search)
        )
    return render(request, "admin_portal/users.html", {
        "residents": residents,
        "search": search,
    })


@staff_member_required(login_url="login")
def issues(request):
    reports = Issue.objects.select_related("user").order_by("-created_at")
    status = request.GET.get("status", "").strip()
    search = request.GET.get("search", "").strip()

    valid_statuses = {value for value, label in Issue.STATUS_CHOICES}
    if status in valid_statuses:
        reports = reports.filter(status=status)
    if search:
        reports = reports.filter(
            Q(title__icontains=search)
            | Q(location__icontains=search)
            | Q(user__username__icontains=search)
        )

    return render(request, "admin_portal/issues.html", {
        "reports": reports,
        "statuses": Issue.STATUS_CHOICES,
        "selected_status": status,
        "search": search,
    })


@staff_member_required(login_url="login")
@require_POST
def update_issue_status(request, pk):
    issue = get_object_or_404(Issue.objects.select_related("user"), pk=pk)
    new_status = request.POST.get("status", "").strip()
    valid_statuses = {value for value, label in Issue.STATUS_CHOICES}

    if new_status not in valid_statuses:
        messages.error(request, "Please choose a valid report status.")
        return redirect("admin-issues")

    if issue.status != new_status:
        old_status = issue.status
        issue.status = new_status
        issue.save(update_fields=["status"])
        Notification.objects.create(
            user=issue.user,
            title="Your report status has changed",
            message=f"The status of '{issue.title}' changed from {old_status} to {new_status}.",
        )
        messages.success(request, f"Updated “{issue.title}” to {new_status}.")
    else:
        messages.info(request, "The report already has that status.")

    return redirect("admin-issues")


@staff_member_required(login_url="login")
def events(request):
    items = Event.objects.select_related("organizer").order_by("-event_date", "-event_time")
    return render(request, "admin_portal/events.html", {"items": items})


@staff_member_required(login_url="login")
def opportunities(request):
    items = Opportunity.objects.select_related("user").order_by("-created_at")
    return render(request, "admin_portal/opportunities.html", {"items": items})


@staff_member_required(login_url="login")
def notifications(request):
    items = Notification.objects.select_related("user").order_by("-created_at")[:100]
    return render(request, "admin_portal/notifications.html", {"items": items})


@staff_member_required(login_url="login")
def reports(request):
    total = Issue.objects.count()
    category_counts = Issue.objects.values("category").annotate(total=Count("id")).order_by("-total")
    context = {
        "total": total,
        "pending": Issue.objects.filter(status="Pending").count(),
        "in_progress": Issue.objects.filter(status="In Progress").count(),
        "resolved": Issue.objects.filter(status="Resolved").count(),
        "category_counts": category_counts,
        "recent_issues": Issue.objects.select_related("user").order_by("-created_at")[:10],
    }
    return render(request, "admin_portal/reports.html", context)


@staff_member_required(login_url="login")
def settings(request):
    return render(request, "admin_portal/settings.html")
