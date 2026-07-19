from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def coming_soon(request, feature=""):
    """Fallback page for features not yet built."""
    ctx = {"feature": feature}
    return render(request, "pages/coming_soon.html", ctx)
