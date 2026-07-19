from rest_framework import serializers

from .models import Calibration


class CalibrationSerializer(serializers.ModelSerializer):
    """Serialize calibrations for the API."""

    submitter_name = serializers.ReadOnlyField()
    calibration_bucket = serializers.SerializerMethodField()

    class Meta:
        model = Calibration
        fields = [
            "id",
            "submitter_name",
            "subject",
            "result",
            "calibration_level",
            "calibration_bucket",
            "method",
            "category",
            "notes",
            "visibility",
            "verification_count",
            "flag_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "verification_count",
            "flag_count",
            "created_at",
            "updated_at",
        ]

    def get_calibration_bucket(self, obj):
        """Map level to Hawkins' consciousness bucket."""
        if obj.calibration_level is None:
            return None
        if obj.calibration_level < 200:
            return "Force"
        if obj.calibration_level < 400:
            return "Lower Mind"
        if obj.calibration_level < 500:
            return "Reason"
        if obj.calibration_level < 540:
            return "Love"
        if obj.calibration_level < 600:
            return "Joy"
        if obj.calibration_level < 700:
            return "Peace"
        return "Enlightenment"

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)
