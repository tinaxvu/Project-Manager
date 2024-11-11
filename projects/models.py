from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="created_projects")
    members = models.ManyToManyField('users.User', related_name="member_projects")
    requested = models.ManyToManyField('users.User', related_name="projects_requested_by_users", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically add creator as a member of the project
        self.members.add(self.created_by)

    def __str__(self):
        return self.name


class Todo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="todos")
    description = models.TextField()
    date_due = models.DateField()
    is_finished = models.BooleanField(default=False)
    priority = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    assigned_to = models.ManyToManyField('users.User', related_name="assigned_todos", blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="created_todos")

    def __str__(self):
        return self.description


class Calendar(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="calendar_events")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField()
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="created_calendar_events")

    def __str__(self):
        return self.title


class Collaboration(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="collaborations")
    title = models.CharField(max_length=200, default="Untitled Collaboration")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="created_collaborations")

    def __str__(self):
        return self.title


class TeamHandbook(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="team_handbook")
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.custom_username}'s description"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.name


class FileUpload(models.Model):
    User = get_user_model()
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name="files")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="uploaded_files")
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_title = models.CharField(default="", max_length=255, help_text="Title for the file")
    description = models.TextField(default="", help_text="Description of the file content")
    keywords = models.TextField(help_text="Comma-separated list of keywords for the file", blank=True)
    tags = models.ManyToManyField(Tag, related_name="files", blank=True)

    def __str__(self):
        return self.file.name


class Timeline(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="timeline")
    event = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.event


class ScheduleMeet(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="schedule_meets")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    meeting_date = models.DateTimeField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    #location = models.CharField(max_length=100, blank=True, null=True)
    #participants = models.ManyToManyField('users.User', related_name="meetings_attending", blank=True)

    def __str__(self):
        return self.title
