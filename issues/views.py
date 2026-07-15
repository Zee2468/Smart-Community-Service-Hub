from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Issue
from .forms import IssueForm
from notifications.models import Notification
import json


def issue_list(request):

    issues = Issue.objects.all().order_by('-created_at')

    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:
        issues = issues.filter(
            title__icontains=search
        )

    if category:
        issues = issues.filter(
            category=category
        )

    total_issues = Issue.objects.count()

    pending = Issue.objects.filter(
        status="Pending"
    ).count()

    in_progress = Issue.objects.filter(
        status="In Progress"
    ).count()

    resolved = Issue.objects.filter(
        status="Resolved"
    ).count()

    context = {

        "issues": issues,

        "total_issues": total_issues,

        "pending": pending,

        "in_progress": in_progress,

        "resolved": resolved,

        "search": search,

        "category": category,

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

            return redirect(
                "issue-list"
            )

    return render(
        request,
        "issues/report_issue.html",
        {
            "form": form
        }
    )


def issue_detail(request, pk):

    issue = get_object_or_404(
        Issue,
        pk=pk
    )

    return render(
        request,
        "issues/issue_detail.html",
        {
            "issue": issue
        }
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

            return redirect(
                "issue-detail",
                pk=issue.id
            )

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

        return redirect(
            "issue-list"
        )

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