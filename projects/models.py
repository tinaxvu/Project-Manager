from django.conf import settings
from django.db import models
from django.utils import timezone

# from users.models import User

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="created_projects")
    members = models.ManyToManyField('users.User', related_name="member_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

class FileUpload(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    uploaded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name="uploaded_files")
    file_name = models.CharField(max_length=255, default="Untitled File")
    s3_url = models.URLField(default="")
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

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
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100, blank=True, null=True)
    participants = models.ManyToManyField('users.User', related_name="meetings_attending", blank=True)

    def __str__(self):
        return self.title
