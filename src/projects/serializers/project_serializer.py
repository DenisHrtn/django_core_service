from rest_framework import serializers

from projects.models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с моделью Project
    """

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("project_id", "created_at", "updated_at")

    def update(self, instance, validated_data):
        """
        Метод обновления проекта
        """
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
