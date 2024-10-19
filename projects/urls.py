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
    path('schedule-meets/', views.schedule_meets_view, name='schedule-meets'),  # schedule meets
    path('<int:project_id>/request-to-join/', views.request_to_join, name='request-to-join'),  # request to join
    path('<int:project_id>/files/', views.project_files, name='project_files'),
]
