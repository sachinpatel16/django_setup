from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources
from freelancing.projects.models import ProjectType, Project

# Define resources for import-export functionality
class ProjectTypeResource(resources.ModelResource):
    class Meta:
        model = ProjectType
        fields = ('id', 'name', 'create_time', 'update_time')  # Use create_time and update_time
        export_order = ('id', 'name', 'create_time', 'update_time')

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('id', 'type__name', 'title', 'desc', 'live_link', 'create_time', 'update_time')  # Use create_time and update_time
        export_order = ('id', 'type__name', 'title', 'desc', 'live_link', 'create_time', 'update_time')

# Register admin with import-export functionality
@admin.register(ProjectType)
class ProjectTypeAdmin(ImportExportModelAdmin):
    resource_class = ProjectTypeResource
    list_display = ('id', 'name', 'create_time', 'update_time')  # Use create_time and update_time
    search_fields = ('name',)
    list_filter = ('create_time',)

@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    list_display = ('id', 'title', 'type', 'live_link', 'create_time', 'update_time')  # Use create_time and update_time
    search_fields = ('title', 'type__name')
    list_filter = ('type', 'create_time')
