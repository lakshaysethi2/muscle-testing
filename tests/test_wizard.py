"""Tests for the guided muscle testing wizard."""

import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User
from apps.calibrations.models import Calibration


@pytest.mark.django_db
class TestWizardFlow:
    """Test the full wizard flow end-to-end."""

    def _get_step(self, client, expected_text):
        """Navigate to /test/ and verify the expected step text is present."""
        response = client.get(reverse("start_testing"))
        assert response.status_code == 200
        content = response.content.decode()
        assert expected_text in content
        return content

    def _post_step(self, client, data=None):
        """POST to /test/ and follow the redirect."""
        return client.post(reverse("start_testing"), data or {})

    def test_step1_prepare_loads(self):
        """Step 1 shows preparation checklist."""
        client = Client()
        content = self._get_step(client, "Before You Begin")
        assert "Hydration" in content
        assert "Emotional Neutrality" in content
        assert "Centering Exercise" in content

    def test_step2_method_selection(self):
        """Step 2 shows method selection with instructions."""
        client = Client()
        self._post_step(client)  # advance from prepare
        content = self._get_step(client, "Choose Your Testing Method")
        assert "O-Ring" in content
        assert "Finger-over-Finger" in content
        assert "Sway" in content

    def test_step3_test_form(self):
        """Step 3 shows the test entry form."""
        client = Client()
        self._post_step(client)  # prepare → method
        self._post_step(client, {"method": "sway"})  # method → test
        content = self._get_step(client, "Perform Your Test")
        assert "subject" in content.lower()

    def test_full_flow_creates_calibration(self):
        """Complete wizard flow saves a Calibration."""
        client = Client()
        self._post_step(client)  # prepare → method
        self._post_step(client, {"method": "finger_over_finger"})  # method → test
        self._post_step(
            client,
            {
                "subject": "Green smoothie benefits me",
                "result": "strong",
                "calibration_level": "480",
                "visibility": "public",
                "notes": "Tested in morning",
            },
        )  # test → result

        content = self._get_step(client, "Green smoothie benefits me")
        assert "Strong" in content
        assert "480" in content

        cal = Calibration.objects.first()
        assert cal.subject == "Green smoothie benefits me"
        assert cal.result == "strong"
        assert cal.calibration_level == 480
        assert cal.method == "finger_over_finger"
        assert cal.visibility == Calibration.Visibility.PUBLIC
        assert cal.notes == "Tested in morning"

    def test_wizard_without_subject_shows_error(self):
        """Submitting test step without subject shows error."""
        client = Client()
        self._post_step(client)  # prepare → method
        self._post_step(client, {"method": "o_ring"})  # method → test

        # Post missing subject and result
        resp = client.post(reverse("start_testing"), {"subject": ""})
        assert resp.status_code == 302

        content = self._get_step(client, "Perform Your Test")
        assert "enter a subject" in content.lower()

    def test_wizard_resets_after_result(self):
        """After viewing result, clicking 'Test Another' starts fresh."""
        client = Client()
        self._post_step(client)  # prepare → method
        self._post_step(client, {"method": "o_ring"})
        self._post_step(
            client,
            {
                "subject": "First test",
                "result": "weak",
                "visibility": "private",
            },
        )

        # View result page
        content = self._get_step(client, "First test")
        assert "Weak" in content

        # POST from result page resets wizard
        self._post_step(client)
        content = self._get_step(client, "Before You Begin")
        assert "Before You Begin" in content

    def test_weak_calibration_works(self):
        """A weak calibration is saved correctly."""
        client = Client()
        self._post_step(client)
        self._post_step(client, {"method": "interlocking_o"})
        self._post_step(
            client,
            {
                "subject": "Expired supplement",
                "result": "weak",
                "calibration_level": "80",
            },
        )

        content = self._get_step(client, "Expired supplement")
        assert "Weak" in content
        assert "80" in content

        cal = Calibration.objects.first()
        assert cal.result == "weak"
        assert cal.calibration_level == 80

    def test_calibration_level_out_of_range_is_ignored(self):
        """Values outside 1-1000 are silently dropped."""
        client = Client()
        self._post_step(client)
        self._post_step(client, {"method": "o_ring"})
        self._post_step(
            client,
            {
                "subject": "X",
                "result": "strong",
                "calibration_level": "9999",
            },
        )

        cal = Calibration.objects.first()
        assert cal.calibration_level is None

    def test_authenticated_user_saved(self):
        """Calibration links to authenticated user."""
        User.objects.create_user(username="tester", email="t@x.com", password="p")
        client = Client()
        client.login(username="t@x.com", password="p")

        self._post_step(client)
        self._post_step(client, {"method": "o_ring"})
        self._post_step(client, {"subject": "Auth test", "result": "strong"})

        cal = Calibration.objects.first()
        assert cal.user is not None
        assert cal.user.email == "t@x.com"
