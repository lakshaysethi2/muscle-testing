from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """Custom User model for TruthCheck.

    Fields beyond AbstractUser:
    - bio: user's self-description / intention
    - avatar: profile picture
    - testing_method: preferred muscle testing technique
    - karma: community trust score (upvotes minus flags)
    """

    class TestingMethod(models.TextChoices):
        O_RING = "o_ring", "O-Ring Test (two-person)"
        FINGER_OVER_FINGER = "finger_over_finger", "Finger-over-Finger"
        SWAY = "sway", "Sway Test"
        INTERLOCKING_O = "interlocking_o", "Interlocking O-Ring (solo)"
        PROXY = "proxy", "Proxy / Surrogate Testing"
        OTHER = "other", "Other"

    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    testing_method = models.CharField(
        max_length=30,
        choices=TestingMethod.choices,
        default=TestingMethod.O_RING,
        help_text="Preferred muscle testing method",
    )
    karma = models.IntegerField(default=0, help_text="Community trust score")

    class Meta:
        db_table = "accounts_user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.get_full_name() or self.email or self.username

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"username": self.username})

    @property
    def display_name(self):
        """Fall back through name → email → username."""
        return self.get_full_name() or self.email or self.username

    @property
    def calibration_count(self):
        """Total calibrations submitted by this user.

        Returns 0 until the Calibration model with related_name='calibrations'
        is added to the calibrations app.
        """
        if hasattr(self, "calibrations"):
            return self.calibrations.count()
        return 0
