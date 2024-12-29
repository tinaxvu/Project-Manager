from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    custom_username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    permission_level = models.CharField(max_length=20,
                                        choices=[('admin', 'Admin'), ('owner', 'Owner'), ('common', 'Common')],
                                        default='member')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    profile_description = models.TextField(blank=True, null=True)
    requested_projects = models.ManyToManyField('projects.Project', related_name="users_requested_projects", blank=True)
    joined_projects = models.ManyToManyField('projects.Project', related_name="member", blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def owned_projects(self):
        return self.projects.filter(permission_level='owner')

    def __str__(self):
        return self.username

