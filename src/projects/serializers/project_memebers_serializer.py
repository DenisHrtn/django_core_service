from rest_framework import serializers

from projects.models import ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = "__all__"
        read_only_fields = ("member_id", "user_id", "email", "created_at", "updated_at")

    def update(self, instance, validated_data):
        """
        Метод обновления участника проекта
        """
        permissions = validated_data.get("permissions")
        if permissions:
            instance.permissions = permissions

        instance.save()
        return instance
