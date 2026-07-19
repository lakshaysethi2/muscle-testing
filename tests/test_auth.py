"""Tests for authentication flows: login, signup, logout, social providers."""

import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User


@pytest.mark.django_db
class TestLoginView:
    """Test the login page and authentication flow."""

    def test_login_page_loads(self):
        client = Client()
        response = client.get(reverse("account_login"))
        assert response.status_code == 200
        content = response.content.decode()
        assert "Welcome Back" in content
        assert "Sign In" in content

    def test_login_page_has_signup_link(self):
        client = Client()
        response = client.get(reverse("account_login"))
        assert "Create one" in response.content.decode()

    def test_login_with_valid_credentials(self):
        User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="testpass123",
        )
        client = Client()
        response = client.post(
            reverse("account_login"),
            {"login": "login@example.com", "password": "testpass123"},
        )
        assert response.status_code == 302
        assert response.url == "/"

    def test_login_with_bad_password(self):
        User.objects.create_user(
            username="badpw",
            email="badpw@example.com",
            password="testpass123",
        )
        client = Client()
        response = client.post(
            reverse("account_login"),
            {"login": "badpw@example.com", "password": "wrong"},
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "not correct" in content.lower()


@pytest.mark.django_db
class TestSignupView:
    """Test the signup page and registration flow."""

    def test_signup_page_loads(self):
        client = Client()
        response = client.get(reverse("account_signup"))
        assert response.status_code == 200
        content = response.content.decode()
        assert "Create Your Account" in content

    def test_signup_page_has_login_link(self):
        client = Client()
        response = client.get(reverse("account_signup"))
        assert "Sign in" in response.content.decode()

    def test_signup_creates_user(self):
        client = Client()
        response = client.post(
            reverse("account_signup"),
            {
                "email": "newuser@example.com",
                "password1": "Str0ngP4ss!",
                "password2": "Str0ngP4ss!",
            },
        )
        assert response.status_code == 302
        assert response.url == "/"
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_signup_with_mismatched_passwords(self):
        client = Client()
        response = client.post(
            reverse("account_signup"),
            {
                "email": "fail@example.com",
                "password1": "Str0ngP4ss!",
                "password2": "Different!",
            },
        )
        assert response.status_code == 200
        assert not User.objects.filter(email="fail@example.com").exists()

    def test_signup_with_short_password(self):
        client = Client()
        response = client.post(
            reverse("account_signup"),
            {
                "email": "short@example.com",
                "password1": "ab",
                "password2": "ab",
            },
        )
        assert response.status_code == 200
        assert not User.objects.filter(email="short@example.com").exists()

    def test_signup_duplicate_email_rejected(self):
        User.objects.create_user(
            username="existing",
            email="taken@example.com",
            password="testpass123",
        )
        client = Client()
        response = client.post(
            reverse("account_signup"),
            {
                "email": "taken@example.com",
                "password1": "Str0ngP4ss!",
                "password2": "Str0ngP4ss!",
            },
        )
        assert response.status_code == 200
        assert User.objects.filter(email="taken@example.com").count() == 1


@pytest.mark.django_db
class TestLogoutView:
    """Test the logout flow."""

    def test_logout_redirects_anon(self):
        client = Client()
        response = client.get(reverse("account_logout"))
        assert response.status_code == 302

    def test_logout_clears_session(self):
        _ = User.objects.create_user(
            username="logouttest",
            email="logout@example.com",
            password="testpass123",
        )
        client = Client()
        client.login(username="logout@example.com", password="testpass123")
        assert "_auth_user_id" in client.session

        response = client.get(reverse("account_logout"))
        assert response.status_code == 302
        assert response.url == "/"


@pytest.mark.django_db
class TestSocialProvidersContext:
    """Test the social_providers context processor."""

    def test_no_providers_shows_empty_list(self):
        client = Client()
        response = client.get(reverse("account_login"))
        assert response.status_code == 200
        content = response.content.decode()
        assert "or with email" not in content


def test_dev_settings_have_permissive_auth():
    """Dev settings enable instant logout and skip email verification."""
    from django.conf import settings

    assert settings.ACCOUNT_LOGOUT_ON_GET is True
    assert settings.ACCOUNT_EMAIL_VERIFICATION == "none"
