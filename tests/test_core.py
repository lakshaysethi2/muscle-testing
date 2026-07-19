import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_returns_200():
    """The landing page should load successfully."""
    client = Client()
    response = client.get("/")
    assert response.status_code == 200
    assert "TruthCheck" in response.content.decode()


@pytest.mark.django_db
def test_homepage_has_disclaimer():
    """The landing page must include the legal disclaimer."""
    client = Client()
    response = client.get("/")
    content = response.content.decode()
    assert "not medical diagnoses" in content.lower()


@pytest.mark.django_db
class TestComingSoon:
    """Placeholder pages for unbuilt features."""

    def test_start_testing_now_shows_wizard(self):
        """The /test/ page is now the live wizard, not coming-soon."""
        client = Client()
        response = client.get(reverse("start_testing"))
        assert response.status_code == 200
        assert "Before You Begin" in response.content.decode()

    def test_community_db_coming_soon(self):
        client = Client()
        response = client.get(reverse("community_db"))
        assert response.status_code == 200
        assert "Coming Soon" in response.content.decode()
        assert "F-09" in response.content.decode()

    def test_practice_coming_soon(self):
        client = Client()
        response = client.get(reverse("practice"))
        assert response.status_code == 200
        assert "Coming Soon" in response.content.decode()

    def test_dashboard_coming_soon(self):
        client = Client()
        response = client.get(reverse("dashboard"))
        assert response.status_code == 200
        assert "Coming Soon" in response.content.decode()
