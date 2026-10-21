from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="admin-portal-dashboard"),
    path("users/", views.users, name="admin-users"),
    path("issues/", views.issues, name="admin-issues"),
    path("issues/<int:pk>/status/", views.update_issue_status, name="admin-update-issue-status"),
    path("events/", views.events, name="admin-events"),
    path("opportunities/", views.opportunities, name="admin-opportunities"),
    path("notifications/", views.notifications, name="admin-notifications"),
    path("reports/", views.reports, name="admin-reports"),
    path("settings/", views.settings, name="admin-settings"),
]
