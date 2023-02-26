from rest_framework import serializers
from .models import Url
from django.utils import timezone


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = [
            "original_url",
            "short_url",
            "expires_at",
        ]

    def validate_expires_at(self, value):
        """
        Checks that if the expiring datetime is in the past
        """
        if value and timezone.now() > value:
            raise serializers.ValidationError(
                "The specified expiration date/time is in the past."
            )
        return value
