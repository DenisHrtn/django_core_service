from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from projects.models import Project
from projects.permissions.project_permission import ProjectPermission
from projects.serializers.project_serializer import (
    ProjectSerializer,
    ProjectsTicketsSerializer,
)
from projects.services.project_service import ProjectService


class ProjectReadOnlyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    ViewSet для просмотра проектов.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def get_queryset(self):
        return ProjectService.get_all_projects(
            self.request.user_id, self.request.role_name
        )

    def get_object(self):
        project_id = self.kwargs.get("pk")
        try:
            return ProjectService.get_project_by_id(project_id=project_id)
        except Project.DoesNotExist as exc:
            raise NotFound("Проект не найден") from exc


class ProjectCreateViewSet(GenericViewSet):
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

    def get_object(self):
        project_id = self.kwargs.get("pk")
        try:
            return Project.objects.get(pk=project_id)
        except Project.DoesNotExist as exc:
            raise NotFound("Проект не найден") from exc

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(
            instance=project, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class ProjectDeleteViewSet(DestroyModelMixin, GenericViewSet):
    """
    ViewSet для удаления проектов.
    """

    queryset = Project.objects.all()
    permission_classes = [ProjectPermission]

    def get_object(self):
        project_id = self.kwargs.get("pk")
        try:
            return Project.objects.get(pk=project_id)
        except Project.DoesNotExist as exc:
            raise NotFound("Проект не найден") from exc

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        deleted_project = ProjectService.delete_project(project)
        return Response(deleted_project, status=204)


class ProjectWithTasksViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Ручка для получения проектов с их задачами
    """

    serializer_class = ProjectsTicketsSerializer
    permission_classes = [ProjectPermission]

    def get_queryset(self):
        try:
            return ProjectService.get_all_projects_with_tasks(request=self.request)
        except ObjectDoesNotExist as exc:
            raise NotFound("Не найдены проекты с задачами") from exc
