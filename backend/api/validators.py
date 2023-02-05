from rest_framework import serializers


class DoubleValidator:
    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def __call__(self, value):
        values = [value[field_name] for field_name in self.fields]
        if len(values) != len(set(values)):
            raise serializers.ValidationError(
                self.message)
