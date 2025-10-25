from rest_framework import serializers

class ProjectCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=191)
    description = serializers.CharField(allow_blank=True, required=False)
