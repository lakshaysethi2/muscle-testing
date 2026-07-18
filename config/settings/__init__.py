import os

DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev")

if DJANGO_ENV == "prod":
    from .prod import *  # noqa: F403
else:
    from .dev import *  # noqa: F403
