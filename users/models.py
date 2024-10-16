from django.db import models
from django.contrib.auth.models import AbstractUser
from projects.models import Project

class User(AbstractUser):
    permission_level = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('owner', 'Owner'), ('member', 'Member')], default='member')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    custom_username = models.CharField(max_length=50, blank=True, null=True)
    profile_description = models.TextField(blank=True, null=True)
    requested_projects = models.ManyToManyField(Project, related_name="pending_requests", blank=True)
    joined_projects = models.ManyToManyField(Project, related_name="members", blank=True)

    def owned_projects(self):
        return Project.objects.filter(owner=self)

    def __str__(self):
        return self.username