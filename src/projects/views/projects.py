from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common_services.permissions.project_permission import ProjectPermission
from projects.models import Project
from projects.serializers.project_serializer import ProjectSerializer
from projects.services.project_service import ProjectService


class ProjectReadOnlyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    ViewSet для просмотра проектов.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def list(self, request, *args, **kwargs):
        projects = ProjectService.get_all_projects(request.user_id, request.role_name)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        project_id = kwargs.get("pk")
        project = ProjectService.get_project_by_id(project_id=project_id)
        serializer = self.get_serializer(project)
        return Response(serializer.data)


class ProjectCreateViewSet(CreateModelMixin, GenericViewSet):
    """
    ViewSet для создания проектов.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def create(self, request, *args, **kwargs):
        project = ProjectService.create_new_project(request=request, data=request.data)
        return Response(project, status=201)


class ProjectUpdateViewSet(UpdateModelMixin, GenericViewSet):
    """
    ViewSet для обновления проектов.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        updated_project = ProjectService.update_project(request.data, project)
        return Response(updated_project, status=200)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProjectDeleteViewSet(DestroyModelMixin, GenericViewSet):
    """
    ViewSet для удаления проектов.
    """

    queryset = Project.objects.all()
    permission_classes = [ProjectPermission]

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        deleted_project = ProjectService.delete_project(project)
        return Response(deleted_project, status=204)
