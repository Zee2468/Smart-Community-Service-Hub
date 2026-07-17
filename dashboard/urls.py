from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin-dashboard"
    ),

    path(
        "services/",
        views.services,
        name="services"
    ),

    path(
    "contact/",
    views.contact,
    name="contact"
),
path(
    "about/",
    views.about,
    name="about"
),

]