from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Folder, Document
from .forms import FolderForm, DocumentForm
from django.contrib.auth.models import Permission
from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404
import os
import re

def serve_document(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'documents', filename)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={filename}'
            return response
    else:
        raise Http404("Document not found")

@login_required
def assign_permissions(request):
    user = request.user  # Get the logged-in user

    # Assign 'add_folder' permission to the user (replace with the actual codename)
    permission = Permission.objects.get(codename='add_folder')
    user.user_permissions.add(permission)

    return render(request, 'some_template.html')

@login_required
def document_list(request):
    folders = Folder.objects.all().order_by('name')
    documents = Document.objects.all()

    def get_sort_key(document):
        file_name = os.path.basename(document.file.name)
        file_name = file_name.replace("documents/", "")  # Remove "documents/" if it exists.
        return re.sub(r'[^\w\.]', '', file_name).lower()

    documents = sorted(documents, key=get_sort_key)

    can_add_folder = request.user.has_perm('documents:create_folder')
    can_delete_document = request.user.has_perm('documents:delete_document')

    return render(request, 'documents/document_list.html', {
        'folders': folders,
        'documents': documents,
        'can_add_folder': can_add_folder,
        'can_delete_document': can_delete_document,
    })

@permission_required('documents.add_folder', raise_exception=True)
def create_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('documents:document_list')
    else:
        form = FolderForm()
    return render(request, 'documents/create_folder.html', {'form': form})

@permission_required('documents.add_document', raise_exception=True)
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect('documents:document_list')
    else:
        form = DocumentForm()
    return render(request, 'documents/upload_document.html', {'form': form})

@login_required
def download_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return redirect(document.file.url)

@permission_required('documents.delete_document', raise_exception=True)
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.file.delete()
    document.delete()
    return redirect('documents:document_list')