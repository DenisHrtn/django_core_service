from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common_services.permissions.project_members_permissions import (
    ProjectMemberPermissions,
)
from projects.models import ProjectMember
from projects.serializers.project_memebers_serializer import ProjectMemberSerializer
from projects.services.project_members_service import ProjectMembersService


class ProjectMembersReadOnlyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [ProjectMemberPermissions]
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.all()

    def list(self, request, *args, **kwargs):
        project_members = ProjectMembersService.get_project_members(
            project_id=kwargs["project_id"], role_name=request.role_name
        )
        serializer = ProjectMemberSerializer(project_members, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        project_members = ProjectMembersService.get_project_member_by_id(
            project_id=kwargs["project_id"], member_id=kwargs["member_id"]
        )
        serializer = ProjectMemberSerializer(project_members)
        return Response(serializer.data)


class ProjectMembersUpdateViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [ProjectMemberPermissions]
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.all()

    def update(self, request, *args, **kwargs):
        updated_project_members = ProjectMembersService.update_project_member(
            member=kwargs["member_id"],
            data=request.data,
            project_id=kwargs["project_id"],
        )
        return Response(updated_project_members, status=200)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProjectMembersDeleteViewSet(DestroyModelMixin, GenericViewSet):
    permission_classes = [ProjectMemberPermissions]
    queryset = ProjectMember.objects.all()

    def destroy(self, request, *args, **kwargs):
        deleted_project_members = ProjectMembersService.delete_project_member(
            member_id=kwargs["member_id"], project_id=kwargs["project_id"]
        )
        return Response(deleted_project_members, status=204)
