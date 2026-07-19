from django.urls import path

from . import views

app_name = "calibrations"

urlpatterns = [
    path("", views.CalibrationListCreateAPI.as_view(), name="api_list"),
    path("<int:pk>/", views.CalibrationDetailAPI.as_view(), name="api_detail"),
]
