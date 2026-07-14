from django.shortcuts import render
from issues.models import Issue


def home(request):
    context = {
        'total_issues': Issue.objects.count(),
        'pending': Issue.objects.filter(status='Pending').count(),
        'in_progress': Issue.objects.filter(status='In Progress').count(),
        'resolved': Issue.objects.filter(status='Resolved').count(),
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )