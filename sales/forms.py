from django import forms
from .models import Sale
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from clients.models import Client
from leads.models import Agent

User = get_user_model()

class SaleModelForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            'status', 'address', 'area', 'city', 'property_type', 'mandate_type', 'agent', 'commission_percentage', 'listing_price',
            'sale_price', 'date_listed','mandate_expiry', 'date_sold', 'seller_1', 'seller_2', 'buyer_1', 'buyer_2', 
        ]
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'date_listed': forms.DateInput(attrs={'type': 'date'}),
            'date_sold': forms.DateInput(attrs={'type': 'date'}),
            'commission_percentage': forms.NumberInput(attrs={'step': 0.01}),
            'listing_price': forms.NumberInput(attrs={'min': 0}),
            'sale_price': forms.NumberInput(attrs={'min': 0}),
        }

    # Custom field for Sellers and Buyers
    seller_1 = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Seller 1")
    seller_2 = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Seller 2")
    buyer_1 = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Buyer 1")
    buyer_2 = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Buyer 2")
