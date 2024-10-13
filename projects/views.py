from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user  # Associate the project with the logged-in user
            project.save()
            return redirect('/')  # Replace 'project_list' with the appropriate URL
    else:
        form = ProjectForm()
    
    return render(request, 'create_project.html', {'form': form})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)  # Fetch the project by ID
    return render(request, 'project_detail.html', {'project': project})


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
