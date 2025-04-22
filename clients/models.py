from django.db import models
from datetime import date
from leads.models import Agent

class Client(models.Model):
    SOURCE_CHOICES = (
        ('Agent Referral', 'Agent Referral'),
        ('Cold Calling', 'Cold Calling'),
        ('Flyer', 'Flyer'),
        ('Hot List', 'Hot List'),
        ('Marketing Day', 'Marketing Day'),
        ('Newsletter', 'Newsletter'),
        ('Other', 'Other'),
        ('Outside Referral', 'Outside Referral'),
        ('Private Property', 'Private Property'),
        ('Property 24', 'Property 24'),
        ('Social Media', 'Social Media'),
        ('Walk In', 'Walk In'),
        ('Website', 'Website'),
    )

    ROLE_CHOICES = (
        ('Buyer', 'Buyer'),
        ('Landlord', 'Landlord'),
        ('Seller', 'Seller'),
        ('Tenant', 'Tenant'),
        ('Potential Buyer', 'Potential Buyer'),
        ('Potential Landlord', 'Potential Landlord'),
        ('Potential Seller', 'Potential Seller'),
        ('Potential Tenant', 'Potential Tenant'),
    )

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(choices=SOURCE_CHOICES, max_length=50)
    role = models.CharField(choices=ROLE_CHOICES, max_length=50)
    contacted = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    follow_up_date = models.DateField(blank=True, null=True)  # Allow null values
    birthday = models.DateField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name