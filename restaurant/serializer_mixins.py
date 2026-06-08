from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


class DjangoValidationErrorMixin:
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(self._format_django_error(exc)) from exc

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(self._format_django_error(exc)) from exc

    @staticmethod
    def _format_django_error(exc):
        if hasattr(exc, "message_dict"):
            return exc.message_dict
        return exc.messages
