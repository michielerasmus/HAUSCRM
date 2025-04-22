from django.urls import path 
from .views import SaleDeleteView, SaleListView, SaleDetailView, SaleCreateView, SaleUpdateView, export_sales_to_excel

app_name = "sales"

urlpatterns = [
    path('', SaleListView.as_view(), name='sale-list'),
    path("export-excel/", export_sales_to_excel, name="sale-export-excel"),
    path('<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('<int:pk>/update/', SaleUpdateView.as_view(), name='sale-update'),
    path('<int:pk>/delete/', SaleDeleteView.as_view(), name='sale-delete'),
    path('create/', SaleCreateView.as_view(), name='sale-create'),
]