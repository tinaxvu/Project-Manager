from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
import datetime
import json

from .models import Project, Calendar
from .forms import ProjectForm, FileUploadForm
from .utils import get_signed_url
from django.contrib.auth.decorators import login_required, user_passes_test



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

############ Joining Project ############
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

@login_required
def cancel_request(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if user in user.projects_requested_by_users.all():
        project.requested.remove(user)
        return JsonResponse({'success': True, 'action': 'canceled'})
    return redirect('projects:project-detail', project_id=project_id)

############ Calendar ############
@login_required
def calendar_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'specific_pages/calendar.html', {'project': project})


def fetch_events(request, project_id):
    print("Fetching events...")  # Debug print statement
    project = get_object_or_404(Project, id=project_id)
    events = Calendar.objects.filter(project=project)
    events_data = [
        {
            "id": event.id,
            "title": event.title,
            "start": event.event_date.isoformat(),
            "description": event.description
        }
        for event in events
    ]
    return JsonResponse(events_data, safe=False)


def add_event(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description")
        event_date_str = data.get("date")
        if not title or not event_date_str:
            return JsonResponse({"success": False, "error": "Title and date are required."}, status=400)

        event_date = timezone.make_aware(datetime.datetime.strptime(event_date_str, "%Y-%m-%d"))

        event = Calendar.objects.create(
            title=title,
            description=description,
            event_date=event_date,
            created_by=request.user,
            project=project
        )
        return JsonResponse({"id": event.id})



@csrf_exempt
def delete_event(request, event_id):
    if request.method == "DELETE":
        event = get_object_or_404(Calendar, id=event_id)
        if event.created_by == request.user:
            event.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Permission denied."})


@login_required
def team_handbook_view(request):
    return render(request, 'specific_pages/team_handbook.html')

############ Collaboration ############
@login_required
def collaboration_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.created_by == request.user:
        return render(request, 'specific_pages/collaboration.html', {'project': project})
    else:
        return redirect('projects:project-detail', project_id=project.id)

@login_required
def approve_request(request, project_id, user_id):
    User = get_user_model()
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)

    # Check if the current user is the project creator
    if request.user == project.created_by:
        # Ensure user is in the requested list before approving
        if user in project.requested.all():
            project.requested.remove(user)  # Remove from requested
            project.members.add(user)       # Add to members

    # Refresh the page
    return redirect('projects:collaboration', project_id=project_id)

@login_required
def deny_request(request, project_id, user_id):
    User = get_user_model()
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)

    # Check if the current user is the project creator
    if request.user == project.created_by:
        # Ensure user is in the requested list before denying
        if user in project.requested.all():
            project.requested.remove(user)  # Remove from requested list

    # Refresh the page
    return redirect('projects:collaboration', project_id=project_id)


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