from django.contrib import admin
from django.urls import include, path
from health_check import urls as health_check_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    # django-health-check urls
    path("health/", include(health_check_urls)),
]
