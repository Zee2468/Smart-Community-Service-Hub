from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Event
from .forms import EventForm


def event_list(request):

    events = Event.objects.all().order_by("event_date")

    context = {
        "events": events,
    }

    return render(
        request,
        "events/event_list.html",
        context,
    )


@login_required
def create_event(request):

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            event = form.save(commit=False)
            event.organizer = request.user
            event.save()

            return redirect("event-list")

    else:

        form = EventForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "events/create_event.html",
        context,
    )