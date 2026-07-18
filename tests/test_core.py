import pytest
from django.test import Client


@pytest.mark.django_db
def test_homepage_returns_200():
    """The landing page should load successfully."""
    client = Client()
    response = client.get("/")
    assert response.status_code == 200
    assert "KineticTruth" in response.content.decode()


@pytest.mark.django_db
def test_homepage_has_disclaimer():
    """The landing page must include the legal disclaimer."""
    client = Client()
    response = client.get("/")
    content = response.content.decode()
    assert "not medical diagnoses" in content.lower()
