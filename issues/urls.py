from django.urls import path

from .views import (
    issue_list,
    report_issue,
    issue_detail,
    edit_issue,
    delete_issue,
    dashboard,
)

urlpatterns = [

    path(
        "",
        issue_list,
        name="issue-list",
    ),

    path(
        "report/",
        report_issue,
        name="report-issue",
    ),

    path(
        "dashboard/",
        dashboard,
        name="issue-dashboard",
    ),

    path(
        "<int:pk>/",
        issue_detail,
        name="issue-detail",
    ),

    path(
        "<int:pk>/edit/",
        edit_issue,
        name="edit-issue",
    ),

    path(
        "<int:pk>/delete/",
        delete_issue,
        name="delete-issue",
    ),

]