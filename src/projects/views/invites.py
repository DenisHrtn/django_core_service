from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from projects.models import Invite
from projects.permissions.project_invite import InvitePermission
from projects.serializers.invite_serializer import (
    AcceptInviteSerializer,
    InviteSerializer,
)
from projects.services.project_invite_service import ProjectInviteService


class ProjectInviteReadOnlyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    ViewSet для просмотра проектов
    """

    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [InvitePermission]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")

        return ProjectInviteService.get_all_invites(
            self.request.user_id, project_id, self.request.role_name
        )

    def get_object(self):
        invite_id = self.kwargs.get("invite_id")

        try:
            return ProjectInviteService.get_invite_by_id(invite_id)
        except ObjectDoesNotExist as exc:
            raise NotFound("Инвайт не найден") from exc


class ProjectInviteCrateViewSet(CreateModelMixin, GenericViewSet):
    """
    ViewSet для создания и отправки инвайта
    """

    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [InvitePermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invite_data = serializer.validated_data
        response_data = ProjectInviteService.send_invite(
            data=invite_data, project_id=kwargs["project_id"]
        )

        return Response(response_data, status=201)


class ProjectInviteAcceptViewSet(UpdateModelMixin, GenericViewSet):
    """
    ViewSet для отправки ответа юзером
    """

    queryset = Invite.objects.all()
    serializer_class = AcceptInviteSerializer
    permission_classes = [InvitePermission]

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_data = serializer.validated_data
        response_data = ProjectInviteService.accept_invite(
            token=invite_data["token"],
            invite_response=invite_data["invite_response"],
            request=self.request,
        )

        return Response(response_data, status=200)
