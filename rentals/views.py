import openpyxl
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Rental
from .forms import RentalModelForm
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # Import relativedelta

class RentalListView(LoginRequiredMixin, generic.ListView):
    template_name = "rentals/rental_list.html"
    context_object_name = "rentals"

    def get_queryset(self):
        queryset = Rental.objects.all()

        # Restrict to agent's rentals if user is an agent
        if self.request.user.is_agent:
            queryset = queryset.filter(agent__user=self.request.user)

        # Search and filter
        search_query = self.request.GET.get("search", "")
        status_filter = self.request.GET.get("status", "")

        if search_query:
            queryset = queryset.filter(
                Q(address__icontains=search_query) |
                Q(landlord_1__name__icontains=search_query) |
                Q(landlord_2__name__icontains=search_query) |
                Q(tenant_1__name__icontains=search_query) |
                Q(tenant_2__name__icontains=search_query) |
                Q(rental_type__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by("address")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_rentals = self.get_queryset()

        # Categorize rentals
        context["for_rental_rentals"] = all_rentals.exclude(status__in=["Managing", "Tenant Placed", "Closed", "Deal Lost"])
        context["managing_rentals"] = all_rentals.filter(status="Managing")
        context["closed_rentals"] = all_rentals.filter(status="Closed")
        context["lost_rentals"] = all_rentals.filter(status="Deal Lost")

        # Calculate expiring mandates and rentals
        today = timezone.now().date()
        next_month = today + relativedelta(months=+1)
        context["expiring_mandates"] = all_rentals.filter(
            mandate_expiry__gte=today, mandate_expiry__lte=next_month
        ).order_by('mandate_expiry')
        context["expiring_rentals"] = all_rentals.filter(
            rental_expiry__gte=today, rental_expiry__lte=next_month
        ).order_by('rental_expiry')

        # Rentals expiring within the next 30 days
        thirty_days_from_today = today + relativedelta(days=+30)
        context["expiring_rentals_soon"] = all_rentals.filter(
            rental_expiry__gte=today, rental_expiry__lte=thirty_days_from_today
        ).order_by('rental_expiry')

        return context



def export_rentals_to_excel(request):
    """Generate an Excel file containing all rentals"""
    rentals = Rental.objects.all()

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="rentals.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Rentals"

    # Define headers
    headers = [
        "Address", "Area", "City", "Status", "Property Type", "Mandate Type", "Rental Type",
        "Listing Price", "Placement Commission", "Management Commission", "Rental", "Landlord 1", "Landlord 2",
        "Tenant 1", "Tenant 2", "Date Listed", "Date Rented", "Days On Market", "Price Drop", "Agent"
    ]
    worksheet.append(headers)

    # Write rental data
    for rental in rentals:
        # Debugging lines to check if agent is assigned
        if rental.agent:
            print(f"Agent for {rental.address}: {rental.agent.user.username}")  # Showing username here
        else:
            print(f"No agent assigned for {rental.address}")

        agent_username = "Unassigned"  # Default to "Unassigned" if no agent
        if rental.agent and rental.agent.user:
            agent_username = rental.agent.user.username  # Use agent's username

        worksheet.append([
            rental.address,
            rental.area,
            rental.city,
            rental.status,
            rental.property_type,
            rental.mandate_type,
            rental.rental_type,
            rental.listing_price,
            rental.placement_commission_percentage,
            rental.management_commission_percentage,
            rental.rental_price,
            rental.landlord_1.name if rental.landlord_1 else "",
            rental.landlord_2.name if rental.landlord_2 else "",
            rental.tenant_1.name if rental.tenant_1 else "",
            rental.tenant_2.name if rental.tenant_2 else "",
            rental.date_listed,
            rental.date_rented,
            rental.days_on_market(),
            rental.price_drop_percentage(),
            agent_username,  # Add the agent's name (if available)
        ])

    workbook.save(response)
    return response


class RentalDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "rentals/rental_detail.html"
    queryset = Rental.objects.all()
    context_object_name = "rental"


class RentalCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "rentals/rental_create.html"
    form_class = RentalModelForm

    def get_success_url(self):
        return reverse("rentals:rental-list")


class RentalUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "rentals/rental_update.html"
    queryset = Rental.objects.all()
    form_class = RentalModelForm

    def get_success_url(self):
        return reverse("rentals:rental-detail", kwargs={"pk": self.object.pk})


class RentalDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "rentals/rental_delete.html"
    queryset = Rental.objects.all()

    def get_success_url(self):
        return reverse("rentals:rental-list")