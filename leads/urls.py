
from django.urls import path 
from . import views
from .views import LeadDeleteView, LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, export_leads_to_excel, DashboardView

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('convert-lead/<int:lead_id>/', views.convert_lead_to_client, name='convert-lead'),  # Conversion URL
    path("export-excel/", export_leads_to_excel, name="export-excel"),
    path("upload-leads/", views.upload_leads, name="upload-leads"),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]