from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Project
from .forms import ProjectForm, FileUploadForm
from .utils import get_signed_url
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse


@login_required
def project_files(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    files = project.files.all()

    signed_urls = {file: get_signed_url(file) for file in files}

    if request.method == 'POST':
        if project.created_by == request.user or project.members.filter(id=request.user.id).exists():
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_upload = form.save(commit=False)
                file_upload.project = project
                file_upload.uploaded_by = request.user
                file_upload.save()
                return redirect('projects:project_files', project_id=project.id)
        else:
            return redirect('projects:project-detail', project_id=project.id)

    context = {
        'project': project,
        'files': signed_urls,
    }
    return render(request, 'specific_pages/files.html', context)


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('/')
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.created_by == request.user or request.user.permission_level == 'admin':
        return render(request, 'project_detail.html', {'project': project})
    elif project.members.filter(id=request.user.id).exists():
        return render(request, 'project_detail.html', {'project': project})
    else:
        return render(request, 'specific_pages/request_to_join.html', {'project': project})


@login_required
def request_to_join(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    # Check if the user has already requested to join
    if project not in user.projects_requested_by_users.all():
        project.requested.add(user)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Already requested'})


def approve_request(request, project_id, user_id):
    User = get_user_model()
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)

    if request.user == project.created_by:
        user.requested_projects.remove(project)
        project.members.add(user)
    return redirect('projects:project-detail', project_id=project_id)


def deny_request(request, project_id, user_id):
    User = get_user_model()
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)

    if request.user == project.created_by:
        user.requested_projects.remove(project)
        project.denied.add(user)

    return redirect('projects:project-detail', project_id=project_id)


@login_required
def calendar_view(request):
    return render(request, 'specific_pages/calendar.html')


@login_required
def team_handbook_view(request):
    return render(request, 'specific_pages/team_handbook.html')


@login_required
def collaboration_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.created_by == request.user:
        return render(request, 'specific_pages/collaboration.html', {'project': project})
    else:
        return redirect('projects:project-detail', project_id=project.id)


@login_required
def todos_view(request):
    return render(request, 'specific_pages/todos.html')


@login_required
def timeline_view(request):
    return render(request, 'specific_pages/timeline.html')


@login_required
def files_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'specific_pages/files.html', {'project': project})


@login_required
def schedule_meets_view(request):
    return render(request, 'specific_pages//schedule_meets.html')


@require_POST
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Check if the user is an admin or the owner of the project
    if request.user.permission_level == 'admin' or project.owner == request.user:
        project.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'You do not have permission to delete this project.'}, status=403)


@login_required
def delete_file(request, project_id, file_id):
    project = get_object_or_404(Project, id=project_id)
    file_to_delete = get_object_or_404(project.files.all(), id=file_id)

    if request.user.permission_level == 'admin':
        file_to_delete.delete()
        return redirect('projects:project_files', project_id=project_id)
    else:
        return redirect('projects:project-detail', project_id=project_id)
