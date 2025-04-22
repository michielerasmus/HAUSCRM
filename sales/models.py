from django.db import models
from datetime import date
from django.utils import timezone
from leads.models import Agent 
from clients.models import Client  

class Sale(models.Model): 

    PROPERTY_TYPE_CHOICES = (
        ('Commercial', 'Commercial'),
        ('Farm', 'Farm'),
        ('Residential', 'Residential'),
        ('Vacant Land', 'Vacant Land'),
    )

    MANDATE_TYPE_CHOICES = ( 
        ('Dual / Joint', 'Dual / Joint'), 
        ('Exclusive Sole', 'Exclusive Sole'),
        ('Open', 'Open'),
        ('Sole', 'Sole'),
    )

    STATUS_CHOICES = (
        ('New Mandate', 'New Mandate'),
        ('Offer', 'Offer'),
        ('Negotiation', 'Negotiation'),
        ('Contract', 'Contract'),
        ('At Transfer', 'At Transfer'),
        ('Deal Lost', 'Deal Lost'),
        ('Deal Won', 'Deal Won'),
    )

    # Fields
    status = models.CharField(choices=STATUS_CHOICES, max_length=50)
    address = models.CharField(max_length=255)  
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    property_type = models.CharField(choices=PROPERTY_TYPE_CHOICES, max_length=50)
    mandate_type = models.CharField(choices=MANDATE_TYPE_CHOICES, max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_listed = models.DateField(default=timezone.now)
    mandate_expiry = models.DateField(default=date.today().strftime('%d/%m/%Y'))
    date_sold = models.DateField(blank=True, null=True)

    # Sellers and Buyers (linked to the Client model)
    seller_1 = models.ForeignKey(Client, related_name='seller_1', on_delete=models.SET_NULL, null=True, blank=True)
    seller_2 = models.ForeignKey(Client, related_name='seller_2', on_delete=models.SET_NULL, null=True, blank=True)
    buyer_1 = models.ForeignKey(Client, related_name='buyer_1', on_delete=models.SET_NULL, null=True, blank=True)
    buyer_2 = models.ForeignKey(Client, related_name='buyer_2', on_delete=models.SET_NULL, null=True, blank=True)

    # Methods
    def days_on_market(self):
        if not self.date_listed:
            return 0  # Default to 0 if listing date is missing

        end_date = self.date_sold if self.date_sold else timezone.localdate()
        return (end_date - self.date_listed).days

    def price_drop_percentage(self):
        if self.listing_price and self.sale_price:
            drop = (self.listing_price - self.sale_price) / self.listing_price * 100
            return drop
        return 0.0

    def __str__(self):
        return f"Property {self.id} - {self.listing_price} (Listing Price), {self.sale_price} (Sale Price)"

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"
