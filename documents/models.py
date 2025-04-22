from django.conf import settings
from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Define custom permissions with different names
    class Meta:
        permissions = [
            ('custom_add_folder', 'Can add folder'),
            ('custom_change_folder', 'Can change folder'),
            ('custom_delete_folder', 'Can delete folder'),
        ]

    def __str__(self):
        return self.name

class Document(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Define custom permissions with different names
    class Meta:
        permissions = [
            ('custom_add_document', 'Can add document'),
            ('custom_change_document', 'Can change document'),
            ('custom_delete_document', 'Can delete document'),
        ]

    def __str__(self):
        return self.file.name
