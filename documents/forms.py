from django import forms
from .models import Document, Folder

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['folder', 'file']
