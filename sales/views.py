import openpyxl
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Sale
from .forms import SaleModelForm

class SaleListView(LoginRequiredMixin, generic.ListView):
    template_name = "sales/sale_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        queryset = Sale.objects.all()

        # Restrict to agent's sales if user is an agent
        if self.request.user.is_agent:
            queryset = queryset.filter(agent__user=self.request.user)

        # Search and filter
        search_query = self.request.GET.get("search", "")
        status_filter = self.request.GET.get("status", "")

        if search_query:
            queryset = queryset.filter(
                Q(address__icontains=search_query) |
                Q(seller_1__name__icontains=search_query) |
                Q(seller_2__name__icontains=search_query) |
                Q(buyer_1__name__icontains=search_query) |
                Q(buyer_2__name__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by("address")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_sales = self.get_queryset()

        # Categorize sales for better UI grouping
        context["for_sale_sales"] = all_sales.exclude(status__in=["Deal Won", "Deal Lost"])
        context["sold_sales"] = all_sales.filter(status="Deal Won")
        context["lost_sales"] = all_sales.filter(status="Deal Lost")

        return context


def export_sales_to_excel(request):
    """Generate an Excel file containing all sales"""
    sales = Sale.objects.all()

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="sales.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Sales"

    # Define headers
    headers = [
        "Address", "Area", "City", "Status", "Property Type", "Mandate Type", 
        "Listing Price", "Commission", "Sale Price", "Seller 1", "Seller 2", 
        "Buyer 1", "Buyer 2", "Days On Market", "Price Drop", "Agent"
    ]
    worksheet.append(headers)

    # Write sale data
    for sale in sales:
        agent_username = sale.agent.user.username if sale.agent and sale.agent.user else "Unassigned"

        worksheet.append([
            sale.address,
            sale.area,
            sale.city,
            sale.status,
            sale.property_type,
            sale.mandate_type,
            sale.listing_price,
            sale.commission_percentage,
            sale.sale_price,
            sale.seller_1.name if sale.seller_1 else "",
            sale.seller_2.name if sale.seller_2 else "",
            sale.buyer_1.name if sale.buyer_1 else "",
            sale.buyer_2.name if sale.buyer_2 else "",
            sale.days_on_market() if hasattr(sale, 'days_on_market') else "N/A",
            sale.price_drop_percentage() if hasattr(sale, 'price_drop_percentage') else "N/A",
            agent_username,  # Add the agent's username (if available)
        ])

    workbook.save(response)
    return response


class SaleDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "sales/sale_detail.html"
    queryset = Sale.objects.all()
    context_object_name = "sale"

class SaleCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "sales/sale_create.html"
    form_class = SaleModelForm

    def get_success_url(self):
        return reverse("sales:sale-list")

class SaleUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "sales/sale_update.html"
    queryset = Sale.objects.all()
    form_class = SaleModelForm

    def get_success_url(self):
        return reverse("sales:sale-detail", kwargs={"pk": self.object.pk})

class SaleDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name= "sales/sale_delete.html"
    queryset = Sale.objects.all()

    def get_success_url(self):
        return reverse("sales:sale-list")
