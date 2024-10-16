from django.conf import settings
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Todo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="todos")
    description = models.TextField()
    date_due = models.DateField()
    is_finished = models.BooleanField(default=False)
    priority = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    custom_labels = models.CharField(max_length=100, blank=True, null=True)
    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TodoAssignment', related_name="assigned_todos")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_todos")

    def __str__(self):
        return f"{self.description} - {self.project.name}"

class TodoAssignment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('todo', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.todo.description}"

class Calendar(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="calendar_events")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_calendar_events")

    def __str__(self):
        return f"{self.title} - {self.project.name}"

class Collaboration(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="collaborations")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_collaborations")

    def __str__(self):
        return f"Collaboration - {self.project.name} by {self.created_by}"

class TeamHandbook(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="team_handbook")
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Handbook - {self.project.name}"

class FileUpload(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    file_path = models.FileField(upload_to='project_files/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="uploaded_files")
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_path.name} - {self.project.name}"

class Timeline(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="timeline")
    milestone = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"Milestone: {self.milestone} - {self.project.name}"

class ScheduleMeet(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="schedule_meets")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    meeting_date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True, null=True)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="meetings_attending", blank=True)

    def __str__(self):
        return f"Meeting: {self.title} - {self.project.name}"
