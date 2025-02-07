from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.project_members import (
    ProjectMembersDeleteViewSet,
    ProjectMembersReadOnlyViewSet,
    ProjectMembersUpdateViewSet,
)
from .views.projects import (
    ProjectCreateViewSet,
    ProjectDeleteViewSet,
    ProjectReadOnlyViewSet,
    ProjectUpdateViewSet,
)

router = DefaultRouter()
router.register(r"projects", ProjectReadOnlyViewSet, basename="projects")

urlpatterns = [
    path(
        "projects/create/",
        ProjectCreateViewSet.as_view({"post": "create"}),
        name="project-create",
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateViewSet.as_view({"put": "update", "patch": "partial_update"}),
        name="project-update",
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteViewSet.as_view({"delete": "destroy"}),
        name="project-delete",
    ),
    path(
        "projects/<int:project_id>/members/",
        ProjectMembersReadOnlyViewSet.as_view({"get": "list"}),
        name="project-members-list",
    ),
    path(
        "projects/<int:project_id>/members/<int:member_id>/",
        ProjectMembersReadOnlyViewSet.as_view({"get": "retrieve"}),
        name="project-members-detail",
    ),
    path(
        "projects/<int:project_id>/members-update/<int:member_id>/",
        ProjectMembersUpdateViewSet.as_view({"patch": "partial_update"}),
        name="project-members-update",
    ),
    path(
        "projects/<int:project_id>/members-destroy/<int:member_id>/",
        ProjectMembersDeleteViewSet.as_view({"delete": "destroy"}),
        name="project-members-delete",
    ),
]

urlpatterns += router.urls
