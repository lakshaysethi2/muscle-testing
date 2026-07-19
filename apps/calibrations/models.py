"""Calibration model — the heart of TruthCheck.

Stores individual muscle-testing results. Each calibration records:
- What was tested (subject)
- The result (strong/weak)
- An optional numerical calibration on Hawkins' Map of Consciousness (1–1000)
- The testing method used
- Visibility and community-sharing preferences
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from apps.accounts.models import User
from apps.core.models import TimestampedModel


class Calibration(TimestampedModel):
    """A single muscle-testing calibration result."""

    class Result(models.TextChoices):
        STRONG = "strong", "Strong (True / Yes / Positive)"
        WEAK = "weak", "Weak (False / No / Negative)"

    class Category(models.TextChoices):
        PERSON = "person", "Person"
        PLACE = "place", "Place"
        FOOD = "food", "Food / Supplement"
        IDEA = "idea", "Idea / Concept"
        BOOK = "book", "Book / Media"
        SUBSTANCE = "substance", "Substance"
        ENTITY = "entity", "Entity / Organization"
        PRACTICE = "practice", "Practice / Technique"
        OTHER = "other", "Other"

    class Visibility(models.TextChoices):
        PRIVATE = "private", "Only Me"
        PUBLIC = "public", "Community (Public)"

    # Core fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="calibrations",
        null=True,
        blank=True,
        help_text="User who performed the test. Null for anonymous.",
    )
    subject = models.CharField(
        max_length=300,
        help_text="The person, object, idea, or statement being tested.",
    )
    result = models.CharField(
        max_length=10,
        choices=Result.choices,
        help_text="Strong = true/resonant; Weak = false/dissonant.",
    )

    # Map of Consciousness
    calibration_level = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text="Numerical calibration (1–1000) on Hawkins' Map of Consciousness.",
    )

    # Testing method for this specific test
    method = models.CharField(
        max_length=30,
        choices=User.TestingMethod.choices,
        default=User.TestingMethod.O_RING,
        help_text="Method used for this test.",
    )

    # Metadata
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.OTHER
    )
    notes = models.TextField(
        blank=True, default="", help_text="Context or observations."
    )
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
        help_text="PRIVATE = only you; PUBLIC = appears in Community DB.",
    )

    # Community feedback
    verification_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of community verifications.",
    )
    flag_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times flagged for review.",
    )
    is_removed = models.BooleanField(
        default=False,
        help_text="Soft-delete: hidden from public when True.",
    )

    class Meta:
        db_table = "calibrations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["subject"]),
            models.Index(fields=["category"]),
            models.Index(fields=["visibility"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["result"]),
        ]

    def __str__(self):
        icon = "✅" if self.result == self.Result.STRONG else "❌"
        level = f" [{self.calibration_level}]" if self.calibration_level else ""
        return f"{icon} {self.subject}{level}"

    def get_absolute_url(self):
        return reverse("calibration_detail", kwargs={"pk": self.pk})

    @property
    def submitter_name(self):
        """Display name for community listings."""
        if self.user:
            return self.user.display_name
        return "Anonymous"

    @property
    def is_public(self):
        return self.visibility == self.Visibility.PUBLIC and not self.is_removed
