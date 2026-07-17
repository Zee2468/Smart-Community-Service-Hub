from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="admin-dashboard"
    ),

    path(
        "users/",
        views.users,
        name="admin-users"
    ),

    path(
        "issues/",
        views.issues,
        name="admin-issues"
    ),

    path(
        "events/",
        views.events,
        name="admin-events"
    ),

    path(
        "opportunities/",
        views.opportunities,
        name="admin-opportunities"
    ),

    path(
        "notifications/",
        views.notifications,
        name="admin-notifications"
    ),

    path(
        "reports/",
        views.reports,
        name="admin-reports"
    ),

    path(
        "settings/",
        views.settings,
        name="admin-settings"
    ),

]