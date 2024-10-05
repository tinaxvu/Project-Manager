# landing/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def landing_page(request):
    if request.user.is_authenticated:
        user = request.user
        user_email = user.email  # Get the logged-in user's email
        user_groups = user.groups.all()
        return render(request, 'landing/index.html', {'email': user_email, 'groups': user_groups})
    else:
        return render(request, 'landing/index.html', {'error': 'You are not logged in.'})

@login_required
def calendar_view(request):
    return render(request, 'specific_pages/calendar.html')

@login_required
def team_handbook_view(request):
    return render(request, 'specific_pages/team_handbook.html')

@login_required
def collaboration_view(request):
    return render(request, 'specific_pages/collaboration.html')

@login_required
def todos_view(request):
    return render(request, 'specific_pages/todos.html')

@login_required
def timeline_view(request):
    return render(request, 'specific_pages/timeline.html')

@login_required
def files_view(request):
    return render(request, 'specific_pages/files.html')

@login_required
def schedule_meets_view(request):
    return render(request, 'specific_pages//schedule_meets.html')
