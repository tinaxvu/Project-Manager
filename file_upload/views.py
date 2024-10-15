from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from django.core.files.storage import default_storage

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = default_storage.save(file.name, file)
            file_url = default_storage.url(file_name)
            return HttpResponse(f"File uploaded successfully: <a href='{file_url}'>{file_url}</a>")
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
