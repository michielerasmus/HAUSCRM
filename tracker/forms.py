from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Tracker

User = get_user_model()

class TrackerModelForm(forms.ModelForm):
    class Meta: 
        model = Tracker
        fields = [
            'month',
            'agent',
            'calls_made',
            'appointments_set',
            'listings_secured',
            'showings_concluded',
            'deals_closed',
            'follow_ups',
            'social_media_posts',
            'database_growth',
        ]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2") 
