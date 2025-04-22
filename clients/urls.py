from django.urls import path 
from . import views
from .views import ClientDeleteView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, export_clients_to_excel

app_name = "clients"

urlpatterns = [
    path('', ClientListView.as_view(), name='client-list'),
    path("export-excel/", export_clients_to_excel, name="client-export-excel"),
     path("upload-clients/", views.upload_clients, name="upload-clients"),
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    path('create/', ClientCreateView.as_view(), name='client-create'),
]