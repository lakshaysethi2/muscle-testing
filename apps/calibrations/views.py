from django.db.models import Q
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
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        subject = self.request.query_params.get("q")
        if subject:
            qs = qs.filter(subject__icontains=subject)
        return qs.select_related("user")


class CalibrationDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single calibration.

    - Anonymous users: only public, non-removed records.
    - Authenticated users: public non-removed + their own records.
    - Writes (PUT/PATCH/DELETE): owner only.
    """

    serializer_class = CalibrationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Calibration.objects.filter(is_removed=False)
        if self.request.user.is_authenticated:
            qs = qs.filter(
                Q(visibility=Calibration.Visibility.PUBLIC) | Q(user=self.request.user)
            )
        else:
            qs = qs.filter(visibility=Calibration.Visibility.PUBLIC)
        return qs.select_related("user")

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            if not self.request.user.is_authenticated or obj.user != self.request.user:
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
