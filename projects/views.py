import datetime
import json
import boto3
import traceback

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Project, Tag, Message, Thread, FileUpload, Calendar, Todo, ScheduleMeet
from .forms import ProjectForm, FileUploadForm, MessageForm, ThreadForm
from .utils import get_signed_url

User = get_user_model()


@login_required
def project_files(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    selected_tags = request.GET.getlist('tags')

    if request.method == 'POST':
        if project.created_by == request.user or project.members.filter(id=request.user.id).exists():
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_upload = form.save(commit=False)
                file_upload.project = project
                file_upload.uploaded_by = request.user
                file_upload.save()

                # Parse keywords and create/associate tags
                keywords = form.cleaned_data['keywords']
                if keywords:
                    tags = [tag.strip() for tag in keywords.split(',')]
                    for tag_name in tags:
                        tag, created = Tag.objects.get_or_create(name=tag_name, project=project)
                        file_upload.tags.add(tag)

                form.save_m2m()
                return redirect('projects:project_files', project_id=project.id)
    else:
        form = FileUploadForm()

    # Current behavior is to just take all files if they have ANY of the selected tags.
    if selected_tags:
        files = project.files.filter(tags__name__in=selected_tags).distinct()
    else:
        files = project.files.all()

    signed_urls = {file: get_signed_url(file) for file in files}
    tags = Tag.objects.filter(project=project).distinct()

    context = {
        'project': project,
        'files': signed_urls,
        'tags': tags,
        'selected_tags': selected_tags,
        'form': form,
    }
    return render(request, 'specific_pages/files.html', context)


@login_required
def view_file(request, project_id, file_id):
    project = get_object_or_404(Project, id=project_id)
    file_upload = get_object_or_404(FileUpload, id=file_id, project=project)

    # Get the signed URL for displaying the file (so that the file is securely accessed from AWS)
    file_url = get_signed_url(file_upload)
    # If file is hosted on AWS S3
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_S3_REGION_NAME)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    file_key = file_upload.file.name  # This is the path to the file in S3

    # Get the text file content if it is a txt file
    if '.txt' in file_key:
        file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = file_obj['Body'].read().decode('utf-8')  # Decode as utf-8 text
    else:
        file_content = ''
    context = {
        'project': project,
        'file': file_upload,
        'file_url': file_url,
        'file_content': file_content
    }
    return render(request, 'specific_pages/file.html', context)


@login_required
def delete_file(request, project_id, file_id):
    project = get_object_or_404(Project, id=project_id)
    file_to_delete = get_object_or_404(project.files.all(), id=file_id)

    file_to_delete.delete()
    return redirect('projects:project_files', project_id=project_id)


@login_required
def files_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'specific_pages/files.html', {'project': project})


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

    # Check if the user has already requested to join the project
    if not project.requested.filter(id=user.id).exists():
        project.requested.add(user)
        return JsonResponse({'success': True, 'requested': True})
    else:
        return JsonResponse(
            {'success': False, 'requested': True, 'message': 'You have already requested to join this project.'})


@login_required
def leave_project(request, project_id):
    user = request.user
    project = get_object_or_404(Project, id=project_id)
    project.members.remove(user)
    project.requested.remove(user)
    return redirect('landing_page')


@login_required
def approve_request(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)

    if request.user == project.created_by:
        user.requested_projects.remove(project)
        project.members.add(user)
        project.requested.remove(user)

    return redirect('projects:project-detail', project_id=project_id)


@login_required
def deny_request(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)

    if request.user == project.created_by:
        user.requested_projects.remove(project)
        project.requested.remove(user)

    return redirect('projects:project-detail', project_id=project_id)


############ Calendar ############
@login_required
def calendar_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'specific_pages/calendar.html', {'project': project})


def fetch_events(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    events = Calendar.objects.filter(project=project)
    events_data = [
        {
            "id": event.id,
            "title": event.title,
            "start": event.event_date.isoformat(),
            "end": event.end_date.isoformat() if event.end_date else None,
            "description": event.description,
            "type": event.type
        }
        for event in events
    ]
    return JsonResponse(events_data, safe=False)


def add_event(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        if request.method == "POST":
            data = json.loads(request.body)
            title = data.get("title")
            description = data.get("description")
            start_date_str = data.get("start_date")
            end_date_str = data.get("end_date")
            type = data.get("type")

            if not title or not start_date_str or not end_date_str:
                return JsonResponse({"success": False, "error": "Title and date are required."}, status=400)

            start_date = timezone.make_aware(datetime.datetime.fromisoformat(start_date_str), timezone.utc)
            end_date = timezone.make_aware(datetime.datetime.fromisoformat(end_date_str), timezone.utc)

            event = Calendar.objects.create(
                title=title,
                description=description,
                event_date=start_date,
                end_date=end_date,
                created_by=request.user,
                project=project,
                type=type
            )
            return JsonResponse({"id": event.id})
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"success": False, "error": "An unexpected error occurred."}, status=500)


def delete_event(request, event_id):
    if request.method == "DELETE":
        event = get_object_or_404(Calendar, id=event_id)
        if event.created_by == request.user:
            event.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Permission denied."})


@login_required
def collaboration_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.created_by == request.user:
        return render(request, 'specific_pages/collaboration.html', {'project': project})
    else:
        return redirect('projects:project-detail', project_id=project.id)


