from rest_framework import serializers

from tickets.models.ticket import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("ticket_id", "project", "creator", "assignee_ids")

    def update(self, instance, validated_data):
        """
        Метод обновления задачи
        """
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AssigneeActionSerializer(serializers.Serializer):
    """
    Сериализатор для добавления участника на задачу
    """

    user_id = serializers.IntegerField(required=True)
