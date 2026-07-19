from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions

from .models import Calibration
from .serializers import CalibrationSerializer

# --- API views ---


class CalibrationListCreateAPI(generics.ListCreateAPIView):
    """List public calibrations, or create a new one."""

    serializer_class = CalibrationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Calibration.objects.filter(
            visibility=Calibration.Visibility.PUBLIC, is_removed=False
        )
        # Filters
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        subject = self.request.query_params.get("q")
        if subject:
            qs = qs.filter(subject__icontains=subject)
        return qs.select_related("user")


class CalibrationDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single calibration."""

    serializer_class = CalibrationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Calibration.objects.all().select_related("user")

    def get_object(self):
        obj = super().get_object()
        # Only the owner can update/delete
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            if obj.user != self.request.user:
                self.permission_denied(self.request)
        return obj


# --- Template views ---


def calibration_detail(request, pk):
    """Public detail page for a community calibration."""
    cal = get_object_or_404(
        Calibration.objects.select_related("user"),
        pk=pk,
        visibility=Calibration.Visibility.PUBLIC,
        is_removed=False,
    )
    return render(request, "calibrations/detail.html", {"cal": cal})
