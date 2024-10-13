# landing/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project

def landing_page(request):
    if request.user.is_authenticated:
        user = request.user
        user_email = user.email  # Get the logged-in user's email
        user_groups = user.groups.all()
        projects = Project.objects.filter(owner=user)
        return render(request, 'landing/index.html', {'email': user_email, 'groups': user_groups, 'projects': projects})
    else:
        return render(request, 'landing/index.html', {'error': 'You are not logged in.'})
