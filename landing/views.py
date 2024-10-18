# landing/views.py
from django.shortcuts import render
from projects.models import Project

def landing_page(request):
    if request.user.is_authenticated:
        user_projects = Project.objects.filter(created_by=request.user)

        all_projects = Project.objects.exclude(created_by=request.user)

        return render(request, 'landing/index.html', {
            'user_projects': user_projects,
            'all_projects': all_projects
        })
    else:
        return render(request, 'landing/index.html')