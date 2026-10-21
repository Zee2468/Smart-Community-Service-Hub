from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Issue
from .forms import IssueForm
from notifications.models import Notification
import json



@login_required
def issue_list(request):
    # Residents can only see their own reports.
    issues = Issue.objects.filter(
        user=request.user
    ).order_by("-created_at")

    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()

    if search:
        issues = issues.filter(title__icontains=search)

    valid_categories = {
        value for value, label in Issue.CATEGORY_CHOICES
    }

    valid_statuses = {
        value for value, label in Issue.STATUS_CHOICES
    }

    if category in valid_categories:
        issues = issues.filter(category=category)

    if status in valid_statuses:
        issues = issues.filter(status=status)

    # Statistics are calculated only for the logged-in resident.
    resident_issues = Issue.objects.filter(user=request.user)

    context = {
        "issues": issues,
        "total_issues": resident_issues.count(),
        "pending": resident_issues.filter(status="Pending").count(),
        "in_progress": resident_issues.filter(
            status="In Progress"
        ).count(),
        "resolved": resident_issues.filter(status="Resolved").count(),
        "search": search,
        "category": category,
        "status": status,
        "category_choices": Issue.CATEGORY_CHOICES,
        "status_choices": Issue.STATUS_CHOICES,
    }

    return render(
        request,
        "issues/issue_list.html",
        context
    )


@login_required
def report_issue(request):

    form = IssueForm()

    if request.method == "POST":

        form = IssueForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            issue = form.save(
                commit=False
            )

            issue.user = request.user
            issue.save()

            # Create Notification
            Notification.objects.create(

                user=request.user,

                title="Issue Submitted",

                message=f"Your issue '{issue.title}' has been submitted successfully."

            )

            messages.success(request, "Your community report has been submitted.")
            return redirect("issue-list")

    return render(
        request,
        "issues/report_issue.html",
        {
            "form": form
        }
    )



@login_required
def issue_detail(request, pk):
    issue = get_object_or_404(
        Issue,
        pk=pk,
        user=request.user
    )

    return render(
        request,
        "issues/issue_detail.html",
        {"issue": issue}
    )



@login_required
def edit_issue(request, pk):

    issue = get_object_or_404(
        Issue,
        pk=pk,
        user=request.user
    )

    form = IssueForm(
        instance=issue
    )

    if request.method == "POST":

        form = IssueForm(
            request.POST,
            request.FILES,
            instance=issue
        )

        if form.is_valid():

            form.save()

            Notification.objects.create(

                user=request.user,

                title="Issue Updated",

                message=f"Your issue '{issue.title}' has been updated."

            )

            messages.success(request, "Your report details have been updated.")
            return redirect("issue-detail", pk=issue.id)

    return render(
        request,
        "issues/edit_issue.html",
        {
            "form": form,
            "issue": issue
        }
    )


@login_required
def delete_issue(request, pk):

    issue = get_object_or_404(
        Issue,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        Notification.objects.create(

            user=request.user,

            title="Issue Deleted",

            message=f"Your issue '{issue.title}' has been deleted."

        )

        issue.delete()
        messages.success(request, "Your report has been deleted.")

        return redirect("issue-list")

    return render(
        request,
        "issues/delete_issue.html",
        {
            "issue": issue
        }
    )


@login_required
def dashboard(request):

    total_issues = Issue.objects.filter(
        user=request.user
    ).count()

    pending = Issue.objects.filter(
        user=request.user,
        status="Pending"
    ).count()

    in_progress = Issue.objects.filter(
        user=request.user,
        status="In Progress"
    ).count()

    resolved = Issue.objects.filter(
        user=request.user,
        status="Resolved"
    ).count()

    recent_issues = Issue.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    chart_labels = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    chart_data = [
        pending,
        in_progress,
        resolved
    ]

    context = {

        "total_issues": total_issues,

        "pending": pending,

        "in_progress": in_progress,

        "resolved": resolved,

        "recent_issues": recent_issues,

        "chart_labels": json.dumps(chart_labels),

        "chart_data": json.dumps(chart_data),

    }

    return render(
        request,
        "issues/dashboard.html",
        context
    )