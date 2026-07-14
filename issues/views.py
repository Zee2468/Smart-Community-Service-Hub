from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Issue
from .forms import IssueForm


def issue_list(request):
    issues = Issue.objects.all().order_by('-created_at')

    search = request.GET.get('search')
    category = request.GET.get('category')

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
        status='Pending'
    ).count()

    in_progress = Issue.objects.filter(
        status='In Progress'
    ).count()

    resolved = Issue.objects.filter(
        status='Resolved'
    ).count()

    context = {
        'issues': issues,
        'total_issues': total_issues,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'search': search,
        'category': category,
    }

    return render(
        request,
        'issues/issue_list.html',
        context
    )


@login_required
def report_issue(request):

    form = IssueForm()

    if request.method == 'POST':
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

            return redirect(
                'issue-list'
            )

    context = {
        'form': form
    }

    return render(
        request,
        'issues/report_issue.html',
        context
    )


def issue_detail(request, pk):

    issue = get_object_or_404(
        Issue,
        pk=pk
    )

    context = {
        'issue': issue
    }

    return render(
        request,
        'issues/issue_detail.html',
        context
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

    if request.method == 'POST':

        form = IssueForm(
            request.POST,
            request.FILES,
            instance=issue
        )

        if form.is_valid():
            form.save()

            return redirect(
                'issue-detail',
                pk=issue.id
            )

    context = {
        'form': form,
        'issue': issue
    }

    return render(
        request,
        'issues/edit_issue.html',
        context
    )


@login_required
def delete_issue(request, pk):

    issue = get_object_or_404(
        Issue,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        issue.delete()

        return redirect(
            'issue-list'
        )

    context = {
        'issue': issue
    }

    return render(
        request,
        'issues/delete_issue.html',
        context
    )
    from django.shortcuts import render
from .models import Issue
import json


def dashboard(request):
    total_issues = Issue.objects.count()
    pending = Issue.objects.filter(status='Pending').count()
    in_progress = Issue.objects.filter(
        status='In Progress'
    ).count()
    resolved = Issue.objects.filter(
        status='Resolved'
    ).count()

    chart_labels = [
        'Pending',
        'In Progress',
        'Resolved'
    ]

    chart_data = [
        pending,
        in_progress,
        resolved
    ]

    context = {
        'total_issues': total_issues,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }

    return render(
        request,
        'issues/dashboard.html',
        context
    )