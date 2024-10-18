from django.db import models
from django.contrib.auth.models import AbstractUser
from projects.models import Project

class User(AbstractUser):
    custom_username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    permission_level = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('owner', 'Owner'), ('common', 'Common')], default='member')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    profile_description = models.TextField(blank=True, null=True)
    requested_projects = models.ManyToManyField(Project, related_name="requested", blank=True)
    joined_projects = models.ManyToManyField(Project, related_name="member", blank=True)

    def owned_projects(self):
        return Project.objects.filter(owner=self)

    def __str__(self):
        return self.username