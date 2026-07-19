"""Tests for the Calibration model, API, and views."""

import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User
from apps.calibrations.models import Calibration


@pytest.mark.django_db
class TestCalibrationModel:
    """Test the Calibration model directly."""

    def test_create_strong_calibration(self):
        user = User.objects.create_user(username="tester", password="p")
        cal = Calibration.objects.create(
            user=user,
            subject="Vitamin C",
            result=Calibration.Result.STRONG,
            calibration_level=500,
            method=User.TestingMethod.O_RING,
            category=Calibration.Category.FOOD,
            visibility=Calibration.Visibility.PUBLIC,
        )
        assert cal.result == "strong"
        assert cal.calibration_level == 500
        assert cal.is_public is True
        assert "✅" in str(cal)
        assert "Vitamin C" in str(cal)
        assert "[500]" in str(cal)

    def test_create_weak_calibration(self):
        cal = Calibration.objects.create(
            subject="Expired milk",
            result=Calibration.Result.WEAK,
        )
        assert cal.result == "weak"
        assert "❌" in str(cal)

    def test_calibration_defaults(self):
        cal = Calibration.objects.create(
            subject="Test subject",
            result=Calibration.Result.STRONG,
        )
        assert cal.user is None
        assert cal.visibility == Calibration.Visibility.PRIVATE
        assert cal.category == Calibration.Category.OTHER
        assert cal.is_removed is False
        assert cal.verification_count == 0
        assert cal.flag_count == 0
        assert cal.notes == ""

    def test_submitter_name_user(self):
        user = User.objects.create_user(
            username="jane", first_name="Jane", password="p"
        )
        cal = Calibration.objects.create(
            user=user, subject="Test", result=Calibration.Result.STRONG
        )
        assert cal.submitter_name == "Jane"

    def test_submitter_name_anonymous(self):
        cal = Calibration.objects.create(
            subject="Test", result=Calibration.Result.STRONG
        )
        assert cal.submitter_name == "Anonymous"

    def test_calibration_level_validation(self):
        from django.core.exceptions import ValidationError

        cal = Calibration(
            subject="X", result=Calibration.Result.STRONG, calibration_level=0
        )
        with pytest.raises(ValidationError):
            cal.full_clean()

        cal2 = Calibration(
            subject="Y", result=Calibration.Result.STRONG, calibration_level=1001
        )
        with pytest.raises(ValidationError):
            cal2.full_clean()

        cal3 = Calibration(
            subject="Z", result=Calibration.Result.STRONG, calibration_level=500
        )
        cal3.full_clean()  # should not raise

    def test_is_public_false_for_private(self):
        cal = Calibration.objects.create(
            subject="X",
            result=Calibration.Result.STRONG,
            visibility=Calibration.Visibility.PRIVATE,
        )
        assert cal.is_public is False

    def test_is_public_false_when_removed(self):
        cal = Calibration.objects.create(
            subject="X",
            result=Calibration.Result.STRONG,
            visibility=Calibration.Visibility.PUBLIC,
            is_removed=True,
        )
        assert cal.is_public is False

    def test_user_calibration_count(self):
        user = User.objects.create_user(username="counter", password="p")
        assert user.calibration_count == 0

        Calibration.objects.create(
            user=user, subject="A", result=Calibration.Result.STRONG
        )
        Calibration.objects.create(
            user=user, subject="B", result=Calibration.Result.WEAK
        )
        assert user.calibration_count == 2


