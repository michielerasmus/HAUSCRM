from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from .models import Folder, Document

@receiver(post_migrate)
def create_permissions(sender, **kwargs):
    if sender.name == "documents":
        organiser_group, created = Group.objects.get_or_create(name="Organiser")

        folder_ct = ContentType.objects.get_for_model(Folder)
        document_ct = ContentType.objects.get_for_model(Document)

        permissions = [
            ("add_folder", "Can add folder"),
            ("change_folder", "Can change folder"),
            ("delete_folder", "Can delete folder"),
            ("add_document", "Can add document"),
            ("change_document", "Can change document"),
            ("delete_document", "Can delete document"),
        ]

        for codename, name in permissions:
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=folder_ct if "folder" in codename else document_ct
            )
            organiser_group.permissions.add(perm)
