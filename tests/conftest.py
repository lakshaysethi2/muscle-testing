from django.conf import settings


def pytest_configure():
    settings.DEBUG = False
    settings.DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
