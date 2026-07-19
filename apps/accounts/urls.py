from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
]
