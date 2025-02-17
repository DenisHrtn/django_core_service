from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from health_check import urls as health_check_urls
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="DJango Core Service API",
        default_version="v1",
        description="Swagger docs for all APIs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="test@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # django-health-check urls
    path("health/", include(health_check_urls)),
    path("admin/", admin.site.urls),
    path("api/projects/", include("projects.urls")),
    path("api/tickets/", include("tickets.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