@login_required
def todos_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        # Process the form data
        description = request.POST.get('description')
        date_due = request.POST.get('date_due')
        priority = request.POST.get('priority')
        assigned_to = request.POST.getlist('assigned_to')
        is_finished = request.POST.get('is_finished', 'off') == 'on'

        # Assuming there's a project_id in the session or a similar way to determine the project
        # project_id = request.session.get('current_project_id')
  

        # Create a new Todo instance
        todo = Todo(project=project, description=description, date_due=date_due, priority=priority,
                    is_finished=is_finished, created_by=request.user)
        todo.save()

        # Assign users to the todo
        for user_id in assigned_to:
            user = get_object_or_404(User, id=user_id)
            todo.assigned_to.add(user)
        return redirect('projects:todos', project_id=project_id)

    users = User.objects.all()
    todos = Todo.objects.filter(project=project_id)
    return render(request, 'specific_pages/todos.html', {'users': users, 'todos': todos, 'project_id': project_id, 'project': project})


@login_required
def todo_detail(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    return render(request, 'specific_pages/todo_detail.html', {'todo': todo})


@login_required
def toggle_todo_complete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_finished = not todo.is_finished
    todo.save()
    return redirect('projects:todos', project_id=todo.project.id)


def toggle_todo_complete_detail(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_finished = not todo.is_finished
    todo.save()
    return redirect('projects:todo-detail', todo_id=todo.id)


@login_required
def schedule_meets_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    schedule_meets = ScheduleMeet.objects.filter(project=project)
    return render(request, 'specific_pages/schedule_meets.html',
                  {'project': project, 'schedule_meets': schedule_meets, 'project_id': project_id})


@login_required
def delete_meet(request, project_id, meeting_id):
    meet = get_object_or_404(ScheduleMeet, id=meeting_id)
    meet.delete()
    return redirect('projects:schedule-meets', project_id=project_id)


@login_required
def make_meets(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description')
        title = request.POST.get('title')
        meeting_date = request.POST.get('meeting_date')

        if start_time >= end_time:
            messages.error(request, "Start time must be before end time.")
            return redirect('projects:schedule-meets', project_id=project_id)
        
        if len(title) > 200:
            messages.error(request, "Title must be less than 200 characters.")
            return redirect('projects:schedule-meets', project_id=project_id)

        meeting = ScheduleMeet(project=project, start_time=start_time, end_time=end_time, description=description,
                               title=title, meeting_date=meeting_date)
        meeting.save()

        return redirect('projects:schedule-meets', project_id=project_id)

    schedule_meets = ScheduleMeet.objects.filter(project=project)

    return render(request, 'projects/schedule_meets.html',
                  {'project': project, 'schedule_meets': schedule_meets, 'project_id': project_id})


@login_required
def message_board_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    message_form = MessageForm()
    thread_form = ThreadForm()
    if request.method == 'POST':
        if 'message_form' in request.POST:
            thread_id = request.POST.get('thread_id')
            thread = get_object_or_404(Thread, id=thread_id)
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.project = project
                message.posted_by = request.user
                message.thread = thread
                message.save()
                return redirect('projects:message_board', project_id=project.id)
        elif 'thread_form' in request.POST:
            thread_form = ThreadForm(request.POST)
            if thread_form.is_valid():
                thread = thread_form.save(commit=False)
                thread.project = project
                thread.posted_by = request.user
                thread.save()
                return redirect('projects:message_board', project_id=project.id)
    messages = project.message.all()
    threads = project.thread.all()
    threads_with_messages = {}
    for thread in threads:
        has_message = any(message.thread.id == thread.id for message in messages)
        threads_with_messages[thread.id] = has_message
    print(threads_with_messages)
    context = {
        'project': project,
        'thread_form': thread_form,
        'message_form': message_form,
        'messages': messages,
        'threads': threads,
        'threads_with_messages': threads_with_messages
    }
    return render(request, 'specific_pages/message_board.html', context)


@login_required
def delete_message(request, project_id, message_id):
    project = get_object_or_404(Project, id=project_id)
    message = get_object_or_404(Message, id=message_id)
    if request.user.permission_level == 'admin' or message.posted_by == request.user:
        message.delete()
        return redirect('projects:message_board', project_id=project_id)


@login_required
def pin_thread(request, project_id, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.pinned = True
    thread.save()
    return redirect('projects:message_board', project_id=project_id)


@login_required
def unpin_thread(request, project_id, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.pinned = False
    thread.save()
    return redirect('projects:message_board', project_id=project_id)


@login_required
def delete_thread(request, project_id, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user.permission_level == 'admin' or thread.posted_by == request.user:
        thread.delete()
        return redirect('projects:message_board', project_id=project_id)


@require_POST
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.permission_level == 'admin' or project.owner == request.user:
        project.delete()
        return redirect('/')

    return JsonResponse({'success': False, 'error': 'You do not have permission to delete this project.'}, status=403)


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    project.delete()
    return redirect('/')


@login_required
def delete_todo(request, project_id, todo_id):
    project = get_object_or_404(Project, id=project_id)
    todo_to_delete = get_object_or_404(project.todos.all(), id=todo_id)

    todo_to_delete.delete()
    return redirect('projects:todos', project_id=project_id)
