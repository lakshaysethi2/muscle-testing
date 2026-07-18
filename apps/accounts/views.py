from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileEditForm
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
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.bio = form.cleaned_data["bio"]
            user.testing_method = form.cleaned_data["testing_method"]
            if "avatar" in request.FILES:
                user.avatar = request.FILES["avatar"]
            user.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile", username=user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(
            initial={
                "bio": request.user.bio,
                "testing_method": request.user.testing_method,
            }
        )

    return render(request, "accounts/edit_profile.html", {"form": form})
