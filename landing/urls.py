from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # landing page
    path('calendar/', views.calendar_view, name='calendar'),  # calendar
    path('team-handbook/', views.team_handbook_view, name='team_handbook'),  # team handbook
    path('collaboration/', views.collaboration_view, name='collaboration'),  # collaboration
    path('todos/', views.todos_view, name='todos'),  # to-do's
    path('timeline/', views.timeline_view, name='timeline'),  # timeline
    path('files/', views.files_view, name='files'),  # files
    path('schedule-meets/', views.schedule_meets_view, name='schedule_meets'),  # schedule meets
]
