# projects/context_processors.py
from .models import Project


def project_context(request):
    if request.user.is_authenticated:
        user_projects = Project.objects.filter(created_by=request.user)
        joined_projects = request.user.member_projects.exclude(created_by=request.user)
        return {
            'user_projects': user_projects,
            'joined_projects': joined_projects,
        }
    return {}
