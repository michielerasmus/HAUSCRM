from django.urls import path 
from .views import RentalDeleteView, RentalListView, RentalDetailView, RentalCreateView, RentalUpdateView, export_rentals_to_excel

app_name = "sales"

urlpatterns = [
    path('', RentalListView.as_view(), name='rental-list'),
    path("export-excel/", export_rentals_to_excel, name="rental-export-excel"),
    path('<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
    path('<int:pk>/update/', RentalUpdateView.as_view(), name='rental-update'),
    path('<int:pk>/delete/', RentalDeleteView.as_view(), name='rental-delete'),
    path('create/', RentalCreateView.as_view(), name='rental-create'),
]