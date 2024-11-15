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
    path('<int:project_id>/files/delete/<int:file_id>/', views.delete_file, name='delete-file'),
    path('<int:project_id>/request-to-join/', views.request_to_join, name='request-to-join'),
    path('<int:project_id>/approve-request/<int:user_id>/', views.approve_request, name='approve-request'),
    path('<int:project_id>/deny-request/<int:user_id>/', views.deny_request, name='deny-request'),
    path('<int:project_id>/collaboration/', views.collaboration_view, name='collaboration'),
    path('<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('<int:project_id>/file/<int:file_id>/', views.view_file, name='view_file'),
    path('<int:project_id>/leave-project', views.leave_project, name="leave_project"),
    path('<int:project_id>/message_board', views.message_board_view, name="message_board"),
    path('<int:project_id>/<int:message_id>/delete_message', views.delete_message, name="delete_message"),
    path('<int:project_id>/<int:thread_id>/pin_thread', views.pin_thread,name="pin_thread"),
    path('<int:project_id>/<int:thread_id>/unpin_thread', views.unpin_thread,name="unpin_thread"),
    path('<int:project_id>/<int:thread_id>/delete_thread', views.delete_thread,name="delete_thread")
]
