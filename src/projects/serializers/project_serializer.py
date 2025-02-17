from rest_framework import serializers

from projects.models.project import Project
from tickets.serializers import TicketSerializer


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


class ProjectsTicketsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения всех проектов и их тикетов
    """

    tickets = TicketSerializer(many=True, source="tickets.all")

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("project_id", "created_at", "updated_at")

    def to_representation(self, instance):
        """
        Используем, чтобы сделать JSON с тикетами последним полем.
        """
        data = super().to_representation(instance)
        tickets = data.pop("tickets")
        data["tickets"] = tickets
        return data
