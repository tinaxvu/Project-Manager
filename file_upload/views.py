from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from django.core.files.storage import default_storage
from django.http import HttpResponseForbidden
from .models import Project, FileUpload


@login_required
def user_projects(request):
    projects = request.user.projects.all()  # Get all projects associated with the user
    return render(request, 'file_upload/user_projects.html', {'projects': projects})


@login_required
def project_files(request, project_id):
    # Fetch the project by id and check if the user is a member
    project = Project.objects.filter(id=project_id, members=request.user).first()
    if project:
        files = project.files.all()
        return render(request, 'file_upload/project_files.html', {'project': project, 'files': files})
    else:
        return HttpResponseForbidden("You do not have access to this project.")


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']  # Get the file from the form
            project_id = request.POST.get('project_id')  # Get the associated project ID
            project = Project.objects.get(id=project_id)  # Get the project

            # Create the FileUpload instance and associate it with the project
            file_upload = FileUpload.objects.create(project=project, file=file)

            return HttpResponse(
                f"File uploaded successfully: <a href='{file_upload.file.url}'>{file_upload.file.url}</a>")
    else:
        form = FileUploadForm()

        # Pass user's projects to the template
    user_projects = request.user.projects.all()
    return render(request, 'file_upload.html', {'form': form})
