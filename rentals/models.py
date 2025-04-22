from django.db import models
from datetime import date
from django.utils import timezone
from leads.models import Agent 
from clients.models import Client 

class Rental(models.Model): 

    PROPERTY_TYPE_CHOICES = (
        ('Commercial', 'Commercial'),
        ('Farm', 'Farm'),
        ('Residential', 'Residential'),
    )

    MANDATE_TYPE_CHOICES = ( 
        ('Management', 'Management'), 
        ('Placement', 'Placement'),
        ('Management and Placement', 'Management and Placement'),
    )

    STATUS_CHOICES = (
        ('New Mandate', 'New Mandate'),
        ('Tenant Application', 'Tenant Application'),
        ('Tenant Placed', 'Tenant Placed'),
        ('Managing', 'Managing'),
        ('Deal Lost', 'Deal Lost'),
        ('Closed', 'Closed'),
    )
    RENTAL_TYPE_CHOICES = ( 
        ('Long-Term', 'Long-Term'), 
        ('Short-Term', 'Short-Term'),
        ('Holiday', 'Holiday'),
    )

    # Fields
    status = models.CharField(choices=STATUS_CHOICES, max_length=50)
    address = models.CharField(max_length=255)  
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    property_type = models.CharField(choices=PROPERTY_TYPE_CHOICES, max_length=50)
    mandate_type = models.CharField(choices=MANDATE_TYPE_CHOICES, max_length=50)
    rental_type = models.CharField(choices=RENTAL_TYPE_CHOICES, max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 
    follow_up_date = models.DateField(null=True, blank=True)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    placement_commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    management_commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_listed = models.DateField(default=timezone.now)
    mandate_expiry = models.DateField(default=date.today().strftime('%Y/%m/%d'))
    date_rented = models.DateField(blank=True, null=True)
    rental_expiry = models.DateField(default=date.today().strftime('%Y/%m/%d'))

    # Tenants and Landlords (linked to the Client model)
    landlord_1 = models.ForeignKey(Client, related_name='landlord_1', on_delete=models.SET_NULL, null=True, blank=True)
    landlord_2 = models.ForeignKey(Client, related_name='landlord_2', on_delete=models.SET_NULL, null=True, blank=True)
    tenant_1 = models.ForeignKey(Client, related_name='tenant_1', on_delete=models.SET_NULL, null=True, blank=True)
    tenant_2 = models.ForeignKey(Client, related_name='tenant_2', on_delete=models.SET_NULL, null=True, blank=True)

    # Methods
    def days_on_market(self):
        if not self.date_listed:
            return 0  # Default to 0 if listing date is missing

        end_date = self.date_rented if self.date_rented else timezone.localdate()
        return (end_date - self.date_listed).days

    def price_drop_percentage(self):
        if self.listing_price and self.rental_price:
            drop = (self.listing_price - self.rental_price) / self.listing_price * 100
            return drop
        return 0.0

    def __str__(self):
        return f"Property {self.id} - {self.listing_price} (Listing Price), {self.rental_price} (Rental Price)"

    class Meta:
        verbose_name = "Rental"
        verbose_name_plural = "Rentals"
