from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm, FileUploadForm
from .utils import get_signed_url
from django.contrib.auth.decorators import login_required


@login_required
def project_files(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    files = project.files.all()  # Access related files

    # Generate signed URLs for the files
    signed_urls = {file: get_signed_url(file) for file in files}

    if request.method == 'POST':
        # Check if the user is a member or the owner
        if project.created_by == request.user or project.members.filter(id=request.user.id).exists():
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                # Save the file and associate it with the project
                file_upload = form.save(commit=False)
                file_upload.project = project  # Associate the uploaded file with the project
                file_upload.uploaded_by = request.user  # Associate the uploader with the file
                file_upload.save()
                return redirect('projects:project_files', project_id=project.id)  # Redirect to the same page after upload
        else:
            # Handle unauthorized access
            return redirect('projects:project-detail', project_id=project.id)

    context = {
        'project': project,
        'files': signed_urls,  # Pass signed URLs to the template
    }
    return render(request, 'specific_pages/files.html', context)


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user  # Associate the project with the logged-in user
            project.save()
            return redirect('/')  # Replace 'project_list' with the appropriate URL
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)  # Fetch the project by ID

    # Check if the current user is the owner or a member
    if project.created_by == request.user:
        # If the user is the owner, render the collaboration options
        return render(request, 'project_detail.html', {'project': project})
    elif project.members.filter(id=request.user.id).exists():
        # If the user is a member, also render the collaboration options
        return render(request, 'project_detail.html', {'project': project})
    else:
        # If the user is not a member, they should see the option to request to join
        return render(request, 'specific_pages/request_to_join.html', {'project': project})


@login_required
def request_to_join(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if user not in project.members.all():
        user.requested_projects.add(project)
        return redirect('projects:project-detail',
                        project_id=project_id)  # Redirect to project detail after requesting to join
    return redirect('projects:project-detail', project_id=project_id)  # Ensure there's always a redirect


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
        return redirect('projects:project-detail', project_id=project.id)  # Redirect if not owner


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
