from django.urls import path 
from .views import TrackerDeleteView, TrackerListView, TrackerCreateView, TrackerUpdateView

app_name = "clients"

urlpatterns = [
    path('', TrackerListView.as_view(), name='tracker-list'),
    path('<int:pk>/update/', TrackerUpdateView.as_view(), name='tracker-update'),
    path('<int:pk>/delete/', TrackerDeleteView.as_view(), name='tracker-delete'),
    path('create/', TrackerCreateView.as_view(), name='tracker-create'),
]