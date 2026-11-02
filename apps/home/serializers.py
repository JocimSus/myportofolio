from typing import ClassVar

from django.utils.html import strip_tags
from rest_framework import serializers

from .models import Project


class TechnologiesField(serializers.ListField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = [data]
        if isinstance(data, list):
            data = [
                value.strip()
                for item in data
                for value in str(item).split(",")
                if value.strip()
            ]
        return super().to_internal_value(data)

    def run_child_validation(self, data):
        values = super().run_child_validation(data)
        return [
            strip_tags(value).strip() for value in values if strip_tags(value).strip()
        ]


class ProjectSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    technologies = TechnologiesField(required=False)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields: ClassVar = [
            "id",
            "slug",
            "title",
            "description",
            "thumbnail",
            "project_url",
            "technologies",
            "category",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields: ClassVar = [
            "id",
            "slug",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return obj.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
