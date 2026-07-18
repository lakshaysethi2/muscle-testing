from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Dev-specific overrides
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
