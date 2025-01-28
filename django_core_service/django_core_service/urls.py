from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # django-health-check urls
    path(r"ht/", include("health_check.urls")),
]
