from rest_framework import serializers
from freelancing.projects.models import Project, ProjectType

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ['id', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    type = ProjectTypeSerializer()  # Nested serialization of type

    class Meta:
        model = Project
        fields = ['id', 'type', 'pic', 'title', 'desc', 'live_link', 'exe_or_build']


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['type', 'pic', 'title', 'desc', 'live_link', 'exe_or_build']
