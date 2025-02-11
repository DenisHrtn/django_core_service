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
        access_rights = validated_data.get("access_rights")
        if access_rights:
            instance.access_rights = access_rights

        instance.save()
        return instance
