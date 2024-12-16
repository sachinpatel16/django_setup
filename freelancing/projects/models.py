from django.db import models


from freelancing.custom_auth.models import BaseModel
# Create your models here.


class ProjectType(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Project(BaseModel):
    type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, related_name="projects")
    pic = models.ImageField(upload_to="project_pics/")
    title = models.CharField(max_length=255)
    desc = models.TextField()
    live_link = models.URLField(blank=True, null=True)
    exe_or_build = models.FileField(upload_to="project_files/", blank=True, null=True)

    def __str__(self):
        return self.title