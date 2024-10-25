from django import forms
from .models import Project
from .models import FileUpload


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file', 'file_title', 'description', 'keywords']
        widgets = {
            'keywords': forms.TextInput(attrs={'placeholder': 'e.g., Minutes, Event Planning, Map'})
        }
