from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.opportunity_list,
        name="opportunity-list"
    ),

    path(
        "create/",
        views.create_opportunity,
        name="create-opportunity"
    ),

    path(
        "<int:pk>/",
        views.opportunity_detail,
        name="opportunity-detail"
    ),

    path(
        "<int:pk>/edit/",
        views.edit_opportunity,
        name="edit-opportunity"
    ),

    path(
        "<int:pk>/delete/",
        views.delete_opportunity,
        name="delete-opportunity"
    ),

]