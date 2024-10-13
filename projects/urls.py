from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create', views.create_project, name='create-project'),
    path('<int:project_id>/', views.project_detail, name='project-detail'),
    path('calendar/', views.calendar_view, name='calendar'),  # calendar
    path('team-handbook/', views.team_handbook_view, name='team-handbook'),  # team handbook
    path('collaboration/', views.collaboration_view, name='collaboration'),  # collaboration
    path('todos/', views.todos_view, name='todos'),  # to-do's
    path('timeline/', views.timeline_view, name='timeline'),  # timeline
    path('files/', views.files_view, name='files'),  # files
    path('schedule-meets/', views.schedule_meets_view, name='schedule-meets'),  # schedule meets
]