@pytest.mark.django_db
class TestCalibrationAPI:
    """Test the DRF API endpoints."""

    def test_list_public_calibrations(self):
        Calibration.objects.create(
            subject="Public A",
            result=Calibration.Result.STRONG,
            visibility=Calibration.Visibility.PUBLIC,
        )
        Calibration.objects.create(
            subject="Private B",
            result=Calibration.Result.WEAK,
            visibility=Calibration.Visibility.PRIVATE,
        )

        client = Client()
        response = client.get(reverse("calibrations:api_list"))
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["subject"] == "Public A"

    def test_list_filter_by_category(self):
        Calibration.objects.create(
            subject="Pizza",
            result=Calibration.Result.STRONG,
            category=Calibration.Category.FOOD,
            visibility=Calibration.Visibility.PUBLIC,
        )
        Calibration.objects.create(
            subject="Yoga",
            result=Calibration.Result.STRONG,
            category=Calibration.Category.PRACTICE,
            visibility=Calibration.Visibility.PUBLIC,
        )

        client = Client()
        response = client.get(reverse("calibrations:api_list") + "?category=food")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["subject"] == "Pizza"

    def test_list_search_by_subject(self):
        Calibration.objects.create(
            subject="Meditation benefits",
            result=Calibration.Result.STRONG,
            visibility=Calibration.Visibility.PUBLIC,
        )
        Calibration.objects.create(
            subject="Running shoes",
            result=Calibration.Result.WEAK,
            visibility=Calibration.Visibility.PUBLIC,
        )

        client = Client()
        response = client.get(reverse("calibrations:api_list") + "?q=meditation")
        data = response.json()
        assert data["count"] == 1
        assert "Meditation" in data["results"][0]["subject"]

    def test_create_calibration_requires_login(self):
        client = Client()
        response = client.post(
            reverse("calibrations:api_list"),
            {"subject": "X", "result": "strong"},
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_create_calibration_as_user(self):
        User.objects.create_user(
            username="apitest",
            email="api@test.com",
            password="p",
            first_name="API",
            last_name="Tester",
        )
        client = Client()
        client.login(username="api@test.com", password="p")

        response = client.post(
            reverse("calibrations:api_list"),
            {
                "subject": "Green tea",
                "result": "strong",
                "calibration_level": 450,
                "category": "food",
                "visibility": "public",
            },
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.json()
        assert data["subject"] == "Green tea"
        assert data["calibration_level"] == 450
        assert data["submitter_name"] == "API Tester"

    def test_calibration_detail_api(self):
        cal = Calibration.objects.create(
            subject="Detail test",
            result=Calibration.Result.WEAK,
            calibration_level=200,
            visibility=Calibration.Visibility.PUBLIC,
        )
        client = Client()
        response = client.get(reverse("calibrations:api_detail", kwargs={"pk": cal.pk}))
        assert response.status_code == 200
        assert response.json()["subject"] == "Detail test"


@pytest.mark.django_db
class TestCalibrationView:
    """Test the HTML template views."""

    def test_detail_page_public(self):
        user = User.objects.create_user(
            username="author", first_name="Author", password="p"
        )
        cal = Calibration.objects.create(
            user=user,
            subject="A public calibration",
            result=Calibration.Result.STRONG,
            calibration_level=500,
            visibility=Calibration.Visibility.PUBLIC,
            notes="Some notes here.",
        )
        client = Client()
        response = client.get(reverse("calibration_detail", kwargs={"pk": cal.pk}))
        assert response.status_code == 200
        content = response.content.decode()
        assert "A public calibration" in content
        assert "Strong" in content
        assert "500" in content
        assert "Author" in content
        assert "Some notes here" in content
        assert "Disclaimer" in content

    def test_detail_page_404_for_private(self):
        cal = Calibration.objects.create(
            subject="Secret",
            result=Calibration.Result.STRONG,
            visibility=Calibration.Visibility.PRIVATE,
        )
        client = Client()
        response = client.get(reverse("calibration_detail", kwargs={"pk": cal.pk}))
        assert response.status_code == 404

    def test_detail_page_404_for_removed(self):
        cal = Calibration.objects.create(
            subject="Bad entry",
            result=Calibration.Result.STRONG,
            visibility=Calibration.Visibility.PUBLIC,
            is_removed=True,
        )
        client = Client()
        response = client.get(reverse("calibration_detail", kwargs={"pk": cal.pk}))
        assert response.status_code == 404
