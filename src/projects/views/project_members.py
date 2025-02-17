from rest_framework.exceptions import NotFound
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from projects.models import ProjectMember
from projects.permissions.project_members_permissions import ProjectMemberPermissions
from projects.serializers.project_memebers_serializer import ProjectMemberSerializer
from projects.services.project_members_service import ProjectMembersService


class ProjectMembersReadOnlyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [ProjectMemberPermissions]
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.all()

    def get_queryset(self):
        return ProjectMembersService.get_project_members(
            project_id=self.kwargs["project_id"], role_name=self.request.role_name
        )

    def get_object(self):
        return ProjectMembersService.get_project_member_by_id(
            project_id=self.kwargs["project_id"], member_id=self.kwargs["member_id"]
        )


class ProjectMembersUpdateViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [ProjectMemberPermissions]
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.all()

    def get_object(self):
        return ProjectMembersService.get_project_member_by_id(
            project_id=self.kwargs["project_id"], member_id=self.kwargs["member_id"]
        )

    def partial_update(self, request, *args, **kwargs):
        project_member = self.get_object()

        serializer = self.get_serializer(
            instance=project_member, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)


class ProjectMembersDeleteViewSet(DestroyModelMixin, GenericViewSet):
    permission_classes = [ProjectMemberPermissions]
    queryset = ProjectMember.objects.all()

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return ProjectMember.objects.filter(project_id=project_id)

    def get_object(self):
        project_id = self.kwargs.get("project_id")
        member_id = self.kwargs.get("member_id")
        try:
            return ProjectMember.objects.get(project_id=project_id, member_id=member_id)
        except ProjectMember.DoesNotExist as exc:
            raise NotFound("Участник проекта не найден") from exc

    def destroy(self, request, *args, **kwargs):
        project_member = self.get_object()
        deleted_project_members = ProjectMembersService.delete_project_member(
            member_id=project_member.member_id, project_id=project_member.project_id
        )
        return Response(deleted_project_members, status=204)
