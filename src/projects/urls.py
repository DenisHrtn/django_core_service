from django.urls import path
from rest_framework.routers import DefaultRouter

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
]

urlpatterns += router.urls
