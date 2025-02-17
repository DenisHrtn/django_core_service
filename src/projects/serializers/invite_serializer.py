from rest_framework import serializers

from projects.models import Invite


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = [
            "invite_id",
            "project_id",
            "token",
            "email",
            "status",
            "created_at",
        ]
        read_only_fields = ["invite_id", "token", "created_at"]


class AcceptInviteSerializer(serializers.Serializer):
    token = serializers.CharField()
    invite_response = serializers.BooleanField()
