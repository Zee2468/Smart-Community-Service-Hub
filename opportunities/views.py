from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Opportunity
from .forms import OpportunityForm


def opportunity_list(request):

    opportunities = Opportunity.objects.all().order_by("-created_at")

    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:
        opportunities = opportunities.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(location__icontains=search)
        )

    if category:
        opportunities = opportunities.filter(category=category)

    total = Opportunity.objects.count()

    jobs = Opportunity.objects.filter(
        category="Job"
    ).count()

    internships = Opportunity.objects.filter(
        category="Internship"
    ).count()

    bursaries = Opportunity.objects.filter(
        category="Bursary"
    ).count()

    learnerships = Opportunity.objects.filter(
        category="Learnership"
    ).count()

    context = {

        "opportunities": opportunities,

        "total": total,

        "jobs": jobs,

        "internships": internships,

        "bursaries": bursaries,

        "learnerships": learnerships,

        "search": search,

        "category": category,

    }

    return render(
        request,
        "opportunities/opportunity_list.html",
        context
    )


def opportunity_detail(request, pk):

    opportunity = get_object_or_404(
        Opportunity,
        pk=pk
    )

    return render(
        request,
        "opportunities/opportunity_detail.html",
        {
            "opportunity": opportunity
        }
    )


@login_required
def create_opportunity(request):

    if request.method == "POST":

        form = OpportunityForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            opportunity = form.save(commit=False)

            opportunity.user = request.user

            opportunity.save()

            return redirect("opportunity-list")

    else:

        form = OpportunityForm()

    return render(
        request,
        "opportunities/create_opportunity.html",
        {
            "form": form
        }
    )


@login_required
def edit_opportunity(request, pk):

    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        form = OpportunityForm(
            request.POST,
            request.FILES,
            instance=opportunity
        )

        if form.is_valid():

            form.save()

            return redirect(
                "opportunity-detail",
                pk=opportunity.pk
            )

    else:

        form = OpportunityForm(
            instance=opportunity
        )

    return render(
        request,
        "opportunities/edit_opportunity.html",
        {
            "form": form,
            "opportunity": opportunity
        }
    )


@login_required
def delete_opportunity(request, pk):

    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        opportunity.delete()

        return redirect("opportunity-list")

    return render(
        request,
        "opportunities/delete_opportunity.html",
        {
            "opportunity": opportunity
        }
    )