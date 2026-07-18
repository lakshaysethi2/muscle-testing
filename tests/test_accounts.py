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
