from django.urls import path, include
from rest_framework.routers import DefaultRouter
from freelancing.projects import api

router = DefaultRouter()
router.register("v1/project_types", api.ProjectTypeViewSet, basename="project_types")
router.register("v1/projects", api.ProjectViewSet, basename="projects")

urlpatterns = [
    path("", include(router.urls)),
]
