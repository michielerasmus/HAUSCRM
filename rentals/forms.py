from django import forms
from .models import Rental
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from clients.models import Client
from leads.models import Agent

User = get_user_model()

class RentalModelForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = [
            'status', 'address', 'area', 'city', 'property_type', 'mandate_type', 'rental_type', 'agent', 'placement_commission_percentage', 'management_commission_percentage', 'listing_price',
            'rental_price', 'date_listed','mandate_expiry', 'date_rented','rental_expiry', 'landlord_1', 'landlord_2', 'tenant_1', 'tenant_2'
        ]
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'date_listed': forms.DateInput(attrs={'type': 'date'}),
            'mandate_expiry': forms.DateInput(attrs={'type': 'date'}),
            'rrental_expiry': forms.DateInput(attrs={'type': 'date'}),
            'placement_commission_percentage': forms.NumberInput(attrs={'step': 0.01}),
            'management_commission_percentage': forms.NumberInput(attrs={'step': 0.01}),
            'listing_price': forms.NumberInput(attrs={'min': 0}),
            'rental_price': forms.NumberInput(attrs={'min': 0}),
        }

    # Custom field for Landlords and Tenants
    landlord_1 = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Landlord 1")
    landlord_2 = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Landlord 2")
    tenant_1 = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Tenant 1")
    tenant_2 = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Tenant 2")
