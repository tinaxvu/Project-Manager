from django.urls import path
from .views import user_projects, project_files, upload_file

urlpatterns = [
    path('projects/', user_projects, name='user_projects'),  # URL for user projects
    path('project/<int:project_id>/files/', project_files, name='project_files'),  # URL for project files
    path('upload/', upload_file, name='upload_file'),  # URL for file upload
]
