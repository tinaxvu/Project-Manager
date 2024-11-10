# landing/views.py
from django.shortcuts import render
from projects.models import Project

def landing_page(request):
    if request.user.is_authenticated:
        # Projects created by the user
        user_projects = Project.objects.filter(created_by=request.user)

        # Projects the user is a member of, excluding those they created
        joined_projects = request.user.member_projects.exclude(created_by=request.user)

        # All projects excluding those created by the user and those they are members of
        all_projects = Project.objects.exclude(created_by=request.user).exclude(
            id__in=joined_projects.values_list('id', flat=True))

        # All projects the user requested
        requested_projects = request.user.projects_requested_by_users.all()

        context = {
            'user_projects': user_projects,
            'joined_projects': joined_projects,
            'all_projects': all_projects,
            'requested_projects': requested_projects,
        }

        return render(request, 'landing/index.html', context)
    else:
        all_projects = Project.objects.all()
        context = { 
            'all_projects': all_projects
        }
        return render(request, 'landing/index.html', context)
