from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create/', views.create_project, name='create-project'),
    path('<int:project_id>/', views.project_detail, name='project-detail'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('team-handbook/', views.team_handbook_view, name='team-handbook'),
    path('collaboration/', views.collaboration_view, name='collaboration'),
    path('todos/', views.todos_view, name='todos'),
    path('timeline/', views.timeline_view, name='timeline'),
    path('schedule-meets/', views.schedule_meets_view, name='schedule-meets'),
    path('<int:project_id>/files/', views.project_files, name='project_files'),
    path('<int:project_id>/request-to-join/', views.request_to_join, name='request-to-join'),
    path('<int:project_id>/approve-request/<int:user_id>/', views.approve_request, name='approve-request'),
    path('<int:project_id>/deny-request/<int:user_id>/', views.deny_request, name='deny-request'),
    path('<int:project_id>/collaboration/', views.collaboration_view, name='collaboration'),
]
