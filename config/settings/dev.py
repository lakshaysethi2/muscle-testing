from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Dev-specific overrides
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Dev convenience: disable email verification and allow instant logout
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = True
