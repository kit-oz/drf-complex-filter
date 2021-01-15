from rest_framework import serializers

from .models import TestCaseModel


class TestCaseModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestCaseModel
        fields = (
            "group1",
            "group2",
            "integer",
            "float",
            "date",
            "datetime",
            "user",
        )
