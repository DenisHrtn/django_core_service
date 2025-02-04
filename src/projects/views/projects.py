from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from projects.serializers.project_serializer import ProjectSerializer
from projects.services.project_service import ProjectService


class ProjectViewSet(ViewSet):
    def list(self, request):
        projects = ProjectService.get_all_projects(request)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=200)

    def retrieve(self, request, pk=None):
        project = ProjectService.get_project_by_id(request=request, project_id=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=200)

    def create(self, request):
        project = ProjectService.create_new_project(request=request, data=request.data)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        project = ProjectService.update_project(request=request, data=request.data)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        project = ProjectService.update_project(request=request, data=request.data)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=200)

    def destroy(self, request, pk=None):
        project = ProjectService.delete_project(request=request, project_id=pk)
        return Response({"status": project}, status=200)
