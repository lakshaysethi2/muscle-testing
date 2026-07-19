"""Template context processors for TruthCheck."""

from allauth.socialaccount.models import SocialApp


def social_providers(request):
    """Expose configured social providers to all templates.

    Returns an empty list if no providers are configured in the admin,
    so templates can conditionally hide social login buttons.
    """
    providers = []
    try:
        for app in SocialApp.objects.all().prefetch_related("sites"):
            if app.provider:
                providers.append({"id": app.provider, "name": app.name})
    except Exception:
        # Table may not exist during initial migrations
        pass
    return {"socialaccount_providers": providers}
