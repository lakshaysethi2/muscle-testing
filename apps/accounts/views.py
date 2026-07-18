from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import User


def profile(request, username):
    """Public profile page for any user."""
    profile_user = get_object_or_404(User, username=username)
    return render(
        request,
        "accounts/profile.html",
        {"profile_user": profile_user},
    )


@login_required
def edit_profile(request):
    """Allow logged-in users to edit their own profile."""
    if request.method == "POST":
        user = request.user
        user.bio = request.POST.get("bio", "")
        user.testing_method = request.POST.get(
            "testing_method", user.TestingMethod.O_RING
        )
        if "avatar" in request.FILES:
            user.avatar = request.FILES["avatar"]
        user.save()
        messages.success(request, "Profile updated.")
        return redirect("accounts:profile", username=user.username)

    return render(request, "accounts/edit_profile.html")
