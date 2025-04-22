from django.urls import path
from . import views
from .views import document_list, create_folder, upload_document, download_document, delete_document
from django.conf.urls.static import static
from django.conf import settings

app_name = "documents"

urlpatterns = [
    path('', document_list, name='document_list'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('upload/', upload_document, name='upload_document'),
    path('download/<int:document_id>/', download_document, name='download_document'),
    path('delete/<int:document_id>/', delete_document, name='delete_document'),
    path('documents/<str:filename>/', views.serve_document, name='serve_document'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

