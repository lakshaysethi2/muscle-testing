import os
import sys

import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User


@pytest.mark.django_db
class TestUserModel:
    """Test the custom User model."""

    def test_create_user(self):
        user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="testpass123",
        )
        assert user.username == "tester"
        assert user.email == "tester@example.com"
        assert user.testing_method == User.TestingMethod.O_RING
        assert user.karma == 0

    def test_default_testing_method(self):
        """New users default to O-ring testing method."""
        user = User.objects.create_user(username="defaults", password="testpass123")
        assert user.testing_method == User.TestingMethod.O_RING

    def test_bio_defaults_empty(self):
        user = User.objects.create_user(username="nobio", password="testpass123")
        assert user.bio == ""

    def test_display_name_uses_full_name(self):
        user = User.objects.create_user(
            username="jdoe",
            first_name="Jane",
            last_name="Doe",
            password="testpass123",
        )
        assert user.display_name == "Jane Doe"

    def test_display_name_falls_back_to_username(self):
        user = User.objects.create_user(username="anon", password="testpass123")
        assert user.display_name == "anon"

    def test_calibration_count_returns_zero(self):
        """calibration_count returns 0 before Calibration model exists."""
        user = User.objects.create_user(username="nocals", password="testpass123")
        assert user.calibration_count == 0

    def test_get_absolute_url(self):
        user = User.objects.create_user(username="profileuser", password="testpass123")
        expected = reverse("accounts:profile", kwargs={"username": "profileuser"})
        assert user.get_absolute_url() == expected

    def test_str_uses_full_name(self):
        user = User.objects.create_user(
            username="uid123",
            first_name="Alice",
            last_name="Smith",
            password="testpass123",
        )
        assert str(user) == "Alice Smith"


@pytest.mark.django_db
class TestProfileViews:
    """Test profile page views."""

    def test_profile_page_loads(self):
        User.objects.create_user(
            username="viewer",
            password="testpass123",
            bio="A test bio",
        )
        client = Client()
        response = client.get(
            reverse("accounts:profile", kwargs={"username": "viewer"})
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "viewer" in content
        assert "A test bio" in content

    def test_profile_404_for_nonexistent_user(self):
        client = Client()
        response = client.get(
            reverse("accounts:profile", kwargs={"username": "nobody"})
        )
        assert response.status_code == 404

    def test_edit_profile_requires_login(self):
        client = Client()
        response = client.get(reverse("accounts:edit_profile"))
        assert response.status_code == 302  # redirects to login

    def test_edit_profile_loads_when_logged_in(self):
        user = User.objects.create_user(username="editor", password="testpass123")
        client = Client()
        client.force_login(user)
        response = client.get(reverse("accounts:edit_profile"))
        assert response.status_code == 200
        assert "Edit Profile" in response.content.decode()

    def test_edit_profile_post_updates_fields(self):
        user = User.objects.create_user(username="updater", password="testpass123")
        client = Client()
        client.force_login(user)
        response = client.post(
            reverse("accounts:edit_profile"),
            {
                "bio": "Updated bio text",
                "testing_method": User.TestingMethod.SWAY,
            },
            follow=True,
        )
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.bio == "Updated bio text"
        assert user.testing_method == User.TestingMethod.SWAY

    def test_edit_profile_rejects_invalid_method(self):
        """Invalid testing_method value is rejected by form validation."""
        user = User.objects.create_user(username="hacker", password="testpass123")
        client = Client()
        client.force_login(user)
        response = client.post(
            reverse("accounts:edit_profile"),
            {
                "bio": "trying injection",
                "testing_method": "not-a-method",
            },
        )
        # Form is invalid — returns 200 with errors, not a redirect
        assert response.status_code == 200
        assert "not-a-method" in response.content.decode()
        user.refresh_from_db()
        # Must NOT have changed since form was invalid
        assert user.testing_method == User.TestingMethod.O_RING
        assert user.bio == ""


def test_prod_settings_require_secret_key():
    """Production settings must crash if DJANGO_SECRET_KEY is unset."""
    from django.core.exceptions import ImproperlyConfigured
    from django.core.management.utils import get_random_secret_key

    saved = os.environ.pop("DJANGO_SECRET_KEY", None)

    # Clear any cached imports of config.settings.prod
    for key in list(sys.modules):
        if "config.settings" in key:
            del sys.modules[key]

    try:
        with pytest.raises(ImproperlyConfigured):
            import config.settings.prod  # noqa: F401
    finally:
        # Restore
        if saved:
            os.environ["DJANGO_SECRET_KEY"] = saved
        else:
            os.environ["DJANGO_SECRET_KEY"] = get_random_secret_key()
        # Clean up cached modules again so other tests aren't affected
        for key in list(sys.modules):
            if "config.settings" in key:
                del sys.modules[key]
