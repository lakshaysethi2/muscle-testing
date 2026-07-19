from django.urls import path

from apps.calibrations.views import calibration_detail

from . import views, wizard

urlpatterns = [
    path("", views.home, name="home"),
    path("test/", wizard.guided_test, name="start_testing"),
    path(
        "community/",
        views.coming_soon,
        {"feature": "F-09 — Community Database"},
        name="community_db",
    ),
    path(
        "practice/",
        views.coming_soon,
        {"feature": "F-12 — Practice Mode"},
        name="practice",
    ),
    path(
        "dashboard/",
        views.coming_soon,
        {"feature": "F-13 — Personal Dashboard"},
        name="dashboard",
    ),
    path("calibrations/<int:pk>/", calibration_detail, name="calibration_detail"),
]
