from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")  # noqa: F405

# Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Postgres in prod
DATABASES = {"default": env.db_url("DATABASE_URL")}  # noqa: F405

# Static files — whitenoise serves in prod
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
