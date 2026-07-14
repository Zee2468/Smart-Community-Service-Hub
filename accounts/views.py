from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from issues.models import Issue


def register(request):

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Redirect to profile after login
            return redirect('profile')

    return render(
        request,
        'accounts/login.html'
    )


@login_required
def profile(request):

    total_issues = Issue.objects.filter(
        user=request.user
    ).count()

    pending = Issue.objects.filter(
        user=request.user,
        status='Pending'
    ).count()

    in_progress = Issue.objects.filter(
        user=request.user,
        status='In Progress'
    ).count()

    resolved = Issue.objects.filter(
        user=request.user,
        status='Resolved'
    ).count()

    context = {
        'total_issues': total_issues,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
    }

    return render(
        request,
        'accounts/profile.html',
        context
    )


@login_required
def logout_user(request):

    logout(request)

    return redirect('login')