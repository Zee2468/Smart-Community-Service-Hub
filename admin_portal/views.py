from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):

    return render(
        request,
        "admin_portal/dashboard.html"
    )


@login_required
def users(request):

    return render(
        request,
        "admin_portal/users.html"
    )


@login_required
def issues(request):

    return render(
        request,
        "admin_portal/issues.html"
    )


@login_required
def events(request):

    return render(
        request,
        "admin_portal/events.html"
    )


@login_required
def opportunities(request):

    return render(
        request,
        "admin_portal/opportunities.html"
    )


@login_required
def notifications(request):

    return render(
        request,
        "admin_portal/notifications.html"
    )


@login_required
def reports(request):

    return render(
        request,
        "admin_portal/reports.html"
    )


@login_required
def settings(request):

    return render(
        request,
        "admin_portal/settings.html"
    )