from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from issues.models import Issue
from notifications.models import Notification

User = get_user_model()


class ResidentIssueAccessTests(TestCase):
    def setUp(self):
        self.resident = User.objects.create_user(
            username="resident_one",
            password="Test-pass-2026!",
        )
        self.other_resident = User.objects.create_user(
            username="resident_two",
            password="Test-pass-2026!",
        )
        self.staff = User.objects.create_user(
            username="hub_staff",
            password="Test-pass-2026!",
            is_staff=True,
        )
        self.resident_issue = Issue.objects.create(
            user=self.resident,
            title="Water leak",
            description="A water leak near the community hall.",
            category="Water",
            location="Ward 17",
        )
        self.other_issue = Issue.objects.create(
            user=self.other_resident,
            title="Damaged road",
            description="A damaged road needs attention.",
            category="Roads",
            location="Ward 17",
        )

    def test_resident_only_sees_their_own_reports(self):
        self.client.force_login(self.resident)
        response = self.client.get(reverse("issue-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Water leak")
        self.assertNotContains(response, "Damaged road")

    def test_resident_cannot_open_another_residents_report(self):
        self.client.force_login(self.resident)
        response = self.client.get(
            reverse("issue-detail", args=[self.other_issue.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_staff_can_update_report_status_and_notify_resident(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("admin-update-issue-status", args=[self.resident_issue.pk]),
            {"status": "In Progress"},
        )
        self.assertRedirects(response, reverse("admin-issues"))
        self.resident_issue.refresh_from_db()
        self.assertEqual(self.resident_issue.status, "In Progress")
        self.assertTrue(
            Notification.objects.filter(
                user=self.resident,
                title="Your report status has changed",
            ).exists()
        )

    def test_resident_cannot_access_admin_workspace(self):
        self.client.force_login(self.resident)
        response = self.client.get(reverse("admin-portal-dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_logout_requires_post(self):
        self.client.force_login(self.resident)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
