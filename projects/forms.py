from django import forms
from .models import Project, FileUpload, Tag

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class FileUploadForm(forms.ModelForm):
    tag_names = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas (e.g., Minutes, Planning)"
    )

    class Meta:
        model = FileUpload
        fields = ['file', 'file_title', 'description', 'keywords', 'tag_names']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True, project=None):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if project:
            tag_names = self.cleaned_data.get('tag_names')
            if tag_names:
                tag_list = [name.strip() for name in tag_names.split(',')]
                for tag_name in tag_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name, project=project)
                    instance.tags.add(tag)
        return instance
